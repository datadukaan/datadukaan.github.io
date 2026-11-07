# Day 7 · Rate limits & backoff: code

`supplier_api.py` is a simulated API (the single counter) that runs in-process with a fake clock: 10 requests per minute, HTTP 429 with `Retry-After` when over the limit, and a 24-hour ban (403) after 20 strikes. `data/items.csv` holds the 500 items Raju needs prices for.

| File | Shows | Expected result |
|---|---|---|
| `01_no_limit.py` | The problem: burst + instant retries | banned; only 10 of 500 prices |
| `02_rate_limit.py` | Fix 1: token bucket at 10/min | 50 of 50, no 429s |
| `03_backoff.py` | Fix 2: exponential backoff + jitter on 429/503 | 30 of 30, never banned |
| `04_pagination_checkpoint.py` | Fix 3: 100 per page + checkpoint, crash after page 3 | run 2 resumes at page 4; 500 items in 5 requests |
| `airflow_and_spark_notes.py` | Where these live in Airflow, requests, Spark and ADF | (notes, not run) |

Requirements: Python 3.10+ only (no extra packages). Run every script from this folder.
