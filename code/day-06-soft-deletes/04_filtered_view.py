"""Day 6 - Fix 3: a filtered view - reports read only active rows.

Soft-deleted rows stay in the table (for audit, undo, history), so every
report must leave them out. Instead of trusting each analyst to remember
"WHERE NOT is_deleted", publish a view that does it once, and point
dashboards at the view.
"""
import duckdb

con = duckdb.connect()
con.execute("create table orders as select * from read_csv_auto('data/orders_night2_soft_delete.csv')")
con.execute("create view orders_active as select * exclude (is_deleted) from orders where not is_deleted")

for name in ("orders", "orders_active"):
    n, total = con.execute(f"select count(*), sum(amount) from {name}").fetchall()[0]
    print(f"report from {name:<14} {n:>2} orders, total Rs {total:,}")
