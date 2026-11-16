"""Fix 3: Z-ordering - sort by customer AND item together by interleaving their bits,
so filters on either column skip blocks."""
import glob, os, shutil
import pyarrow as pa, pyarrow.compute as pc, pyarrow.parquet as pq
from common import show

def zkey(a, b, bits=10):
    z = 0
    for i in range(bits):
        z |= ((a >> i) & 1) << (2*i + 1) | ((b >> i) & 1) << (2*i)
    return z

t = pa.concat_tables(pq.read_table(f) for f in sorted(glob.glob("data/arrival/*.parquet")))
cust = {c: i for i, c in enumerate(sorted(set(t.column("customer").to_pylist())))}
item = {c: i for i, c in enumerate(sorted(set(t.column("item").to_pylist())))}
# scale both ranks to 0..1023 so each column gets equal weight in the curve
z = [zkey(cust[c] * 1023 // (len(cust) - 1), item[i] * 1023 // (len(item) - 1))
     for c, i in zip(t.column("customer").to_pylist(), t.column("item").to_pylist())]
t = t.append_column("_z", pa.array(z)).sort_by("_z").drop(["_z"])
shutil.rmtree("data/zorder", ignore_errors=True); os.makedirs("data/zorder")
for k in range(12):                                             # same 12 files, now z-ordered
    pq.write_table(t.slice(k*50_000, 50_000), f"data/zorder/part-{k:02d}.parquet", row_group_size=5_000)

# compare with a linear sort on customer across the whole table
shutil.rmtree("data/linear", ignore_errors=True); os.makedirs("data/linear")
lt = t.sort_by([("customer", "ascending"), ("item", "ascending")])
for k in range(12):
    pq.write_table(lt.slice(k*50_000, 50_000), f"data/linear/part-{k:02d}.parquet", row_group_size=5_000)

for label, folder in [("linear sort (customer, item)", "data/linear"), ("Z-order (customer, item)", "data/zorder")]:
    print(label)
    show("  WHERE customer = 'Patel Caterers'", folder, "customer", "Patel Caterers")
    show("  WHERE item = 'sugar'", folder, "item", "sugar")
