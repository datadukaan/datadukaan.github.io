# Day 12 · Compaction: code

Sample data: 2,000 small appends of 250 bills each, created by `make_data.py` as 2,000 tiny Parquet files in `data/sales_small/` (not committed).

| File | Shows | Expected result |
|---|---|---|
| `make_data.py` | Creates the tiny files | 2,000 files, avg ~4 KB |
| `01_small_files_problem.py` | The problem: one query opens 2,000 files (DuckDB) | ~150 ms for 8 MB of data |
| `02_compaction.py` | Fix 1: rewrite into a few big files (what `OPTIMIZE` does) | 2,000 files → 3, query ~50× faster |
| `03_optimized_writes.py` | Fix 2: `repartition("month")` before `partitionBy` (PySpark) | 550 files → 11 |
| `04_auto_compaction.py` | Fix 3: merge small files after every write once there are 50 | 40 files instead of 2,000 |
| `platform_notes.sql` | Delta OPTIMIZE / autoOptimize, Iceberg, Snowflake | (notes, not run) |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run `python make_data.py` first, then the scripts in order, from this folder. Timings vary by machine.
