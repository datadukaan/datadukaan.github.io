-- Day 17 · Time travel: where this lives in your tools (notes, not run)

-- Delta Lake / Databricks
DESCRIBE HISTORY stock;                                   -- version, timestamp, user, operation, metrics
SELECT * FROM stock VERSION AS OF 42;
SELECT * FROM stock TIMESTAMP AS OF '2026-03-31';
SELECT * FROM stock@v42;                                  -- shorthand
RESTORE TABLE stock TO VERSION AS OF 42;                  -- or TO TIMESTAMP AS OF '...'
-- How far back you can go is limited by retention (Day 18):
--   delta.logRetentionDuration (default 30 days) and VACUUM's delta.deletedFileRetentionDuration (default 7 days)

-- Compare two versions: what did the bad job change?
SELECT * FROM stock VERSION AS OF 43
EXCEPT
SELECT * FROM stock VERSION AS OF 42;

-- PySpark
-- spark.read.option("versionAsOf", 42).table("stock")
-- spark.read.option("timestampAsOf", "2026-03-31").table("stock")

-- Snowflake: Time Travel + UNDROP (retention: DATA_RETENTION_TIME_IN_DAYS, 1 day by default, up to 90 on Enterprise)
SELECT * FROM stock AT(TIMESTAMP => '2026-03-31 23:59:00'::timestamp_ltz);
SELECT * FROM stock BEFORE(STATEMENT => '<query_id_of_bad_update>');
CREATE TABLE stock_fixed CLONE stock BEFORE(STATEMENT => '<query_id_of_bad_update>');

-- Apache Iceberg
SELECT * FROM stock FOR VERSION AS OF 1234567890;         -- snapshot id
SELECT * FROM stock FOR TIMESTAMP AS OF TIMESTAMP '2026-03-31 23:59:00';
CALL catalog.system.rollback_to_snapshot('db.stock', 1234567890);
