"""Diwali sales: 2,000,000 orders, written as an uncompressed Parquet file."""
import os, random, datetime as dt
import pyarrow as pa, pyarrow.parquet as pq
random.seed(19); N = 2_000_000
ITEMS = ["kaju katli", "laddoo", "soan papdi", "barfi", "diya", "rangoli", "rice", "dal"]
t = pa.table({
    "order_id": pa.array(range(N)),
    "bill_date": pa.array([dt.date(2026, 10, 1) + dt.timedelta(days=i * 45 // N) for i in range(N)]),
    "item": pa.array([random.choice(ITEMS) for _ in range(N)]),
    "qty": pa.array([random.randint(1, 10) for _ in range(N)]),
    "amount": pa.array([random.randint(50, 5000) for _ in range(N)]),
})
os.makedirs("data", exist_ok=True)
pq.write_table(t, "data/orders_none.parquet", compression="none")
print(f"{N:,} orders -> data/orders_none.parquet ({os.path.getsize('data/orders_none.parquet')/1e6:.1f} MB)")
