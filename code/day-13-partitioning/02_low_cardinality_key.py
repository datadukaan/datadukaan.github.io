"""Fix 1: partition by a column with few values (month: 12) instead of customer x day."""
from common import layout, sugar_last_month
for label, path in [("customer + day", "data/by_customer_day"), ("month", "data/by_month")]:
    folders, files, size = layout(path); kg, sec = sugar_last_month(path)
    print(f"{label:15s}: {folders:>6,} folders, avg file {size/files/1e3:>7.1f} KB -> sugar {kg:,} kg in {sec*1000:>5.0f} ms")
