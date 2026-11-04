# Day 5 · Change Data Capture: code

Sample data: a small menu table on Thursday 5 Nov.

- `data/menu_snapshot_midnight.csv`: last night's full copy (Tea 15, Thali 120, Dosa 60, Vada 25).
- `data/change_log.csv`: 4 CDC events from the source's log: Thali 120 → 150 (update), Lassi added (insert), Vada removed (delete), Tea 15 → 18 (update).
- `data/menu_source_noon.csv`: the source table at noon, for checking.

| File | Shows | Expected result |
|---|---|---|
| `01_nightly_full_copy.py` | The problem: a stale nightly copy (PySpark) | 4 rows disagree; ₹1,200 lost on thalis |
| `02_apply_change_log.py` | Fix 1 + 2: apply the change log, including the delete (PySpark) | copy == source: True |
| `03_checkpoint.py` | Fix 3: crash after event 102, restart 3 ways (DuckDB) | checkpoint ✓, latest ✗ (Vada lives on), beginning ✓ (idempotent) |
| `03_apply_changes_delta.sql` | The same MERGE for Delta Lake / Databricks, with a checkpoint table | (run on Databricks) |
| `dbt_project/` | Rebuild the copy from snapshot + log in dbt | `./dbt_project/run_demo.sh`: replays up to lsn 101, then 104 |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
