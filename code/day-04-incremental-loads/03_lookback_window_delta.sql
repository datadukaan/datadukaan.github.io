-- Day 4 on Delta Lake / Databricks: incremental load with a high-water mark and a lookback.
-- load_state holds one row per table: the latest updated_at already loaded.

MERGE INTO orders AS t
USING (
    SELECT * FROM source_orders
    WHERE updated_at > (SELECT high_water_mark FROM load_state WHERE table_name = 'orders')
                       - INTERVAL 1 HOUR                                 -- lookback window
) AS s
ON t.order_id = s.order_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- move the bookmark only after the MERGE succeeded
UPDATE load_state
SET high_water_mark = (SELECT MAX(updated_at) FROM orders)
WHERE table_name = 'orders';
