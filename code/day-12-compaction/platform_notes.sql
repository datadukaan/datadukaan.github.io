-- Day 12 · Compaction: where this lives in your tools (notes, not run)

-- Delta Lake / Databricks: Fix 1, compaction
OPTIMIZE sales;                                   -- bin-packs small files into ~1 GB files
OPTIMIZE sales WHERE bill_date >= '2026-11-01';   -- only recent partitions
OPTIMIZE sales ZORDER BY (item);                  -- compact + co-locate for data skipping (Day 14)
ALTER TABLE sales SET TBLPROPERTIES ('delta.targetFileSize' = '256mb');

-- Fix 2 + Fix 3: optimized writes and auto compaction
ALTER TABLE sales SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',    -- shuffle by partition before writing
  'delta.autoOptimize.autoCompact'   = 'true');   -- compact small files after each write
-- Databricks predictive optimization can run OPTIMIZE for Unity Catalog managed tables automatically.

-- Spark (any table format): fewer files per partition
-- df.repartition("month").write.partitionBy("month").parquet(path)
-- df.coalesce(8).write.parquet(path)

-- Apache Iceberg
CALL catalog.system.rewrite_data_files(table => 'db.sales');

-- Snowflake: micro-partitions are sized and maintained automatically;
--   for loading, aim for files of roughly 100-250 MB compressed.
