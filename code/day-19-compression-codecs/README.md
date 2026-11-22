# Day 19 · Snappy vs ZSTD: code

Sample data: 2,000,000 Diwali orders (`make_data.py`, not committed). Benchmarks use pyarrow and DuckDB; timings vary by machine, sizes don't.

| File | Shows | Result on our machine |
|---|---|---|
| `make_data.py` | Writes the uncompressed file | 21.7 MB |
| `01_codec_benchmark.py` | Size, write and read time per codec | snappy 13.6 MB, zstd 7.5 MB, gzip 17.5 s to write |
| `02_hot_query.py` | Dashboard query on each file (DuckDB) | all within ~1 ms of each other |
| `03_cold_storage_cost.py` | 3 years at 1,000 files/day | zstd ~45% cheaper than snappy |
| `platform_notes.sql` | Spark, Delta, Iceberg, DuckDB settings | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Run `make_data.py` first.
