"""Day 9 - Fix 1: read the heading, not the position.

Select columns by NAME. New columns anywhere in the file don't matter,
and a missing column fails loudly instead of returning wrong numbers.
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day09-name").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

for month in ("october", "november"):
    df = spark.read.csv(f"data/bill_{month}.csv", header=True, inferSchema=True)
    total = df.select("item", "price").agg(F.sum("price")).first()[0]
    print(f"{month:<9} total Rs {total:,}")

try:
    spark.read.csv("data/bill_december_breaking.csv", header=True).select("price").collect()
except Exception as e:
    print("december (price renamed to amount): fails loudly ->", type(e).__name__)
spark.stop()
