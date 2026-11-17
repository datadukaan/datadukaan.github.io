-- Day 15 · Medallion architecture on Databricks / Delta (notes, not run)

-- Bronze: Auto Loader lands files as-is, append-only, with lineage columns
-- spark.readStream.format("cloudFiles").option("cloudFiles.format", "csv")
--   .option("cloudFiles.schemaLocation", "/chk/slips/schema")
--   .load("/landing/slips/")
--   .select("*", F.current_timestamp().alias("_load_time"), F.col("_metadata.file_path").alias("_source_file"))
--   .writeStream.option("checkpointLocation", "/chk/slips").toTable("bronze.slips")

-- Silver: dedupe + cast + units, idempotent MERGE (Day 2), quarantine bad rows
MERGE INTO silver.slips t
USING (
  SELECT slip_id, item,
         CASE unit WHEN 'g' THEN try_cast(qty AS DOUBLE) / 1000 ELSE try_cast(qty AS DOUBLE) END AS qty,
         CASE unit WHEN 'g' THEN 'kg' ELSE unit END AS unit, received_at
  FROM bronze.slips
  WHERE try_cast(qty AS DOUBLE) IS NOT NULL
  QUALIFY row_number() OVER (PARTITION BY slip_id ORDER BY _load_time) = 1
) s ON t.slip_id = s.slip_id
WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *;

INSERT INTO silver.quarantine_slips
SELECT *, 'qty is not a number' AS reason FROM bronze.slips WHERE try_cast(qty AS DOUBLE) IS NULL;

-- Gold: business-ready aggregate
CREATE OR REPLACE TABLE gold.stock_by_item AS
SELECT item, sum(qty) AS qty, any_value(unit) AS unit FROM silver.slips GROUP BY item;

-- Delta Live Tables / Lakeflow: expectations do the quarantine for you
-- CONSTRAINT valid_qty EXPECT (qty IS NOT NULL) ON VIOLATION DROP ROW
