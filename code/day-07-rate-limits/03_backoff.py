"""Day 7 - Fix 2: exponential backoff with jitter.

When the API says "wait" (429) or has a hiccup (503), don't ask again at once.
Wait 1 s, then 2, then 4, 8... (capped), plus a little randomness ("jitter")
so many clients don't all retry at the same instant. Honour Retry-After
when the API sends it. Give up after a few tries and alert a human.
"""
import random
from supplier_api import Clock, SupplierAPI

random.seed(42)

def call_with_backoff(fn, clock, max_tries=6, base=1.0, cap=60.0, log=None):
    for attempt in range(max_tries):
        r = fn()
        if r["status"] == 200:
            return r
        if r["status"] not in (429, 503):          # 4xx like 400/403 won't fix themselves
            raise RuntimeError(f"giving up: HTTP {r['status']}")
        wait = min(cap, base * 2 ** attempt)
        wait = max(wait, r.get("retry_after", 0)) if r["status"] == 429 else wait
        wait = wait * random.uniform(0.8, 1.2)     # jitter
        if log is not None: log.append((r["status"], round(wait, 1)))
        clock.sleep(wait)
    raise RuntimeError("giving up after retries")

clock = Clock(); api = SupplierAPI(clock, fail_every=4)   # every 4th call: 503
got, waits = {}, []
for item_id in range(1, 31):
    r = call_with_backoff(lambda: api.get_price(item_id), clock, log=waits)
    got[item_id] = r["data"]["price"]

print(f"prices received: {len(got)} of 30, requests sent: {api.requests}, banned: {api.banned_until is not None}")
print("first waits (status, seconds):", waits[:6])
print(f"total time: {clock.now / 60:.1f} minutes")
