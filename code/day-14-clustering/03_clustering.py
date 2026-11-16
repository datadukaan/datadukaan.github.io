"""Fix 2: clustering - sort rows by the column people filter on, so each block covers a narrow range."""
import glob, os, shutil
import pyarrow.parquet as pq
from common import show
shutil.rmtree("data/clustered", ignore_errors=True); os.makedirs("data/clustered")
for f in sorted(glob.glob("data/arrival/*.parquet")):           # keep monthly files, sort inside each
    t = pq.read_table(f).sort_by([("customer", "ascending")])
    pq.write_table(t, f"data/clustered/{os.path.basename(f)}", row_group_size=5_000)
md = pq.ParquetFile("data/clustered/2026-03.parquet").metadata; ci = md.schema.names.index("customer")
for g in (0, 9):
    st = md.row_group(g).column(ci).statistics
    print(f"March, block {g}: customers {st.min} .. {st.max}")
show("before (arrival order)", "data/arrival", "customer", "Patel Caterers")
show("after CLUSTER BY customer", "data/clustered", "customer", "Patel Caterers")
show("but WHERE item = 'sugar'", "data/clustered", "item", "sugar")
