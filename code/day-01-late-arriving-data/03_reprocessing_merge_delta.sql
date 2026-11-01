-- Day 1 - Fix 3: nightly reprocessing with MERGE (Delta Lake / Databricks SQL).
-- Recount the last 3 days from the raw orders, and update ONLY the days whose totals changed.
-- A runnable version of the same logic (DuckDB, no cluster needed) is in 03_reprocessing_merge.py.

MERGE INTO daily_sales AS t
USING (
  SELECT CAST(event_time AS DATE) AS sale_date,
         SUM(amount)              AS total,
         COUNT(*)                 AS orders
  FROM   raw_orders
  WHERE  event_time >= date_sub(current_date(), 3)        -- lookback window
  GROUP  BY CAST(event_time AS DATE)
) AS s
ON t.sale_date = s.sale_date
WHEN MATCHED AND (t.total <> s.total OR t.orders <> s.orders) THEN
  UPDATE SET t.total = s.total, t.orders = s.orders, t.updated_at = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT (sale_date, total, orders, updated_at)
  VALUES (s.sale_date, s.total, s.orders, current_timestamp());

-- Events older than the lookback window go to a dead-letter table for review
-- instead of silently changing old, already-reported numbers.
INSERT INTO late_orders_dead_letter
SELECT *, current_timestamp() AS quarantined_at
FROM   raw_orders
WHERE  CAST(event_time AS DATE) < date_sub(current_date(), 3)
  AND  ingest_time >= date_sub(current_date(), 1);
