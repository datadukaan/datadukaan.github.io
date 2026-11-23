"""Raju's bills: 100,000 rows written as plain Parquet (the 'data' all three formats share)."""
import os, random, datetime as dt
import pyarrow as pa, pyarrow.parquet as pq
random.seed(20); N = 100_000
PARTIES = ["CA Sharma", "Gupta Suppliers", "Walk-in", "Hotel Annapurna", "Sweet Corner"]
t = pa.table({
    "bill_id": pa.array(range(1, N + 1), pa.int64()),
    "bill_date": pa.array([dt.date(2026, 11, 1) + dt.timedelta(days=i * 30 // N) for i in range(N)]),
    "party": pa.array([random.choice(PARTIES) for _ in range(N)]),
    "amount": pa.array([random.randint(100, 20_000) for _ in range(N)], pa.int64()),
    "status": pa.array(["unpaid"] * N),
})
os.makedirs("data", exist_ok=True)
pq.write_table(t, "data/bills.parquet")
print(f"{N:,} bills -> data/bills.parquet ({os.path.getsize('data/bills.parquet')/1e6:.1f} MB)")
