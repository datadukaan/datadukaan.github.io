# Day 8 · Partial reads: code

Sample data: `data/diwali_boxes.csv`, 200 Diwali sweet boxes at ₹500 each (₹1,00,000).
The scripts write into `out/` (ignored by git).

| File | Shows | Expected result |
|---|---|---|
| `01_partial_read.py` | The problem: a reader thread reads while a writer thread is still writing | about 80 of 200 boxes, no error |
| `02_atomic_rename.py` | Fix 1: write to `_tmp/…part`, then `os.replace` | the reader only ever sees 0 or 200 |
| `03_success_marker.py` | Fix 2: Spark's `_SUCCESS` file + a wait-for-marker check (PySpark) | part files + `_SUCCESS`; 200 boxes read |
| `04_manifest_check.py` | Fix 3: row count + SHA-256 manifest | complete delivery LOADs; truncated delivery REJECTs |
| `platform_notes.sql` | Delta/Iceberg commits, Snowflake COPY, Airflow FileSensor | (notes, not run) |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder. Timing in `01` depends on your machine, so the count varies a little.
