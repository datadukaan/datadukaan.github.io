-- Day 5 on Delta Lake / Databricks: apply a CDC feed to the copy with MERGE.
-- menu_changes holds the CDC events (op = 'c' insert, 'u' update, 'd' delete, lsn = log position).

MERGE INTO menu_copy AS t
USING (
    -- one event per key: the latest by log position
    SELECT * FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY item_id ORDER BY lsn DESC) AS rn
        FROM menu_changes
        WHERE lsn > (SELECT last_lsn FROM cdc_checkpoint WHERE table_name = 'menu')   -- resume point
    ) WHERE rn = 1
) AS s
ON t.item_id = s.item_id
WHEN MATCHED AND s.op = 'd' THEN DELETE
WHEN MATCHED THEN UPDATE SET t.item = s.item, t.price = s.price
WHEN NOT MATCHED AND s.op != 'd' THEN INSERT (item_id, item, price) VALUES (s.item_id, s.item, s.price);

UPDATE cdc_checkpoint
SET last_lsn = (SELECT MAX(lsn) FROM menu_changes)
WHERE table_name = 'menu';

-- On Databricks you can also let the platform do this:
--   Delta Lake Change Data Feed:  SELECT * FROM table_changes('menu', <start_version>)
--   Lakeflow Declarative Pipelines (DLT):  APPLY CHANGES INTO ... KEYS (item_id) SEQUENCE BY lsn
--                                          APPLY AS DELETE WHEN op = 'd'
-- Structured Streaming stores its checkpoint for you in checkpointLocation.
