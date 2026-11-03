"""Day 3 - Fix 1: pick the latest version by EVENT time, not arrival order.

Order 101: the 9:02 change (Rs 800) arrived BEFORE the 9:00 order (Rs 500).
"Last message received wins" keeps Rs 500 - the bug from the video.
"Latest event_time wins" fixes 101... but order 102 shows the catch: that
phone's clock was 3 minutes slow, so its change is stamped 9:58, before the
10:00 order, and event time alone picks the old value. Fix 2 solves that.
"""
from pyspark.sql import SparkSession, functions as F, Window

spark = SparkSession.builder.master("local[1]").appName("day03-event-time").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
msgs = spark.read.csv("data/order_messages.csv", header=True, inferSchema=True)

def latest(order_col, label):
    w = Window.partitionBy("order_id").orderBy(F.col(order_col).desc())
    out = msgs.withColumn("rn", F.row_number().over(w)).filter("rn = 1").select("order_id", "amount")
    print(f"Latest by {label}:")
    out.orderBy("order_id").show()
    out.agg(F.sum("amount").alias("total")).show()

latest("received_at", "ARRIVAL (last message received wins)")
latest("event_time", "EVENT TIME")
spark.stop()
