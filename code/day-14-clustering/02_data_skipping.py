"""Fix 1: every block keeps min/max per column. It skips well on bill_date (already in order)
but not on customer, because every block holds customers from A to Z."""
import glob, datetime as dt
import pyarrow.parquet as pq
from common import show
md = pq.ParquetFile("data/arrival/2026-03.parquet").metadata
for col in ["bill_date", "customer"]:
    st = md.row_group(0).column(md.schema.names.index(col)).statistics
    print(f"March, block 0, {col:9s}: min {st.min}  max {st.max}")
show("WHERE bill_date = '2026-03-15'", "data/arrival", "bill_date", dt.date(2026, 3, 15))
show("WHERE customer = 'Patel Caterers'", "data/arrival", "customer", "Patel Caterers")
