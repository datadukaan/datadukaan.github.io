"""Raju's Diwali sales: 4,000,000 rows as Parquet (a small stand-in for '1 TB')."""
import os, random
import pyarrow as pa, pyarrow.parquet as pq
random.seed(21); N = 4_000_000
CITIES = ["Mumbai"] * 4 + ["Delhi", "Bengaluru", "Pune", "Chennai", "Kolkata", "Hyderabad"]
os.makedirs("data/sales", exist_ok=True)
for f in range(8):                                   # 8 files, like a folder of daily dumps
    n = N // 8
    t = pa.table({
        "order_id": pa.array(range(f * n, (f + 1) * n), pa.int64()),
        "city": pa.array([random.choice(CITIES) for _ in range(n)]),
        "item": pa.array([random.choice(["kaju katli", "laddoo", "diya", "rangoli", "barfi"]) for _ in range(n)]),
        "amount": pa.array([random.randint(50, 5000) for _ in range(n)], pa.int64()),
    })
    pq.write_table(t, f"data/sales/part-{f}.parquet")
size = sum(os.path.getsize(f"data/sales/{p}") for p in os.listdir("data/sales"))
print(f"{N:,} orders in 8 files -> data/sales/ ({size/1e6:.1f} MB)")
