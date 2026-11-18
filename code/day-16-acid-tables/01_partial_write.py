"""The problem on a plain folder of files: a job that crashes halfway leaves half a change,
and two jobs doing read-modify-write lose one update."""
import os, shutil, threading, time
import pyarrow as pa, pyarrow.parquet as pq, pyarrow.dataset as ds

# 1) crash halfway: a batch of 72 Tatkal bookings, written as 6 files of 12
shutil.rmtree("data/plain_bookings", ignore_errors=True); os.makedirs("data/plain_bookings")
try:
    for f in range(6):
        rows = [{"berth": f*12 + i + 1, "passenger": f"P{f*12 + i + 1:02d}"} for i in range(12)]
        pq.write_table(pa.Table.from_pylist(rows), f"data/plain_bookings/part-{f}.parquet")
        if f == 2: raise RuntimeError("job crashed (out of memory)")
except RuntimeError as e:
    print("writer:", e)
print(f"reader sees {ds.dataset('data/plain_bookings').count_rows()} of 72 bookings  <- half a change, no error")

# 2) lost update: two jobs book the last berth at the same moment
open("data/last_berth.txt", "w").write("free")
results, barrier = {}, threading.Barrier(2)
def book(who):
    seen = open("data/last_berth.txt").read()      # both read "free"
    barrier.wait(); time.sleep(0.01)
    if seen == "free":
        open("data/last_berth.txt", "w").write(who)  # both write
        results[who] = "CONFIRMED"
threads = [threading.Thread(target=book, args=(w,)) for w in ("Raju", "stranger")]
[t.start() for t in threads]; [t.join() for t in threads]
print(f"berth 72: {results}  -> file says {open('data/last_berth.txt').read()!r}: one confirmation is a lie")
