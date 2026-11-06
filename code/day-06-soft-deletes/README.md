# Day 6 · Soft deletes & tombstones: code

Sample data: 10 November orders worth ₹50,000. Order **7** (₹2,000) is cancelled.

- `data/orders_night1.csv`: the source before the cancellation.
- `data/orders_night2_hard_delete.csv`: the source after a **hard delete** (row 7 gone).
- `data/orders_night2_soft_delete.csv`: the source after a **soft delete** (`is_deleted = true`, `updated_at` moved).
- `data/cdc_events.csv`: the CDC **tombstone** for order 7 (`op = d`).

| File | Shows | Expected result |
|---|---|---|
| `01_hard_delete.py` | The problem: incremental load can't see a hard delete (PySpark) | 0 rows changed; copy ₹50,000 vs source ₹48,000; ghost order 7 |
| `02_soft_delete.py` | Fix 1: soft delete reaches the copy (PySpark) | 1 row changed; order 7 flagged; plain sum still ₹50,000 |
| `03_tombstone.py` | Fix 2: apply a CDC delete event (DuckDB) | order 7 flagged deleted |
| `04_filtered_view.py` | Fix 3: reports read an active-rows view (DuckDB) | table ₹50,000 (10 rows) vs view ₹48,000 (9 rows) |
| `delete_patterns_delta.sql` | All three + purge for Delta Lake / Databricks | (run on Databricks) |
| `dbt_project/` | Incremental table + filtered view | `./dbt_project/run_demo.sh` |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
