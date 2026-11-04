"""Day 4 - Fix 3: a lookback window.

Same incremental load, but each night re-reads a little BEFORE the bookmark
(here 1 hour). Rows already loaded come back again, so the write must be an
upsert (Day 2's idempotent write) - then re-reading them changes nothing, and
late-committed rows like order 1827 are caught.
"""
import duckdb

con = duckdb.connect()
con.execute("create table target (order_id int primary key, amount int, created_at timestamp, updated_at timestamp)")
upsert = """insert into target select * from read_csv_auto(?) where updated_at > ?::timestamp - interval 1 hour
            on conflict (order_id) do update set amount = excluded.amount, updated_at = excluded.updated_at"""

con.execute("insert into target select * from read_csv_auto('data/source_night1.csv')")
mark = con.execute("select max(updated_at) from target").fetchall()[0][0]
print("Tuesday night: high-water mark =", mark)

read = con.execute("select count(*) from read_csv_auto('data/source_night2.csv') where updated_at > ?::timestamp - interval 1 hour",
                   [mark]).fetchall()[0][0]
con.execute(upsert, ["data/source_night2.csv", mark])
print("Wednesday night: rows read from source =", read, "(lookback 1 hour)")

inc = con.execute("select count(*), sum(amount) from target").fetchall()[0]
full = con.execute("select count(*), sum(amount) from read_csv_auto('data/source_night2.csv')").fetchall()[0]
print(f"incremental + lookback: {inc[0]} orders, total {inc[1]:,}")
print(f"full reload:            {full[0]} orders, total {full[1]:,}")
print("match:", inc == full)
