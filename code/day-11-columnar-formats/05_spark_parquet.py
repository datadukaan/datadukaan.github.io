"""The same fixes in PySpark: column pruning + pushed filters, visible in the plan."""
import re
from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.master("local[2]").appName("day11").config("spark.ui.enabled", "false").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.parquet("data/bills.parquet")
q = df.where(F.col("bill_date") >= "2026-01-01").select(F.sum("tax").alias("tax_2026"))
plan = q._jdf.queryExecution().executedPlan().toString()
for line in plan.splitlines():
    if "FileScan" in line:
        print(re.search(r"PushedFilters: \[[^\]]*\]", line).group(0))
        print(re.search(r"ReadSchema: \S+", line).group(0))
print(f"tax 2026: Rs {q.collect()[0]['tax_2026']:,.0f}")
spark.stop()
