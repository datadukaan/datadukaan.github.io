# Day 4 · Incremental loads: code

Sample data: two snapshots of a source `orders` table, one order a day for five years.

- `data/source_night1.csv`: the table as of the **Tuesday 3 Nov** nightly load (1,826 rows).
- `data/source_night2.csv`: the table as of **Wednesday 4 Nov** (1,830 rows):
  - 3 new Wednesday orders (1828–1830),
  - Tuesday's bill **1826** fixed on Wednesday (+₹500, `updated_at` = Wed 10:15),
  - order **1827**, stamped Tue 23:40 but committed after Tuesday's load ran.

| File | Shows | Expected result |
|---|---|---|
| `01_full_reload.py` | The problem: read everything every night (PySpark) | 1,830 rows read |
| `02_incremental_load.py` | Fix 1 + 2: high-water mark + incremental load (PySpark) | 4 rows read; order 1827 missed |
| `03_lookback_window.py` | Fix 3: 1-hour lookback + upsert (DuckDB) | 5 rows read; matches the full reload exactly |
| `03_lookback_window_delta.sql` | Same for Delta Lake / Databricks, with a `load_state` table | (run on Databricks) |
| `dbt_project/` | dbt incremental model with lookback | `./dbt_project/run_demo.sh`: same total as a full reload |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
