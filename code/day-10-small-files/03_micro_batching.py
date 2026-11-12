"""Fix 2: collect files for a short window, then process them together as one job."""
import glob, json, os, threading, time
from common import drop_slips, fresh

LANDING = "landing"
fresh(LANDING)
# slips keep arriving during the match, ~2,000 over a couple of seconds
threading.Thread(target=drop_slips, args=(LANDING, 2000), kwargs={"delay": 0.001}).start()

JOB_STARTUP = 0.002
BATCH_WINDOW = 0.5                         # Raju's 5 minutes, scaled down

done, batches = set(), 0
t0 = time.time()
while len(done) < 2000:
    time.sleep(BATCH_WINDOW)               # let slips pile up in the tray
    new = [p for p in sorted(glob.glob(f"{LANDING}/order_*.json")) if p not in done]
    if not new:
        continue
    time.sleep(JOB_STARTUP); batches += 1  # one trip for the whole tray
    total = sum(json.load(open(p))["amount"] for p in new)
    done.update(new)
    print(f"  batch {batches}: {len(new):4d} files, Rs {total:,}")
print(f"files processed : {len(done)}")
print(f"jobs started    : {batches}   (was 2000)")
print(f"time            : {time.time() - t0:.2f}s")

# Bonus: compact the tiny files into one so readers open 1 file, not 2,000
os.makedirs("compacted", exist_ok=True)
with open("compacted/orders.jsonl", "w") as out:
    for p in sorted(done):
        out.write(open(p).read() + "\n")
print("compacted into  : compacted/orders.jsonl (1 file)")
