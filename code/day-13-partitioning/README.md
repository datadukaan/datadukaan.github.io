# Day 13 · Partitioning: code

Sample data: Raju's 2026 sales, 100,000 bills from 100 customers, created by `make_data.py` (not committed) in two layouts:
`data/by_customer_day/` (partitioned by customer and day) and `data/by_month/` (partitioned by month).

| File | Shows | Expected result |
|---|---|---|
| `make_data.py` | Writes both layouts (pyarrow, Hive-style folders) | ~34,000 folders vs 12 |
| `01_over_partitioning.py` | The problem: tiny files, slow query (DuckDB) | ~1 KB files, ~2 s query |
| `02_low_cardinality_key.py` | Fix 1: partition by month | same answer in a few ms |
| `03_partition_pruning.py` | Fix 2: pyarrow, DuckDB and Spark read 1 of 12 folders | `Scanning Files: 1/12`, `PartitionFilters` |
| `04_clustering_small_table.py` | Fix 3: small table, no partitions, sorted | 365 tiny files vs 1 file; Oct reads 2 of 10 row groups |
| `platform_notes.sql` | Delta partitioning / CLUSTER BY, Snowflake, BigQuery | (notes, not run) |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run `python make_data.py` first (about a minute: it writes ~34,000 folders), then the scripts in order. Timings vary by machine.
