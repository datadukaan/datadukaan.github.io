-- Day 13 · Partitioning: where this lives in your tools (notes, not run)

-- Delta / Databricks: partition big tables by a low-cardinality column
CREATE TABLE sales (bill_date DATE, customer STRING, item STRING, qty_kg INT, month STRING)
USING DELTA PARTITIONED BY (month);
-- Databricks guidance: don't partition tables under ~1 TB; aim for >= ~1 GB per partition.

-- Partition pruning: filter on the partition column
SELECT sum(qty_kg) FROM sales WHERE month = '2026-10' AND item = 'sugar';

-- Small or medium tables: no partitions, cluster instead (Day 14)
CREATE TABLE tea_stall (bill_date DATE, item STRING, qty INT) USING DELTA CLUSTER BY (bill_date);

-- Generated column: partition by month while users filter on the date
CREATE TABLE sales2 (bill_date DATE, qty_kg INT,
  bill_month STRING GENERATED ALWAYS AS (date_format(bill_date, 'yyyy-MM')))
USING DELTA PARTITIONED BY (bill_month);

-- Snowflake: no user-managed partitions; micro-partitions + optional clustering key
ALTER TABLE sales CLUSTER BY (bill_date);

-- BigQuery: PARTITION BY DATE_TRUNC(bill_date, MONTH) CLUSTER BY item
