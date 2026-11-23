"""Fix 1: Delta Lake = Parquet files + a JSON transaction log (_delta_log)."""
import warnings; warnings.filterwarnings("ignore", category=DeprecationWarning)
import shutil, json, glob
import pyarrow.parquet as pq
from deltalake import DeltaTable, write_deltalake
from _show import tree

path = "data/delta_bills"
shutil.rmtree(path, ignore_errors=True)
bills = pq.read_table("data/bills.parquet")

write_deltalake(path, bills)                              # version 0
dt = DeltaTable(path)
dt.update(predicate="party = 'CA Sharma'", updates={"status": "'paid'"})   # version 1

print("Folder:")
tree(path)
print("\nHistory:")
for h in sorted(DeltaTable(path).history(), key=lambda h: h['version']):
    print(f"  v{h['version']}: {h['operation']}")
last = sorted(glob.glob(f"{path}/_delta_log/*.json"))[-1]
acts = [list(json.loads(l))[0] for l in open(last)]
print(f"\nLast log file holds actions: {sorted(set(acts))}")
t = DeltaTable(path).to_pyarrow_table()
print(f"Rows: {t.num_rows:,} · paid: {sum(1 for s in t['status'].to_pylist() if s == 'paid'):,}")
