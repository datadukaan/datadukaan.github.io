"""Fix 3: each row group keeps min/max per column, so a filter can skip whole blocks."""
import datetime as dt
import pyarrow.parquet as pq, pyarrow.dataset as ds, duckdb

pf = pq.ParquetFile("data/bills.parquet")          # written in 02, 10 row groups in date order
di = pf.metadata.schema.names.index("bill_date")
need = []
for g in range(pf.metadata.num_row_groups):
    st = pf.metadata.row_group(g).column(di).statistics
    keep = st.max >= dt.date(2026, 1, 1)
    need.append(keep)
    print(f"row group {g}: min {st.min}  max {st.max}  -> {'read' if keep else 'skip'}")
print(f"\nWHERE bill_date >= '2026-01-01': read {sum(need)} of {len(need)} row groups")

# Engines do this for you. pyarrow:
t = ds.dataset("data/bills.parquet").to_table(columns=["tax"], filter=ds.field("bill_date") >= dt.date(2026, 1, 1))
print(f"pyarrow   : {t.num_rows:,} bills in 2026, tax Rs {sum(t.column('tax').to_pylist()):,.0f}")
# DuckDB (the same idea as Spark / Databricks / Snowflake pruning):
r = duckdb.sql("""SELECT count(*), round(sum(tax)) FROM 'data/bills.parquet'
                  WHERE bill_date >= DATE '2026-01-01'""").fetchall()[0]
print(f"duckdb    : {r[0]:,} bills in 2026, tax Rs {r[1]:,.0f}")
