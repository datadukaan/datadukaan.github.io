"""Day 3 - Fix 3: latest version wins - an old message never overwrites a new one.

Messages are applied one by one IN THE ORDER THEY ARRIVED, like a streaming
consumer would. A plain upsert lets whatever arrives last win. A conditional
upsert only updates when the incoming seq is higher than the stored one.
(DuckDB INSERT ... ON CONFLICT ... WHERE; MERGE ... WHEN MATCHED AND s.seq > t.seq
does the same in Delta Lake / Snowflake.)
"""
import duckdb

con = duckdb.connect()
con.execute("create table msgs as select * from read_csv_auto('data/order_messages.csv') order by received_at")
for name in ("plain", "guarded"):
    con.execute(f"create table {name} (order_id int primary key, seq int, amount int)")

for mid, oid, seq, amt in con.execute("select message_id, order_id, seq, amount from msgs").fetchall():
    con.execute("insert into plain values (?, ?, ?) on conflict (order_id) do update set seq = excluded.seq, amount = excluded.amount",
                [oid, seq, amt])
    con.execute("""insert into guarded values (?, ?, ?)
                   on conflict (order_id) do update set seq = excluded.seq, amount = excluded.amount
                   where excluded.seq > guarded.seq""", [oid, seq, amt])
    p = con.execute("select amount from plain where order_id = ?", [oid]).fetchall()[0][0]
    g = con.execute("select amount from guarded where order_id = ?", [oid]).fetchall()[0][0]
    print(f"{mid}: order {oid} seq {seq} Rs {amt:>5}  ->  plain upsert {p:>5}  |  latest-version-wins {g:>5}")

for name in ("plain", "guarded"):
    print(name, "total:", con.execute(f"select sum(amount) from {name}").fetchall()[0][0])
