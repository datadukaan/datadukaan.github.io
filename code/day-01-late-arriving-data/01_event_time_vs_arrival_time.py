"""Day 1 - Fix 1: count by EVENT time, not ARRIVAL time.

Orders 1006 and 1007 were placed on Sunday 25 Oct but only arrived on Tuesday 27 Oct
(the delivery boy's phone had no network). Grouping by arrival day puts them on the
wrong day; grouping by event day puts them on Sunday where they belong.

Run:  python 01_event_time_vs_arrival_time.py
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day01-event-time").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

orders = (spark.read.option("header", True).csv("data/orders.csv")
          .withColumn("amount", F.col("amount").cast("long"))
          .withColumn("event_time", F.to_timestamp("event_time"))
          .withColumn("ingest_time", F.to_timestamp("ingest_time")))

by_arrival = (orders.groupBy(F.to_date("ingest_time").alias("day"))
              .agg(F.sum("amount").alias("total_by_arrival_time")))
by_event = (orders.groupBy(F.to_date("event_time").alias("day"))
            .agg(F.sum("amount").alias("total_by_event_time")))

(by_event.join(by_arrival, "day", "full")
 .orderBy("day")
 .show())
# Sunday 2026-10-25: 2,00,000 by arrival time, but 2,30,000 by event time.
spark.stop()
