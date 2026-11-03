# Day 3 · Out-of-order data: code

Sample data: `data/order_messages.csv`, 5 messages for 3 orders on Tuesday 3 Nov.

- **Order 101:** placed 9:00 for ₹500, changed 9:02 to ₹800. The change **arrived first**.
- **Order 102:** placed 10:00 for ₹300, changed to ₹450. That phone's clock was slow, so the change is stamped **9:58**.
- **Order 103:** one message, ₹1,000.

The correct current total is **₹2,250** (800 + 450 + 1,000).

| File | Shows | Expected result |
|---|---|---|
| `01_event_time.py` | Fix 1: latest by event time vs arrival (PySpark) | Arrival: 101 = 500 (1,950). Event time: 101 = 800, but 102 = 300 (2,100) |
| `02_sequence_number.py` | Fix 2: highest seq wins (PySpark) | 101 = 800, 102 = 450, total 2,250 |
| `03_latest_version_wins.py` | Fix 3: plain vs guarded upsert, applied in arrival order (DuckDB) | Plain 1,950; guarded 2,250 |
| `03_latest_version_wins_delta.sql` | Same guarded MERGE for Delta Lake / Databricks | (run on Databricks) |
| `dbt_project/` | Fix 3 as a dbt incremental model across two runs | `./dbt_project/run_demo.sh`: 101 stays 800 after the late seq 1 |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
