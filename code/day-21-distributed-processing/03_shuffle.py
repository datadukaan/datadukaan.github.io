"""The trap: 'total sales by city' needs a shuffle (an Exchange in the plan).

Every Mumbai row, on every partition, must move to the one task that owns Mumbai.
"""
import time
from pyspark.sql import functions as F
from _spark import spark

s = spark(**{"spark.sql.adaptive.enabled": "false"})
df = s.read.parquet("data/sales")

narrow = df.filter(F.col("amount") > 4000).select("city", "amount")
wide = df.groupBy("city").agg(F.sum("amount").alias("total"))

def has_exchange(d): return "Exchange" in d._jdf.queryExecution().executedPlan().toString()
print("filter + select  -> shuffle?", has_exchange(narrow))
print("groupBy(city)    -> shuffle?", has_exchange(wide))
print("\nPhysical plan for groupBy(city):")
for line in wide._jdf.queryExecution().executedPlan().toString().splitlines():
    print("  " + line[:88])

t = time.time(); narrow.agg(F.count("*")).collect(); tn = time.time() - t
t = time.time(); rows = wide.orderBy(F.desc("total")).collect(); tw = time.time() - t
print(f"\nnarrow job: {tn:.2f} s · wide job (with shuffle): {tw:.2f} s")
print("top city:", rows[0]["city"], f"₹{rows[0]['total']:,}")
s.stop()
