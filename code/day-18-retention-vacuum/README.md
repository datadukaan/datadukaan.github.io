# Day 18 · Retention, VACUUM, cold tiers: code

`tiny_delta.py` is Day 17's teaching table plus a `vacuum()` that deletes files no version inside the retention window needs. `common.py` builds 60 days of daily overwrites of a 50,000-row sales table.

| File | Shows | Expected result |
|---|---|---|
| `01_storage_bloat.py` | The problem: 1 live file, 60 on disk | 98% of storage is dead versions |
| `02_vacuum.py` | Move 1: VACUUM RETAIN 168 HOURS | 24.8 MB → 3.3 MB; time travel to 1 Oct now fails |
| `03_retention_policy.py` | Move 2: one policy per table, generated SQL | VACUUM RETAIN + row retention per table |
| `04_cold_tiering.py` | Move 3: hot / cool / archive costs for 3 years of data | ~4× cheaper overall, archive tier ~23× cheaper per GB |
| `platform_notes.sql` | Delta VACUUM / retention, Iceberg expire_snapshots, Snowflake, lifecycle rules | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Prices in `04` are approximate AWS list prices; check current pricing.
