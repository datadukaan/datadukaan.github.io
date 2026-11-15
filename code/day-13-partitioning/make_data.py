"""Raju's 2026 sales: 100,000 bills from 100 customers, saved two ways."""
import os, shutil, random, datetime as dt
import pyarrow as pa, pyarrow.dataset as ds
random.seed(13)
ITEMS = ["sugar", "rice", "dal", "oil", "tea", "soap"]
rows = []
for i in range(100_000):
    d = dt.date(2026, 1, 1) + dt.timedelta(days=random.randrange(365))
    rows.append({"bill_date": d, "month": d.strftime("%Y-%m"), "customer": f"C{random.randint(1, 100):03d}",
                 "item": random.choice(ITEMS), "qty_kg": random.randint(1, 20)})
table = pa.Table.from_pylist(rows)

def write(path, cols):
    shutil.rmtree(path, ignore_errors=True)
    ds.write_dataset(table, path, format="parquet", partitioning=cols, partitioning_flavor="hive",
                     max_partitions=100_000, max_open_files=2_000)

write("data/by_customer_day", ["customer", "bill_date"])   # one drawer per customer per day
write("data/by_month", ["month"])                          # one drawer per month
print(f"{table.num_rows:,} bills written")
