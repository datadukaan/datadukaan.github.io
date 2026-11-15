"""The problem: partition by customer AND day -> tens of thousands of tiny folders."""
from common import layout, sugar_last_month
folders, files, size = layout("data/by_customer_day")
kg, sec = sugar_last_month("data/by_customer_day")
print(f"folders        : {folders:,}")
print(f"avg file size  : {size/files/1e3:.1f} KB  ({100_000/files:.1f} bills per file)")
print(f"sugar in Oct   : {kg:,} kg")
print(f"query time     : {sec*1000:.0f} ms")
