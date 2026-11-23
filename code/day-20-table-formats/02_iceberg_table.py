"""Fix 2: Iceberg = Parquet files + metadata JSON + manifest files, tracked by a catalog."""
import os, shutil
import pyarrow as pa, pyarrow.parquet as pq
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.expressions import EqualTo
from _show import tree

wh = os.path.abspath("data/iceberg_wh")
shutil.rmtree(wh, ignore_errors=True); os.makedirs(wh)
catalog = SqlCatalog("dukaan", uri=f"sqlite:///{wh}/catalog.db", warehouse=f"file://{wh}")
catalog.create_namespace("shop")
bills = pq.read_table("data/bills.parquet")

tbl = catalog.create_table("shop.bills", schema=bills.schema)
tbl.append(bills)                                          # snapshot 1
ca = tbl.scan(row_filter=EqualTo("party", "CA Sharma")).to_arrow()
ca = ca.set_column(ca.schema.get_field_index("status"), "status", pa.array(["paid"] * ca.num_rows))
tbl.overwrite(ca, overwrite_filter=EqualTo("party", "CA Sharma"))  # delete + append

print("Folder:")
tree(wh, max_files=14)
print("\nSnapshots:")
for s in tbl.refresh().snapshots():
    print(f"  {s.snapshot_id}: {s.summary.operation.value}")
t = tbl.scan().to_arrow()
print(f"\nRows: {t.num_rows:,} · paid: {sum(1 for s in t['status'].to_pylist() if s == 'paid'):,}")
print(f"Catalog points at: {os.path.relpath(tbl.metadata_location.replace('file://', ''))}")
