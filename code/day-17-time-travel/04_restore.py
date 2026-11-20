"""Fix 3: restore. Undo the bad job by committing a new version equal to the good one."""
from tiny_delta import Table
from common import total
t = Table("data/stock")
bad = t.latest_version()
print(f"v{bad} (bad_job)      : {total(t.read())} kg")
good = bad - 1
new = t.restore(good, "raju", "2026-11-20 12:05")
print(f"RESTORE TO VERSION {good} -> new v{new}: {total(t.read())} kg")
print("history is kept, the mistake is still visible:")
for h in t.history()[:3]:
    extra = f" (restored v{h['restoredVersion']})" if "restoredVersion" in h else ""
    print(f"   v{h['version']}  {h['user']:8} {h['operation']}{extra}")
