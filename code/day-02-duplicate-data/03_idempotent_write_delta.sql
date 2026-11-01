-- Day 2 - Fix 3 on Delta Lake / Databricks: MERGE keyed on order_id.
-- Run it once or ten times: the target ends up the same.

MERGE INTO sales AS t
USING (
    -- dedupe inside the incoming batch first, MERGE fails if two source rows match one target row
    SELECT order_id, customer_id, amount, received_at
    FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY received_at DESC) AS rn
        FROM raw_messages
    )
    WHERE rn = 1
) AS s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET t.amount = s.amount, t.received_at = s.received_at
WHEN NOT MATCHED THEN INSERT (order_id, customer_id, amount, received_at)
                      VALUES (s.order_id, s.customer_id, s.amount, s.received_at);
