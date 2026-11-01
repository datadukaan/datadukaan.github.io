"""Day 2 - Fix 2: deduplication - keep one row per order_id.

Batch: keep the FIRST message received for each order_id with a window function
(deterministic, unlike a bare dropDuplicates which may keep any copy).
Streaming: dropDuplicatesWithinWatermark remembers recent IDs only for as long as
retries can realistically arrive, so state doesn't grow forever.
"""
from pyspark.sql import SparkSession, functions as F, Window

spark = SparkSession.builder.master("local[1]").appName("day02-dedup").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
msgs = spark.read.csv("data/orders_received.csv", header=True, inferSchema=True)

w = Window.partitionBy("order_id").orderBy(F.col("received_at").asc())
orders = (msgs.withColumn("rn", F.row_number().over(w))
              .filter("rn = 1").drop("rn"))

orders.select("order_id", "customer_id", "amount", "received_at").orderBy("order_id").show()
orders.agg(F.sum("amount").alias("total"), F.count("*").alias("orders")).show()

# Streaming version (shown, not run here):
# (spark.readStream ...
#      .withWatermark("event_time", "1 hour")
#      .dropDuplicatesWithinWatermark(["order_id"]))
spark.stop()
