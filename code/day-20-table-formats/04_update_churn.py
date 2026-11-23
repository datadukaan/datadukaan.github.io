"""Fix 3 (why Hudi exists): constant updates to the same rows.

A copy-on-write table rewrites a whole data file to change a few rows.
Here: 20 rounds, each marks the same 50 bills paid/unpaid in a Delta table.
"""
import warnings; warnings.filterwarnings("ignore", category=DeprecationWarning)
import os, shutil, glob
import pyarrow.parquet as pq
from deltalake import DeltaTable, write_deltalake

path = "data/delta_churn"
shutil.rmtree(path, ignore_errors=True)
write_deltalake(path, pq.read_table("data/bills.parquet"))
size = lambda: sum(os.path.getsize(f) for f in glob.glob(f"{path}/*.parquet"))
start = size()

for r in range(20):
    s = "paid" if r % 2 == 0 else "unpaid"
    DeltaTable(path).update(predicate="bill_id <= 50", updates={"status": f"'{s}'"})

rows_total = DeltaTable(path).to_pyarrow_table(columns=["bill_id"]).num_rows
new_files = len(glob.glob(f"{path}/*.parquet")) - 1
print(f"rows you changed   : 20 rounds x 50 bills = {20 * 50:,}")
print(f"rows rewritten     : {new_files} files x {rows_total:,} = {new_files * rows_total:,}")
print(f"Parquet rewritten  : {(size() - start) / 1e6:.1f} MB")
print(f"table versions     : {DeltaTable(path).version() + 1}")
