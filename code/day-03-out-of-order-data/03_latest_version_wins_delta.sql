-- Day 3 - Fix 3 on Delta Lake / Databricks: only newer versions update the row.

MERGE INTO orders AS t
USING (
    -- several versions of one order can land in one batch: keep the highest seq first
    SELECT order_id, seq, amount, event_time
    FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY seq DESC) AS rn
        FROM order_messages
    )
    WHERE rn = 1
) AS s
ON t.order_id = s.order_id
WHEN MATCHED AND s.seq > t.seq THEN                -- the guard: old never overwrites new
    UPDATE SET t.seq = s.seq, t.amount = s.amount, t.event_time = s.event_time
WHEN NOT MATCHED THEN
    INSERT (order_id, seq, amount, event_time) VALUES (s.order_id, s.seq, s.amount, s.event_time);
