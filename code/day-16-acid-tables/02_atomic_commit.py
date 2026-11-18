"""Fix 1: atomic commit. Data files are invisible until one log entry is written.
A crash before the commit changes nothing."""
import shutil
from tiny_delta import Table
shutil.rmtree("data/bookings", ignore_errors=True)
t = Table("data/bookings")
v = t.commit(-1, add=[])                                   # version 0: empty table
print(f"v{v}: {len(t.read())} bookings")

# the same 72-booking batch, crashing after 3 of 6 files
written = []
try:
    for f in range(6):
        written.append(t.write_file([{"berth": f*12 + i + 1, "passenger": f"P{f*12+i+1:02d}"} for i in range(12)]))
        if f == 2: raise RuntimeError("job crashed")
    t.commit(v, add=written)
except RuntimeError as e:
    print(f"writer: {e} after writing {len(written)} files, before the commit")
print(f"readers see v{t.latest_version()}: {len(t.read())} bookings  <- nothing changed (3 orphan files are ignored)")

# rerun the job: all 6 files, then one commit
files = [t.write_file([{"berth": f*12 + i + 1, "passenger": f"P{f*12+i+1:02d}"} for i in range(12)]) for f in range(6)]
v = t.commit(t.latest_version(), add=files)
print(f"rerun commits v{v}: readers see {len(t.read())} bookings  <- all or nothing")
