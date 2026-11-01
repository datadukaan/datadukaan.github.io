"""Day 2 - Fix 3: idempotent write - update, don't add.

The same batch of messages is loaded THREE times (a retried job, a re-sent file...).
Plain INSERT appends every time and the total keeps growing.
An upsert keyed on order_id (DuckDB's INSERT ... ON CONFLICT, the same idea as
MERGE in Delta Lake / Snowflake) leaves the table identical after every rerun.
"""
import duckdb

con = duckdb.connect()
con.sql("create table batch as select * from read_csv_auto('data/orders_received.csv')")
con.sql("create table sales_insert (order_id int, customer_id varchar, amount bigint, received_at timestamp)")
con.sql("create table sales_upsert (order_id int primary key, customer_id varchar, amount bigint, received_at timestamp)")

for run in (1, 2, 3):
    con.sql("insert into sales_insert select order_id, customer_id, amount, received_at from batch")
    con.sql("""
        insert into sales_upsert
        select order_id, customer_id, amount, max(received_at)   -- dedupe inside the batch first
        from batch group by all
        on conflict (order_id) do update set
            amount = excluded.amount, received_at = excluded.received_at
    """)
    ins = con.execute("select sum(amount), count(*) from sales_insert").fetchall()[0]
    ups = con.execute("select sum(amount), count(*) from sales_upsert").fetchall()[0]
    print(f"run {run}:  INSERT total {ins[0]:>9,} ({ins[1]:>2} rows)   |   UPSERT total {ups[0]:>9,} ({ups[1]:>2} rows)")
