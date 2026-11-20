"""Fix 1: every write is a new version with commit info (who, when, what). Like DESCRIBE HISTORY."""
import shutil
from tiny_delta import Table
from common import SNAPSHOTS, stock
shutil.rmtree("data/stock", ignore_errors=True)
t = Table("data/stock")
for ts, o, d, r, op, user in SNAPSHOTS:
    t.commit(stock(o, d, r), op, user, ts)
t.commit(stock(0, 0, 0), "UPDATE", "bad_job", "2026-11-20 11:42")      # the wrong UPDATE
print(f"{'version':>7}  {'timestamp':16}  {'user':8}  operation")
for h in t.history():
    print(f"{h['version']:>7}  {h['timestamp']:16}  {h['user']:8}  {h['operation']}")
