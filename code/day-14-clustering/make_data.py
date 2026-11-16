"""Raju's 2026 bills: 600,000 bills from 500 customers, one file per month (Day 13), rows in arrival order."""
import os, shutil, random, datetime as dt
import pyarrow as pa, pyarrow.parquet as pq
random.seed(14)
CUSTOMERS = [f"Cust {i:03d}" for i in range(1, 500)] + ["Patel Caterers"]
ITEMS = ["biscuit", "dal", "ghee", "oil", "rice", "salt", "soap", "sugar", "tea", "wheat"]
shutil.rmtree("data/arrival", ignore_errors=True); os.makedirs("data/arrival")
for m in range(1, 13):
    rows = []
    for _ in range(50_000):
        d = dt.date(2026, m, random.randint(1, 28))
        rows.append({"bill_date": d, "customer": random.choice(CUSTOMERS), "item": random.choice(ITEMS),
                     "amount": random.randint(50, 5000)})
    rows.sort(key=lambda r: r["bill_date"])                 # bills arrive in date order
    pq.write_table(pa.Table.from_pylist(rows), f"data/arrival/2026-{m:02d}.parquet", row_group_size=5_000)
print("12 monthly files x 50,000 bills, 10 row groups each")
