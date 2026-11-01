"""Day 1 - Fix 2: a watermark lets a streaming job wait a little for late data.

We replay the orders in the order they ARRIVED, one micro-batch per arrival, and
keep a running daily total by EVENT time with a 2-hour watermark.

- Orders that are a little late (within 2 hours of the latest event seen) are still counted.
- Orders that are later than the watermark are DROPPED by the stream. That is the
  trade-off of a watermark, and why Fix 3 (reprocessing) exists.

Run:  python 02_watermark_streaming.py
"""
import os, shutil, tempfile
import pandas as pd
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder.master("local[1]").appName("day01-watermark")
         .config("spark.sql.shuffle.partitions", 1)
         .config("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", False)
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

src = tempfile.mkdtemp()
orders = pd.read_csv("data/orders.csv").sort_values("ingest_time")
schema = "order_id INT, amount LONG, event_time TIMESTAMP, ingest_time TIMESTAMP"

stream = (spark.readStream.schema(schema).option("header", True)
          .option("maxFilesPerTrigger", 1).csv(src))

daily = (stream
         .withWatermark("event_time", "2 hours")
         .groupBy(F.window("event_time", "1 day").alias("w"))
         .agg(F.sum("amount").alias("total"), F.count("*").alias("orders")))

q = (daily.writeStream.outputMode("update").format("memory").queryName("daily")
     .option("checkpointLocation", tempfile.mkdtemp()).start())

for i, row in enumerate(orders.itertuples(index=False)):
    pd.DataFrame([row._asdict()]).to_csv(os.path.join(src, f"{i:03d}.csv"), index=False)
    q.processAllAvailable()

q.stop()
result = (spark.table("daily")
          .groupBy(F.to_date("w.start").alias("day"))
          .agg(F.max("total").alias("total_counted_by_stream"))
          .orderBy("day"))
result.show()
# Sunday's late orders arrived ~36 hours late, beyond the 2-hour watermark,
# so the stream keeps Sunday at 2,00,000. Reprocessing (Fix 3) corrects it.
shutil.rmtree(src, ignore_errors=True)
spark.stop()
