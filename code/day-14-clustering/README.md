# Day 14 · Clustering, Z-ordering, data skipping: code

Sample data: Raju's 2026 bills, 600,000 bills from 500 customers (one is "Patel Caterers"), created by `make_data.py` as 12 monthly Parquet files with 10 row groups ("blocks") each, in arrival (date) order. Not committed.

`common.py` counts how many blocks a filter must read, using each block's min/max statistics: the same check Delta, Iceberg, Snowflake and BigQuery do on files / micro-partitions.

| File | Shows | Expected result |
|---|---|---|
| `01_full_table_scan.py` | The problem: filter by customer on a date-split table | 120 of 120 blocks |
| `02_data_skipping.py` | Fix 1: min/max skips on date, not on customer | date 2 of 120; customer 120 of 120 |
| `03_clustering.py` | Fix 2: sort by customer inside each file | 12 of 120; but item still 120 of 120 |
| `04_z_ordering.py` | Fix 3: Z-order on (customer, item) vs a linear sort | customer 10 and item 23 of 120 |
| `platform_notes.sql` | Delta ZORDER / liquid clustering, Snowflake, BigQuery, Iceberg | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Run `python make_data.py` first, then the scripts in order.
