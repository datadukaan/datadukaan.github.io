"""The problem: 2,000 tiny files, one job per file, plus polling a folder over and over."""
import json, os, time
from common import drop_slips, fresh

LANDING = "landing"
fresh(LANDING)
drop_slips(LANDING, 2000)

JOB_STARTUP = 0.002   # pretend cost to start one job (real Spark jobs: seconds)

seen, jobs, list_calls = set(), 0, 0
t0 = time.time()
for poll in range(5):                      # the son checks the printer again and again
    files = os.listdir(LANDING); list_calls += 1
    for name in sorted(files):
        if name in seen:
            continue
        time.sleep(JOB_STARTUP); jobs += 1  # one trip per slip
        with open(os.path.join(LANDING, name)) as f:
            json.load(f)
        seen.add(name)

print(f"files         : {len(seen)}  (avg {os.path.getsize(os.path.join(LANDING, 'order_00000.json'))} bytes each)")
print(f"jobs started  : {jobs}   <- one per file")
print(f"folder LISTs  : {list_calls}  (each lists all {len(files)} files, even when nothing is new)")
print(f"time          : {time.time() - t0:.1f}s, mostly job start-up, not real work")
