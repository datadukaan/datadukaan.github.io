# Day 16 · ACID table formats: code

Story: Tatkal booking. A batch of 72 bookings and the last berth (72) that two people try to book at once.

`tiny_delta.py` is a ~60-line, Delta-style table: Parquet data files plus a `_delta_log/` of numbered JSON commits. A version exists only once its log file is created with put-if-absent (`O_EXCL`), which is the core idea behind Delta Lake's commits. It's a teaching model, not a replacement for Delta or Iceberg (the Delta jars can't be downloaded in this sandbox).

| File | Shows | Expected result |
|---|---|---|
| `01_partial_write.py` | The problem on plain files: crash halfway; two jobs book one berth | 36 of 72 visible; both "CONFIRMED", file corrupted |
| `02_atomic_commit.py` | Fix 1: files invisible until one log entry; crash = no change | 0 → 0 (crash) → 72 |
| `03_optimistic_concurrency.py` | Fix 2: second writer hits a conflict, re-reads, gets waiting list | Raju confirmed, stranger WL |
| `04_snapshot_isolation.py` | Fix 3: reader pinned to v7 while v8 is written | 16, 16, 16 → 22 |
| `05_duckdb_transactions.py` | A real engine: ROLLBACK on failure, write-write conflict | balance unchanged; "Conflict on update!" |
| `platform_notes.sql` | Delta history / isolation levels, Iceberg, S3 caveat, Snowflake | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Run from this folder. Script 01's lost update is a real race, so its exact output can vary.
