-- Day 6 on Delta Lake / Databricks.

-- Fix 1: soft delete in the source instead of DELETE
UPDATE orders SET is_deleted = true, updated_at = current_timestamp() WHERE order_id = 7;

-- Fix 2: apply CDC tombstones (op = 'd') to the copy
MERGE INTO orders_copy AS t
USING order_changes AS s
ON t.order_id = s.order_id
WHEN MATCHED AND s.op = 'd' THEN UPDATE SET t.is_deleted = true, t.updated_at = s.changed_at
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED AND s.op != 'd' THEN INSERT *;

-- Fix 3: reports read a filtered view
CREATE OR REPLACE VIEW orders_active AS
SELECT * EXCEPT (is_deleted) FROM orders_copy WHERE NOT is_deleted;

-- Later: purge soft-deleted rows past their retention period, then clean old files
DELETE FROM orders_copy WHERE is_deleted AND updated_at < current_date() - INTERVAL 90 DAYS;
VACUUM orders_copy RETAIN 168 HOURS;
