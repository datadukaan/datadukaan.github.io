"""Day 3 - Fix 2: a sequence number per order.

The source gives every change to an order the next number (1, 2, 3...).
Unlike a phone's clock, a counter can't be wrong about which came later,
so "highest seq wins" gets both 101 and 102 right.
"""
from pyspark.sql import SparkSession, functions as F, Window

spark = SparkSession.builder.master("local[1]").appName("day03-seq").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
msgs = spark.read.csv("data/order_messages.csv", header=True, inferSchema=True)

w = Window.partitionBy("order_id").orderBy(F.col("seq").desc())
current = msgs.withColumn("rn", F.row_number().over(w)).filter("rn = 1")

current.select("order_id", "seq", "type", "amount").orderBy("order_id").show()
current.agg(F.sum("amount").alias("total")).show()
spark.stop()
