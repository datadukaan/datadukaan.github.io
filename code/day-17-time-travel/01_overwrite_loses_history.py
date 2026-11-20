"""The problem: a plain file overwritten every day keeps only today's numbers."""
import os
import pyarrow as pa, pyarrow.parquet as pq
from common import SNAPSHOTS, stock, total
os.makedirs("data", exist_ok=True)
for ts, o, d, r, op, user in SNAPSHOTS:
    pq.write_table(pa.Table.from_pylist(stock(o, d, r)), "data/stock.parquet")    # overwrite
pq.write_table(pa.Table.from_pylist(stock(0, 0, 0)), "data/stock.parquet")        # one wrong UPDATE
print("today        :", total(pq.read_table("data/stock.parquet").to_pylist()), "kg")
print("31 March     : ?  (overwritten, no copy anywhere)")
print("last Friday  : ?  (overwritten)")
print("undo the bad UPDATE: impossible")
