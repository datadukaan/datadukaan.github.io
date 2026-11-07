"""A tiny simulated supplier API - the clerk at the single counter.

Runs in-process with a fake clock, so every demo is fast and gives the same
result every time. It behaves like many real APIs:

* Rate limit: at most LIMIT requests per WINDOW seconds (sliding window).
* Over the limit -> HTTP 429 Too Many Requests, with a Retry-After hint.
* Keep hammering while limited (more than BAN_AFTER 429s) -> 403, banned until
  "tomorrow" (the shutter comes down).
* /prices?page=N&size=S returns one page of items plus next_page.
"""
import csv, os
from collections import deque

LIMIT, WINDOW, BAN_AFTER, BAN_SECONDS = 10, 60.0, 20, 24 * 3600
HERE = os.path.dirname(os.path.abspath(__file__))


class Clock:
    def __init__(self): self.now = 0.0
    def sleep(self, s): self.now += s


class SupplierAPI:
    def __init__(self, clock, fail_every=None):
        self.clock = clock
        self.calls = deque()
        self.strikes = 0
        self.banned_until = None
        self.requests = 0
        self.fail_every = fail_every          # simulate a flaky 503 every N calls
        with open(os.path.join(HERE, "data", "items.csv")) as f:
            self.items = [dict(item_id=int(r["item_id"]), item=r["item"], price=int(r["price"])) for r in csv.DictReader(f)]

    def _gate(self):
        """Returns (status, retry_after) or None if the call may proceed."""
        self.requests += 1
        now = self.clock.now
        if self.banned_until is not None and now < self.banned_until:
            return 403, self.banned_until - now
        while self.calls and now - self.calls[0] >= WINDOW:
            self.calls.popleft()
        if len(self.calls) >= LIMIT:
            self.strikes += 1
            if self.strikes > BAN_AFTER:
                self.banned_until = now + BAN_SECONDS
                return 403, BAN_SECONDS
            return 429, WINDOW - (now - self.calls[0])
        self.calls.append(now)
        if self.fail_every and self.requests % self.fail_every == 0:
            return 503, 1.0
        return None

    def get_price(self, item_id):
        g = self._gate()
        if g: return {"status": g[0], "retry_after": round(g[1], 1)}
        return {"status": 200, "data": self.items[item_id - 1]}

    def get_page(self, page, size=100):
        g = self._gate()
        if g: return {"status": g[0], "retry_after": round(g[1], 1)}
        start = (page - 1) * size
        rows = self.items[start:start + size]
        nxt = page + 1 if start + size < len(self.items) else None
        return {"status": 200, "data": rows, "next_page": nxt}
