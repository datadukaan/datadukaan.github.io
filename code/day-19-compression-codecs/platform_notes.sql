-- Day 19 · Snappy vs ZSTD: where this lives in your tools (notes, not run)

-- Spark: default Parquet codec is snappy
SET spark.sql.parquet.compression.codec = zstd;           -- for the whole session
-- df.write.option("compression", "zstd").parquet(path)   -- per write

-- Delta Lake / Databricks
ALTER TABLE orders_archive SET TBLPROPERTIES ('delta.parquet.compression.codec' = 'zstd');
-- Existing files keep their codec; OPTIMIZE (or a rewrite) re-encodes them.

-- Apache Iceberg (default zstd since Iceberg 1.4)
ALTER TABLE db.orders SET TBLPROPERTIES ('write.parquet.compression-codec' = 'zstd',
                                         'write.parquet.compression-level' = '3');

-- DuckDB
COPY orders TO 'orders.parquet' (FORMAT parquet, COMPRESSION zstd, COMPRESSION_LEVEL 3);

-- Snowflake / BigQuery compress storage automatically; you choose codecs only for files you export.
