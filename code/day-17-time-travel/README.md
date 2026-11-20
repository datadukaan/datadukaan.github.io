# Day 17 · Time travel: code

Story: Raju's stock table is overwritten daily; a GST officer wants the numbers "as on 31st March", and a bad job sets everything to 0.

`tiny_delta.py` extends Day 16's teaching table with commit info (who / when / operation), `history()`, time travel by version or timestamp, and `restore()`. Old data files are never changed, so any version can be rebuilt by replaying the log.

| File | Shows | Expected result |
|---|---|---|
| `01_overwrite_loses_history.py` | The problem: a plain file overwritten daily | 31 March and last Friday unknowable |
| `02_table_history.py` | Fix 1: every write is a version with who/when/what | v0…v5, bad_job's UPDATE visible |
| `03_time_travel.py` | Fix 2: VERSION AS OF 3, TIMESTAMP AS OF 31 March | 515 kg; 615 kg (v1) |
| `04_restore.py` | Fix 3: RESTORE to v4 as a new commit v6 | 0 kg → 680 kg, history kept |
| `platform_notes.sql` | Delta, PySpark, Snowflake (AT/BEFORE, CLONE), Iceberg | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Run in order from this folder (02 creates the table that 03 and 04 use).
