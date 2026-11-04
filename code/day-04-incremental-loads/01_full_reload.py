"""Day 4 - The problem: a full reload.

Every night the job reads the WHOLE source table - five years of orders - and
overwrites the target, just to pick up one new day. Correct, but the work grows
every day the business exists.
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day04-full").config("spark.sql.session.timeZone", "UTC").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

src = spark.read.csv("data/source_night2.csv", header=True, inferSchema=True)
target = src  # overwrite everything
target.write.mode("overwrite").parquet("/tmp/day04_full_target")

print("Wednesday night, full reload")
print("rows read from source:", src.count())
spark.read.parquet("/tmp/day04_full_target").agg(
    F.count("*").alias("orders"), F.sum("amount").alias("total")).show()
spark.stop()
