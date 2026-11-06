"""Day 6 - Fix 1: soft delete - mark the row as deleted, keep it.

Instead of DELETE, the app runs:
    UPDATE orders SET is_deleted = true, updated_at = now() WHERE order_id = 7
The row still exists and its updated_at moved, so the same incremental load
now picks it up and the copy learns about the cancellation.
"""
from pyspark.sql import SparkSession, functions as F, Window

spark = SparkSession.builder.master("local[1]").appName("day06-soft").config("spark.sql.session.timeZone", "UTC").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
read = lambda f: spark.read.csv(f"data/{f}", header=True, inferSchema=True)

copy = read("orders_night1.csv").withColumn("is_deleted", F.lit(False))
mark = copy.agg(F.date_format(F.max("updated_at"), "yyyy-MM-dd HH:mm:ss")).first()[0]

source = read("orders_night2_soft_delete.csv")
new = source.filter(F.col("updated_at") > F.to_timestamp(F.lit(mark)))
print("Night 2: rows changed since the mark =", new.count())
new.show()

w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
copy = copy.unionByName(new).withColumn("rn", F.row_number().over(w)).filter("rn = 1").drop("rn")

print("Copy now knows order 7 is cancelled:")
copy.filter("order_id = 7").show()
print("But a report that sums every row is still wrong:")
copy.agg(F.sum("amount").alias("total")).show()
spark.stop()
