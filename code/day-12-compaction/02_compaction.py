"""Fix 1: compaction - rewrite many small files into a few big ones (what Delta's OPTIMIZE does)."""
import os, shutil
import pyarrow.dataset as ds, pyarrow.parquet as pq
from common import files, rice_query

SRC, DST = "data/sales_small", "data/sales_compacted"
TARGET_ROWS = 200_000          # Delta's default target is ~1 GB per file; our demo data is tiny
shutil.rmtree(DST, ignore_errors=True); os.makedirs(DST)
table = ds.dataset(SRC).to_table()
for i, start in enumerate(range(0, table.num_rows, TARGET_ROWS)):        # bin-pack rows into big files
    pq.write_table(table.slice(start, TARGET_ROWS), f"{DST}/part-{i:05d}.parquet")

for label, folder in [("before", SRC), ("after ", DST)]:
    n, size = files(folder); kg, sec = rice_query(folder)
    print(f"{label}: {n:>5,} files, avg {size/n/1e3:>7.1f} KB  ->  rice {kg:,} kg in {sec*1000:.0f} ms")
