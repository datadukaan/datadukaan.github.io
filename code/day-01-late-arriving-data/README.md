# Day 1 · Late-arriving data: code

Sample data: `data/orders.csv`, 12 orders. Orders 1006 and 1007 were placed on Sunday 25 Oct but arrived on Tuesday 27 Oct; order 1012 is three weeks late.

| File | Shows | Expected result |
|---|---|---|
| `01_event_time_vs_arrival_time.py` | Fix 1: event time | Sunday = 2,00,000 by arrival, 2,30,000 by event time |
| `02_watermark_streaming.py` | Fix 2: watermark (PySpark Structured Streaming) | 35-min-late order counted; 36-hour-late orders dropped |
| `03_reprocessing_merge.py` | Fix 3: nightly MERGE + dead-letter (DuckDB) | Only Sunday updated to 2,30,000; order 1012 quarantined |
| `03_reprocessing_merge_delta.sql` | Same MERGE for Delta Lake / Databricks | (run on Databricks) |
| `dbt_project/` | Fix 3 as a dbt incremental model with lookback | `./dbt_project/run_demo.sh` replays Monday and Tuesday nights |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
