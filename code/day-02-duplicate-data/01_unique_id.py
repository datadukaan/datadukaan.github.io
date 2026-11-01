"""Day 2 - Fix 1: give every order a unique ID.

A weak network made the rider's phone retry, so orders 101 and 105 arrived twice.
Summing every message counts them twice (2,60,000). Without an ID you can't tell a
retry from a real second order: customer C01 genuinely bought a second Rs 500 item
(order 111), and a "same customer + same amount" rule would wrongly throw it away.
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day02-unique-id").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
msgs = spark.read.csv("data/orders_received.csv", header=True, inferSchema=True)

print("Messages received:", msgs.count())
msgs.agg(F.sum("amount").alias("naive_total")).show()

# Guessing duplicates without an ID: same customer + same amount
guess = msgs.dropDuplicates(["customer_id", "amount"])
print("Dedup by (customer_id, amount) - WRONG, drops real order 111:")
guess.agg(F.sum("amount").alias("total"), F.count("*").alias("orders")).show()

# With a unique order ID, a retry and a real repeat look different
print("Copies per order_id:")
msgs.groupBy("order_id", "customer_id", "amount").count().filter("count > 1").show()
msgs.agg(F.countDistinct("order_id").alias("real_orders")).show()
spark.stop()
