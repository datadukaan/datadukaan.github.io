-- Day 11 · Columnar formats: where this lives in your tools (notes, not run)

-- Spark / Databricks: write Parquet or Delta (Delta = Parquet files + a transaction log)
-- df.write.format("delta").partitionBy("bill_year").save("/lake/bills")
CREATE TABLE bills USING DELTA AS SELECT * FROM csv.`/landing/bills.csv`;

-- Help data skipping: keep related values together so min/max ranges don't overlap
OPTIMIZE bills ZORDER BY (bill_date);          -- or liquid clustering:
ALTER TABLE bills CLUSTER BY (bill_date);

-- Delta keeps min/max stats for the first 32 columns by default
ALTER TABLE bills SET TBLPROPERTIES ('delta.dataSkippingNumIndexedCols' = '8');

-- Compression codec for Parquet files written by Spark
SET spark.sql.parquet.compression.codec = zstd;

-- Snowflake: tables are stored in columnar micro-partitions with min/max metadata
--   automatically; clustering keys improve pruning on big tables
ALTER TABLE bills CLUSTER BY (bill_date);
-- Unload to Parquet: COPY INTO @stage/bills/ FROM bills FILE_FORMAT = (TYPE = PARQUET);

-- dbt (Databricks adapter): {{ config(materialized='table', file_format='delta') }}
