# Day 15 · Medallion architecture: code

Sample data: two days of supplier slips in `landing/` with the usual mess: a duplicate slip, onions in grams, a quantity of `x?`.
Runs on DuckDB (a local stand-in for Delta tables; `platform_notes.sql` has the Databricks version). Creates `medallion.duckdb` (not committed).

| File | Shows | Expected result |
|---|---|---|
| `01_data_swamp.py` | The problem: raw files loaded straight into a dashboard table, overwritten each day | 75,000 "kg" of onions; yesterday's raw rows gone |
| `02_bronze.py` | Bronze: append-only, all text, `_load_time` + `_source_file` | 8 rows, mess kept on purpose |
| `03_silver.py` | Silver: dedupe, cast, convert g → kg, quarantine bad rows | 6 clean rows + 1 quarantined |
| `04_gold.py` | Gold: `stock_by_item` for dashboards | onion 50 kg |
| `05_replay_from_bronze.py` | A silver bug fixed by rebuilding from bronze | 50,000 kg → 50 kg |
| `platform_notes.sql` | Auto Loader → bronze, MERGE → silver, gold, DLT expectations | (notes, not run) |

Requirements: Python 3.10+, `pip install -r ../../requirements.txt`. Run the scripts in order from this folder.
