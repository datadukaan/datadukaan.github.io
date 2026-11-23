-- Day 20 · Delta vs Iceberg vs Hudi: platform notes (not run in this repo)

-- ── Delta Lake (Spark / Databricks) ─────────────────────────────
CREATE TABLE shop.bills (bill_id BIGINT, bill_date DATE, party STRING, amount BIGINT, status STRING)
USING DELTA;
UPDATE shop.bills SET status = 'paid' WHERE party = 'CA Sharma';
DESCRIBE HISTORY shop.bills;
-- Deletion vectors: mark deleted rows instead of rewriting whole files
ALTER TABLE shop.bills SET TBLPROPERTIES ('delta.enableDeletionVectors' = 'true');

-- ── Apache Iceberg (Spark, Trino, Flink, Snowflake, Athena, …) ──
-- spark.sql.catalog.lake = org.apache.iceberg.spark.SparkCatalog  (+ a REST / Glue / Hive catalog)
CREATE TABLE lake.shop.bills (bill_id BIGINT, bill_date DATE, party STRING, amount BIGINT, status STRING)
USING iceberg PARTITIONED BY (months(bill_date));
-- Merge-on-read for update-heavy tables (format v2+)
ALTER TABLE lake.shop.bills SET TBLPROPERTIES (
  'write.update.mode' = 'merge-on-read', 'write.delete.mode' = 'merge-on-read', 'write.merge.mode' = 'merge-on-read');
SELECT * FROM lake.shop.bills.snapshots;
-- Trino reads the same table through the same catalog:
--   SELECT party, sum(amount) FROM iceberg.shop.bills GROUP BY party;

-- ── Apache Hudi (Spark, Flink) ──────────────────────────────────
CREATE TABLE shop.bills_hudi (bill_id BIGINT, bill_date DATE, party STRING, amount BIGINT, status STRING, ts TIMESTAMP)
USING hudi
TBLPROPERTIES (type = 'mor', primaryKey = 'bill_id', preCombineField = 'ts');
-- MOR = merge-on-read: updates land in small log files, compaction merges them later.
MERGE INTO shop.bills_hudi t USING updates u ON t.bill_id = u.bill_id
WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *;

-- ── Don't want to choose just one? ──────────────────────────────
-- Delta UniForm: write Delta, also publish Iceberg metadata for Iceberg readers
ALTER TABLE shop.bills SET TBLPROPERTIES (
  'delta.enableIcebergCompatV2' = 'true', 'delta.universalFormat.enabledFormats' = 'iceberg');
-- Apache XTable (incubating): translates metadata between Delta, Iceberg and Hudi,
-- leaving the Parquet files where they are.
