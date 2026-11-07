"""Day 7 - Fix 3: pagination with a checkpoint.

Ask for one page (100 items) per request instead of one item per request,
and save the last page you finished. If the job dies, the next run starts
after that page - not from item one.
"""
import json, os
from supplier_api import Clock, SupplierAPI

CKPT = "checkpoint.json"

def load():  return json.load(open(CKPT))["last_page"] if os.path.exists(CKPT) else 0
def save(p): json.dump({"last_page": p}, open(CKPT, "w"))

def run(api, crash_after=None):
    page, rows = load() + 1, []
    print(f"  starting at page {page}")
    while page:
        r = api.get_page(page, size=100)
        assert r["status"] == 200, r
        rows += r["data"]                          # in real life: write this page to storage first
        save(page)                                 # ...then move the checkpoint
        print(f"  page {page}: {len(r['data'])} items  -> checkpoint = {page}")
        if crash_after == page:
            print("  *** shutter comes down (job crashes) ***")
            return rows
        page = r["next_page"]
    return rows

if os.path.exists(CKPT): os.remove(CKPT)
clock = Clock(); api = SupplierAPI(clock)
print("Run 1:"); first = run(api, crash_after=3)
print("Run 2 (next day):"); second = run(api)
print(f"items fetched: {len(first) + len(second)} of 500 with {api.requests} requests (one-by-one would be 500)")
os.remove(CKPT)
