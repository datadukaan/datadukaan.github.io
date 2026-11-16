-- Day 14 · Clustering, Z-ordering, data skipping: where this lives in your tools (notes, not run)

-- Delta Lake: data skipping is automatic - min/max stats per file for the first 32 columns
ALTER TABLE sales SET TBLPROPERTIES ('delta.dataSkippingStatsColumns' = 'bill_date,customer,item');

-- Z-ordering (Delta OPTIMIZE): co-locate rows by one or more columns
OPTIMIZE sales ZORDER BY (customer, item);

-- Liquid clustering (Databricks / Delta 3.x): replaces partitioning + ZORDER for new tables
CREATE TABLE sales (bill_date DATE, customer STRING, item STRING, amount INT)
USING DELTA CLUSTER BY (customer, item);
ALTER TABLE sales CLUSTER BY (customer);      -- change keys later without rewriting
OPTIMIZE sales;                               -- clusters new data incrementally

-- Snowflake: automatic pruning on micro-partition min/max; clustering keys for big tables
ALTER TABLE sales CLUSTER BY (customer, item);
SELECT SYSTEM$CLUSTERING_INFORMATION('sales', '(customer)');

-- BigQuery: CREATE TABLE ... PARTITION BY bill_date CLUSTER BY customer, item
-- Iceberg: ALTER TABLE sales WRITE ORDERED BY customer, item;
--          CALL system.rewrite_data_files(table => 'db.sales', strategy => 'sort',
--               sort_order => 'zorder(customer, item)');
