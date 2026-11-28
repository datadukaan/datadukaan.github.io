# Day 21 · Distributed processing (Spark): code

Sample data: 4,000,000 Diwali orders in 8 Parquet files (`make_data.py`, not committed), a small stand-in for "1 TB". Runs on local Spark: `local[n]` = n worker threads, the same driver/executor/task model as a cluster.

| File | Shows | Result on our machine (2 cores) |
|---|---|---|
| `make_data.py` | Writes the sales files | 4,000,000 orders, 27.9 MB |
| `01_partitions.py` | Piece size → number of partitions/tasks | 128 MB → 2, 4 MB → 8, 1 MB → 32 tasks |
| `02_one_vs_many.py` | Same job on 1 core vs all cores | 1.97 s → 1.33 s (1.5×) |
| `03_shuffle.py` | Which queries shuffle (Exchange in the plan) | filter: no · groupBy(city): yes |
| `04_retry.py` | A task fails once and is re-run alone | correct total, partition 3 on attempt 2 |
| `platform_notes.sql` | Cluster sizing, shuffle partitions, AQE, retries | (notes, not run) |

Requirements: Python 3.10+, Java 17+, `pip install -r ../../requirements.txt`. Run `make_data.py` first.
