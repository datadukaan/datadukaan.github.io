"""Write the same table with each codec; measure size, write time and read time (best of 5)."""
import os, time
import pyarrow.parquet as pq
t = pq.read_table("data/orders_none.parquet")
CODECS = [("none", None), ("snappy", None), ("gzip", None), ("lz4", None), ("zstd", 1), ("zstd", 3), ("zstd", 9)]
base = os.path.getsize("data/orders_none.parquet")
print(f"{'codec':10s} {'size MB':>8s} {'ratio':>6s} {'write s':>8s} {'read ms':>8s}")
for codec, level in CODECS:
    path = f"data/orders_{codec}{level or ''}.parquet"
    t0 = time.perf_counter(); pq.write_table(t, path, compression=codec, compression_level=level); w = time.perf_counter() - t0
    best = 1e9
    for _ in range(5):
        t0 = time.perf_counter(); pq.read_table(path); best = min(best, time.perf_counter() - t0)
    name = codec + (f"-{level}" if level else "")
    print(f"{name:10s} {os.path.getsize(path)/1e6:>8.1f} {base/os.path.getsize(path):>5.1f}x {w:>8.2f} {best*1000:>8.0f}")
