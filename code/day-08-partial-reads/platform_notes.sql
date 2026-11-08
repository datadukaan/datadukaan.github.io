-- Day 8 - where this lives on real platforms (notes, not run here).

-- Delta Lake / Iceberg / Hudi: every write is a transaction. New data files are
-- invisible until one commit entry is added to the table's log, so readers
-- never see half a write - atomic rename + success marker, built in.
INSERT INTO sweets SELECT * FROM staging_sweets;      -- readers see all of it, or none

-- Snowflake: COPY INTO loads each file in one transaction, and its load
-- history skips files it already loaded.
COPY INTO sweets FROM @landing/sweets/ FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);

-- Airflow: wait for the marker before the downstream task runs
--   FileSensor(task_id="wait_for_success", filepath="sweets/dt={{ ds }}/_SUCCESS", poke_interval=60)

-- Databricks Auto Loader / ADF storage events fire per file: have the producer
-- upload to a temp prefix and move/rename into the watched folder when done.
