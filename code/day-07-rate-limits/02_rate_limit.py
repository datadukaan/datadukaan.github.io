"""Day 7 - Fix 1: a client-side rate limit (token bucket).

Ask at a steady pace: never more than the API allows (10 per minute here).
A token bucket refills at RATE tokens/second; each request spends one token,
and the client waits when the bucket is empty.
"""
from supplier_api import Clock, SupplierAPI, LIMIT, WINDOW

class TokenBucket:
    def __init__(self, clock, rate, capacity):
        self.clock, self.rate, self.capacity = clock, rate, capacity
        self.tokens, self.last = capacity, clock.now
    def acquire(self):
        now = self.clock.now
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens < 1:
            self.clock.sleep((1 - self.tokens) / self.rate)
            self.tokens, self.last = 1, self.clock.now
        self.tokens -= 1

clock = Clock(); api = SupplierAPI(clock)
bucket = TokenBucket(clock, rate=LIMIT / WINDOW, capacity=1)   # capacity 1 = smooth pace, no burst
got, status = {}, {}
for item_id in range(1, 51):                       # first 50 items
    bucket.acquire()
    r = api.get_price(item_id)
    status[r["status"]] = status.get(r["status"], 0) + 1
    if r["status"] == 200: got[item_id] = r["data"]["price"]

print(f"requests sent: {api.requests}")
print(f"responses: {dict(sorted(status.items()))}")
print(f"prices received: {len(got)} of 50 in {clock.now / 60:.1f} minutes")
print(f"=> 500 items one by one would take {500 / LIMIT:.0f} minutes. Fix 3 fixes that.")
