"""The problem: the table is 1 file of live data, but 60 files sit on disk and you pay for all of them."""
import os
from common import build
from tiny_delta import size_mb
t = build()
live = t.files()
on_disk = [f for f in os.listdir(t.path) if f.endswith(".parquet")]
live_mb = sum(os.path.getsize(os.path.join(t.path, f)) for f in live) / 1e6
print(f"versions          : {t.latest_version() + 1}")
print(f"live files        : {len(live)}  ({live_mb:.1f} MB)")
print(f"files on disk     : {len(on_disk)}  ({size_mb(t):.1f} MB)  <- you pay for this")
print(f"wasted            : {100*(1 - live_mb/size_mb(t)):.0f}% of storage holds data no query reads")
