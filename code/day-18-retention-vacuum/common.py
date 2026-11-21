"""60 days of daily overwrites of a 50,000-row sales table: every UPDATE leaves the old file behind."""
import random, shutil
from datetime import datetime, timedelta
from tiny_delta import Table

def build(path="data/sales", days=60, rows=50_000):
    shutil.rmtree(path, ignore_errors=True)
    t = Table(path); rng = random.Random(18)
    start = datetime(2026, 9, 22, 21, 0)
    for d in range(days):
        data = [{"order_id": i, "item": rng.choice(["rice", "dal", "oil"]), "amount": rng.randint(50, 5000)} for i in range(rows)]
        t.commit(data, "WRITE" if d == 0 else "UPDATE", "etl_job", (start + timedelta(days=d)).strftime("%Y-%m-%d %H:%M"))
    return t

NOW = "2026-11-21 12:00"
