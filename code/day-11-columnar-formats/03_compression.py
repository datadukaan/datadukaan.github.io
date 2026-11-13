"""Fix 2: repeated values are stored once (dictionary + run-length encoding), then compressed."""
import os
import pyarrow.csv as pv, pyarrow.parquet as pq

table = pv.read_csv("data/bills.csv")
csv_mb = os.path.getsize("data/bills.csv") / 1e6
print(f"{'bills.csv':28s} {csv_mb:6.1f} MB")
for codec in ["none", "snappy", "zstd"]:
    path = f"data/bills_{codec}.parquet"
    pq.write_table(table, path, compression=codec)
    mb = os.path.getsize(path) / 1e6
    print(f"{'bills.parquet (' + codec + ')':28s} {mb:6.1f} MB   {csv_mb/mb:4.1f}x smaller")

col = pq.ParquetFile("data/bills_zstd.parquet").metadata.row_group(0).column(2)   # the item column
print(f"\nitem column encodings: {col.encodings}")
print(f"'samosa' appears {table.column('item').to_pylist().count('samosa'):,} times, stored once in the dictionary")
