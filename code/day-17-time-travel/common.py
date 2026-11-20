"""Raju's stock table through the year, as a series of daily overwrites."""
def stock(onion, dal, rice):
    return [{"item": "onion", "qty_kg": onion}, {"item": "dal", "qty_kg": dal}, {"item": "rice", "qty_kg": rice}]

SNAPSHOTS = [   # (timestamp, onion, dal, rice, operation, user)
    ("2026-03-30 21:00", 300, 120, 200, "WRITE",  "etl_job"),
    ("2026-03-31 21:00", 310, 115, 190, "WRITE",  "etl_job"),   # <- the GST officer's date
    ("2026-04-30 21:00", 355, 140, 210, "WRITE",  "etl_job"),
    ("2026-11-13 18:30", 420,  45,  50, "UPDATE", "priya"),     # last Friday
    ("2026-11-20 09:00", 540,  60,  80, "WRITE",  "etl_job"),
]
def total(rows): return sum(r["qty_kg"] for r in rows)
