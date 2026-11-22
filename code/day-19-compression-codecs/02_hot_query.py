"""Hot data: the sale-day dashboard query, run 20 times on each file (DuckDB)."""
import time, duckdb
Q = "SELECT item, sum(amount) FROM read_parquet('{p}') WHERE bill_date = DATE '2026-11-01' GROUP BY item"
for name in ["none", "snappy", "zstd3", "gzip"]:
    p = f"data/orders_{name}.parquet"; con = duckdb.connect(); con.sql(Q.format(p=p)).fetchall()   # warm up
    t0 = time.perf_counter()
    for _ in range(20): con.sql(Q.format(p=p)).fetchall()
    print(f"{name:7s}: {(time.perf_counter() - t0)/20*1000:6.1f} ms per dashboard query")
