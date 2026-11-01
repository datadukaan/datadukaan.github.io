# Day 2 · Duplicate data: code

Sample data: `data/orders_received.csv`, 12 messages for 10 real orders placed on Sunday 1 Nov. The rider's phone retried orders **101** (₹500) and **105** (₹29,500), so they arrived twice. Order **111** is a real second ₹500 order from the same customer as 101.

| File | Shows | Expected result |
|---|---|---|
| `01_unique_id.py` | Fix 1: why you need an order ID (PySpark) | Naive total 2,60,000; guessing by customer + amount wrongly gives 2,29,500 |
| `02_deduplication.py` | Fix 2: keep one row per order_id (PySpark) | 10 orders, 2,30,000 |
| `03_idempotent_write.py` | Fix 3: INSERT vs upsert, run 3 times (DuckDB) | INSERT keeps growing; upsert stays 2,30,000 |
| `03_idempotent_write_delta.sql` | Same MERGE for Delta Lake / Databricks | (run on Databricks) |
| `dbt_project/` | Fix 2 + 3 as a dbt incremental model with `unique_key` | `./dbt_project/run_demo.sh`: 2,30,000 after every run |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
