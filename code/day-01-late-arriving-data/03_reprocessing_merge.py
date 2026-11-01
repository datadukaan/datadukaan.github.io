"""Day 1 - Fix 3: nightly reprocessing with MERGE (runnable with DuckDB, no cluster needed).

Starting point: the daily_sales table the stream produced (Sunday stuck at 2,00,000).
The nightly job recounts the last 3 days from raw orders and MERGEs the result,
updating only days that changed. Orders older than the lookback go to a dead-letter table.

Run:  python 03_reprocessing_merge.py
"""
import duckdb

RUN_DATE = "2026-10-27"   # the night the job runs (Tuesday)
LOOKBACK_DAYS = 3

con = duckdb.connect()
con.execute("""CREATE TABLE raw_orders AS
               SELECT * FROM read_csv('data/orders.csv', header=true,
                      columns={'order_id':'INT','amount':'BIGINT','event_time':'TIMESTAMP','ingest_time':'TIMESTAMP'})""")

# What the streaming job wrote (late Sunday orders were dropped by the watermark).
con.execute("""CREATE TABLE daily_sales (sale_date DATE PRIMARY KEY, total BIGINT, orders INT, updated_at TIMESTAMP);
               INSERT INTO daily_sales VALUES
               ('2026-10-24', 190000, 6, '2026-10-24 23:59'),
               ('2026-10-25', 200000, 5, '2026-10-25 23:59'),
               ('2026-10-26', 103000, 3, '2026-10-26 23:59'),
               ('2026-10-27',  60000, 1, '2026-10-27 23:59');""")
print("Before reprocessing:"); print(con.sql("SELECT * EXCLUDE updated_at FROM daily_sales ORDER BY 1"))

window_start = f"DATE '{RUN_DATE}' - INTERVAL {LOOKBACK_DAYS - 1} DAY"
con.execute(f"""
MERGE INTO daily_sales AS t
USING (SELECT CAST(event_time AS DATE) AS sale_date, SUM(amount) AS total, COUNT(*) AS orders
       FROM raw_orders
       WHERE CAST(event_time AS DATE) >= {window_start} AND CAST(event_time AS DATE) <= DATE '{RUN_DATE}'
       GROUP BY 1) AS s
ON t.sale_date = s.sale_date
WHEN MATCHED AND (t.total <> s.total OR t.orders <> s.orders) THEN
  UPDATE SET total = s.total, orders = s.orders, updated_at = TIMESTAMP '{RUN_DATE} 23:59'
WHEN NOT MATCHED THEN
  INSERT VALUES (s.sale_date, s.total, s.orders, TIMESTAMP '{RUN_DATE} 23:59')
""")

con.execute(f"""CREATE TABLE late_orders_dead_letter AS
                SELECT *, TIMESTAMP '{RUN_DATE} 23:59' AS quarantined_at FROM raw_orders
                WHERE CAST(event_time AS DATE) < {window_start}
                  AND CAST(ingest_time AS DATE) = DATE '{RUN_DATE}'""")

print("After reprocessing (only Sunday changed):")
print(con.sql("SELECT sale_date, total, orders, updated_at FROM daily_sales ORDER BY 1"))
print("Dead-letter (too late to auto-fix, needs review):")
print(con.sql("SELECT order_id, amount, event_time, ingest_time FROM late_orders_dead_letter"))
