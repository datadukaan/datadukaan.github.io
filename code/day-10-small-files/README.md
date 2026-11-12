# Day 10 · The small files problem: code

Sample data: 2,000 tiny order slips (`order_00000.json` …), ~57 bytes each, created by `common.py`.

| File | Shows | Expected result |
|---|---|---|
| `01_small_files_problem.py` | The problem: one job per file, polling the folder | 2,000 jobs, 5 folder LISTs |
| `02_file_notification.py` | Fix 1: storage publishes "file landed" events to a queue | 10 files received, 0 LIST calls |
| `03_micro_batching.py` | Fix 2: collect for a window, one job per batch, then compact | a handful of jobs instead of 2,000 |
| `04_batch_trigger.py` | Fix 3: Spark `maxFilesPerTrigger=50` (PySpark) | 230 files → 5 batches, max 50 each |
| `platform_notes.sql` | Auto Loader notifications, Delta OPTIMIZE, Snowpipe, ADF event triggers | (notes, not run) |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
