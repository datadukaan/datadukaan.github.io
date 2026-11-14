"""Every small save makes a new file: 2,000 appends of 250 bills each -> 2,000 tiny Parquet files."""
import os, shutil, random, datetime as dt
import pyarrow as pa, pyarrow.parquet as pq
random.seed(12)
ITEMS = ["rice", "dal", "oil", "sugar", "samosa", "chai"]
OUT = "data/sales_small"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
for f in range(2000):
    d = dt.date(2026, 1, 1) + dt.timedelta(days=f * 318 // 2000)
    rows = [{"bill_date": d, "customer": f"C{random.randint(1, 300):03d}", "item": random.choice(ITEMS),
             "qty_kg": random.randint(1, 25), "amount": random.randint(50, 5000)} for _ in range(250)]
    pq.write_table(pa.Table.from_pylist(rows), f"{OUT}/part-{f:05d}.parquet")
size = sum(os.path.getsize(f"{OUT}/{n}") for n in os.listdir(OUT))
print(f"{OUT}: {len(os.listdir(OUT)):,} files, {size/1e6:.1f} MB total, avg {size/len(os.listdir(OUT))/1e3:.1f} KB per file")
