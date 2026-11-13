"""The problem: SUM(tax) from a CSV has to read and parse every column of every row."""
import os
import pyarrow.csv as pv

table = pv.read_csv("data/bills.csv")            # a CSV can't be read one column at a time
total = table.column("tax").to_pylist()
print(f"columns parsed : {table.num_columns} of {table.num_columns}  (needed: 1)")
print(f"bytes read     : {os.path.getsize('data/bills.csv')/1e6:.1f} MB (the whole file)")
print(f"total tax      : Rs {sum(total):,.0f}")
