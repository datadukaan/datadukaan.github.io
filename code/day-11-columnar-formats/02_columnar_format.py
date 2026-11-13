"""Fix 1: save as Parquet (column by column) and read only the tax column."""
import os
import pyarrow.csv as pv, pyarrow.parquet as pq

pq.write_table(pv.read_csv("data/bills.csv"), "data/bills.parquet", row_group_size=100_000)
meta = pq.ParquetFile("data/bills.parquet").metadata
tax_i = meta.schema.names.index("tax")
tax_bytes = sum(meta.row_group(g).column(tax_i).total_compressed_size for g in range(meta.num_row_groups))

tax = pq.read_table("data/bills.parquet", columns=["tax"])   # only the tax column chunks are read
print(f"file size      : {os.path.getsize('data/bills.parquet')/1e6:.1f} MB")
print(f"bytes read     : {tax_bytes/1e6:.1f} MB (only the tax column)")
print(f"total tax      : Rs {sum(tax.column('tax').to_pylist()):,.0f}")
