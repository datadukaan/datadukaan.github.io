-- Day 10 · Small files: where the fixes live in your tools (notes, not run)

-- Databricks Auto Loader: file notification mode + batch limits (Fix 1, 2, 3)
-- spark.readStream.format("cloudFiles")
--   .option("cloudFiles.format", "json")
--   .option("cloudFiles.useNotifications", "true")   -- Event Grid / SQS queue, no LIST
--   .option("cloudFiles.maxFilesPerTrigger", 50)
--   .load("abfss://landing@acct.dfs.core.windows.net/orders/")
--   .writeStream.trigger(processingTime="5 minutes") ...

-- Delta Lake: compact many small files into fewer big ones
OPTIMIZE orders;
ALTER TABLE orders SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact'   = 'true');

-- Snowflake: Snowpipe loads on cloud storage events (file notification)
CREATE PIPE orders_pipe AUTO_INGEST = TRUE AS
  COPY INTO orders FROM @landing_stage FILE_FORMAT = (TYPE = JSON);
-- Snowflake recommends files of roughly 100–250 MB compressed for loading.

-- Azure Data Factory: Storage event trigger (BlobCreated) instead of a schedule
-- Airflow: a sensor with mode="reschedule", or dataset-driven scheduling
