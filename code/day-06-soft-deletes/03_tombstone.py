"""Day 6 - Fix 2: tombstone - send a "deleted" message to every copy.

When the source really deletes a row, log-based CDC (Day 5) still sees it in the
database log and emits a delete event: op = 'd', the key, and no values.
That event is the tombstone. Every copy that applies it removes (or flags) the row.
"""
import duckdb

con = duckdb.connect()
con.execute("create table copy as select *, false as is_deleted from read_csv_auto('data/orders_night1.csv')")
events = con.execute("select lsn, op, order_id from read_csv_auto('data/cdc_events.csv') order by lsn").fetchall()
print("CDC events:", events)

for lsn, op, oid in events:
    if op == "d":
        # option A: remove the row from the copy
        # con.execute("delete from copy where order_id = ?", [oid])
        # option B (used here): keep history, flag it like a soft delete
        con.execute("update copy set is_deleted = true where order_id = ?", [oid])

print(con.execute("select order_id, amount, is_deleted from copy where order_id = 7").fetchall())
