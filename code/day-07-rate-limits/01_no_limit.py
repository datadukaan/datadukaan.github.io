"""Day 7 - The problem: asking too fast, and asking again immediately.

The son reads out all 500 items at once. Every refusal (429) is retried
straight away. The supplier counts the strikes and bans the client.
"""
from supplier_api import Clock, SupplierAPI

clock = Clock(); api = SupplierAPI(clock)
got, status = {}, {}
for item_id in range(1, 501):
    for attempt in range(3):                       # "read it all again, louder"
        r = api.get_price(item_id)
        status[r["status"]] = status.get(r["status"], 0) + 1
        if r["status"] == 200:
            got[item_id] = r["data"]["price"]; break
        clock.sleep(0.01)                          # no waiting at all
    clock.sleep(0.05)

print(f"requests sent: {api.requests}")
print(f"responses: {dict(sorted(status.items()))}   (429 = too many, 403 = banned)")
print(f"prices received: {len(got)} of 500")
print(f"banned until: +{(api.banned_until - clock.now) / 3600:.1f} hours" if api.banned_until else "not banned")
