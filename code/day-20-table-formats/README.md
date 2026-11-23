# Day 20 · Delta vs Iceberg vs Hudi: code

Sample data: 100,000 of Raju's bills (`make_data.py`, not committed). Uses `deltalake` (delta-rs) and `pyiceberg` with a local SQLite catalog, so no Spark or cloud account is needed. Hudi has no lightweight Python writer, so it is covered in `platform_notes.sql`.

| File | Shows | Result on our machine |
|---|---|---|
| `make_data.py` | Writes plain Parquet bills | 100,000 bills, 0.9 MB |
| `01_delta_table.py` | Delta = Parquet + `_delta_log/*.json`; one UPDATE | 2 versions, log has add/remove actions |
| `02_iceberg_table.py` | Iceberg = Parquet + metadata JSON + Avro manifests + catalog | 3 snapshots |
| `03_who_can_read.py` | Read each folder with and without its log | without the log: 200,000 rows instead of 100,000 |
| `04_update_churn.py` | 20 rounds of updates to the same 50 bills (copy-on-write) | 2,000,000 rows rewritten to change 1,000 |
| `platform_notes.sql` | Spark SQL for Delta, Iceberg, Hudi MOR, UniForm, XTable | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Run `make_data.py`, then the scripts in order (03 needs 01 and 02).
