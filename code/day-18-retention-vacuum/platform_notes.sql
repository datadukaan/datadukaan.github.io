-- Day 18 · Retention, VACUUM, cold tiers: where this lives in your tools (notes, not run)

-- Delta Lake / Databricks
VACUUM sales DRY RUN;                         -- list what would be deleted
VACUUM sales;                                 -- default: keep 7 days (168 hours)
VACUUM sales RETAIN 336 HOURS;                -- keep 14 days of time travel
ALTER TABLE sales SET TBLPROPERTIES (
  'delta.deletedFileRetentionDuration' = 'interval 14 days',   -- what VACUUM keeps
  'delta.logRetentionDuration'         = 'interval 30 days');  -- how long the log keeps history
-- Never set RETAIN below 168 hours while jobs may still read older versions
-- (spark.databricks.delta.retentionDurationCheck.enabled guards this).
-- Databricks predictive optimization can run VACUUM and OPTIMIZE automatically for Unity Catalog managed tables.

-- Row retention: actually delete old business data
DELETE FROM clickstream WHERE event_date < current_date() - INTERVAL 90 DAYS;
VACUUM clickstream;                           -- the deleted rows' files go only after VACUUM

-- Apache Iceberg
CALL catalog.system.expire_snapshots(table => 'db.sales', older_than => TIMESTAMP '2026-11-14 00:00:00');
CALL catalog.system.remove_orphan_files(table => 'db.sales');

-- Snowflake
ALTER TABLE sales SET DATA_RETENTION_TIME_IN_DAYS = 7;   -- Time Travel window (plus 7 days of Fail-safe)
CREATE TRANSIENT TABLE tmp_staging (...);               -- no Fail-safe storage for scratch data

-- Cloud storage tiers: lifecycle rules on the bucket / container
--   AWS S3 lifecycle: transition to STANDARD_IA after 90 days, GLACIER_DEEP_ARCHIVE after 365
--   Azure Blob lifecycle management: tierToCool / tierToArchive by daysAfterModificationGreaterThan
--   GCS Object Lifecycle: SetStorageClass NEARLINE / COLDLINE / ARCHIVE
-- Only tier files no active table version references (e.g. old partitions you've exported), or
-- the table will try to read archived files.
