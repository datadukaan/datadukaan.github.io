"""Shared helper: drop N tiny order files (one order slip each) into a folder."""
import json, os, shutil, time

def drop_slips(folder, n, start=0, delay=0.0):
    os.makedirs(folder, exist_ok=True)
    for i in range(start, start + n):
        tmp = os.path.join(folder, f".order_{i:05d}.json.tmp")
        with open(tmp, "w") as f:
            json.dump({"order_id": i, "item": "samosa", "qty": 2, "amount": 40}, f)
        os.replace(tmp, os.path.join(folder, f"order_{i:05d}.json"))  # atomic (Day 8)
        if delay:
            time.sleep(delay)

def fresh(folder):
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)
