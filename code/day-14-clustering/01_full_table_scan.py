"""The problem: the table is split by month, but Patel asks by customer -> every block is read."""
import duckdb
from common import show
n, total = duckdb.sql("""SELECT count(*), sum(amount) FROM 'data/arrival/*.parquet'
                         WHERE customer = 'Patel Caterers'""").fetchall()[0]
print(f"Patel's bills: {n:,}, total Rs {total:,}")
show("WHERE customer = 'Patel Caterers'", "data/arrival", "customer", "Patel Caterers")
