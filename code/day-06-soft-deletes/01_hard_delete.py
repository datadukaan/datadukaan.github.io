"""Day 6 - The problem: a hard delete leaves a ghost in the copy.

Night 1: the warehouse copy loads all 10 November orders (Rs 50,000).
Then order 7 (Rs 2,000) is cancelled and DELETED from the source table.
Night 2: the incremental load (Day 4) asks "what has updated_at > mark?".
A deleted row has no updated_at - it isn't there - so nothing arrives,
and the copy keeps the cancelled order forever.
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day06-hard").config("spark.sql.session.timeZone", "UTC").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
read = lambda f: spark.read.csv(f"data/{f}", header=True, inferSchema=True)

copy = read("orders_night1.csv")
mark = copy.agg(F.date_format(F.max("updated_at"), "yyyy-MM-dd HH:mm:ss")).first()[0]

source = read("orders_night2_hard_delete.csv")
new = source.filter(F.col("updated_at") > F.to_timestamp(F.lit(mark)))
print("Night 2: rows changed since the mark =", new.count())

print("Source total (truth):"); source.agg(F.sum("amount").alias("total")).show()
print("Copy total (report):");  copy.agg(F.sum("amount").alias("total")).show()
print("Ghost rows in the copy:"); copy.join(source, "order_id", "left_anti").show()
spark.stop()
