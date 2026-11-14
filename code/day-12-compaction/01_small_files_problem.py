"""The problem: the same data in 2,000 tiny files - every query opens every file."""
from common import files, rice_query
n, size = files("data/sales_small")
kg, sec = rice_query("data/sales_small")
print(f"files          : {n:,}  (avg {size/n/1e3:.1f} KB)")
print(f"rice this year : {kg:,} kg")
print(f"query time     : {sec*1000:.0f} ms")
