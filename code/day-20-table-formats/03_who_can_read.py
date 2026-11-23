"""'Nothing talks to it': an engine that ignores the log reads the wrong data.

Run 01 and 02 first. Both tables had one update, so their folders hold
old AND new Parquet files. Only the log/metadata says which ones are live.
"""
import warnings; warnings.filterwarnings("ignore", category=DeprecationWarning)
import duckdb
from deltalake import DeltaTable
from pyiceberg.catalog.sql import SqlCatalog
import os

con = duckdb.connect()
def raw(glob):
    return con.sql(f"SELECT count(*), count(*) FILTER (status = 'paid') FROM read_parquet('{glob}')").fetchall()[0]

wh = os.path.abspath("data/iceberg_wh")
ice = SqlCatalog("dukaan", uri=f"sqlite:///{wh}/catalog.db", warehouse=f"file://{wh}").load_table("shop.bills")
d = DeltaTable("data/delta_bills").to_pyarrow_table(columns=["status"])
i = ice.scan(selected_fields=("status",)).to_arrow()

rows = [
    ("Delta, read via its log",      d.num_rows, d["status"].to_pylist().count("paid")),
    ("Delta folder as plain Parquet", *raw("data/delta_bills/*.parquet")),
    ("Iceberg, read via catalog",    i.num_rows, i["status"].to_pylist().count("paid")),
    ("Iceberg folder as plain Parquet", *raw("data/iceberg_wh/shop/bills/data/*.parquet")),
]
print(f"{'how it was read':34} {'rows':>8} {'paid':>7}")
for name, n, p in rows:
    flag = "" if n == 100_000 else "   <- wrong"
    print(f"{name:34} {n:>8,} {p:>7,}{flag}")
