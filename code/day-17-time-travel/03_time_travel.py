"""Fix 2: time travel. Read the table as it was, by version or by timestamp."""
from tiny_delta import Table
from common import total
t = Table("data/stock")                    # created by 02_table_history.py
print("today (after bad_job)     :", total(t.read()), "kg")
print("VERSION AS OF 3           :", total(t.read(3)), "kg  (last Friday, priya's update)")
v = t.version_as_of("2026-03-31 23:59")
print(f"TIMESTAMP AS OF 31 March  : {total(t.read(v))} kg  (resolves to version {v})")
for row in t.read(v): print("   ", row)
