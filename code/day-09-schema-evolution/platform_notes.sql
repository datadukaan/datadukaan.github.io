-- Day 9 - schema changes on real platforms (notes, not run here).

-- Delta Lake: schema ENFORCEMENT is on by default - a write with an unexpected column fails.
-- Opt in to EVOLUTION for additive changes:
--   df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable("bills")
SET spark.databricks.delta.schema.autoMerge.enabled = true;       -- also lets MERGE add new columns
ALTER TABLE bills ADD COLUMNS (discount INT);                      -- or add it explicitly

-- Renames and drops on Delta need column mapping (no rewrite of data files):
ALTER TABLE bills SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name');
ALTER TABLE bills RENAME COLUMN amount TO price;

-- Databricks Auto Loader: new columns in incoming files
--   .option("cloudFiles.schemaEvolutionMode", "addNewColumns")   -- or "rescue" into _rescued_data

-- Snowflake: let COPY add columns that appear in the files
ALTER TABLE bills SET ENABLE_SCHEMA_EVOLUTION = TRUE;

-- dbt: enforce a model's contract (build fails if columns or types drift)
--   models:
--     - name: supplier_bills
--       config: { contract: { enforced: true } }
--       columns:
--         - { name: item,  data_type: varchar }
--         - { name: qty,   data_type: varchar }
--         - { name: price, data_type: integer, constraints: [{ type: not_null }] }
--   and on_schema_change: append_new_columns   for incremental models
