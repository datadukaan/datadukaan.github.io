"""Day 4 - Fix 1 + 2: a high-water mark and an incremental load.

Tuesday night: first (full) load, then save the bookmark = the latest updated_at loaded.
Wednesday night: read only rows with updated_at > bookmark and upsert them.

Note: the filter uses updated_at, not created_at, so Tuesday's bill that was fixed
on Wednesday (order 1826) is picked up too.

The catch: order 1827 is stamped 23:40, but its transaction committed AFTER
Tuesday's load ran. Its timestamp is behind the bookmark (23:50), so a strict
"> bookmark" filter never sees it. Fix 3 handles that.
"""
from pyspark.sql import SparkSession, functions as F, Window

spark = SparkSession.builder.master("local[1]").appName("day04-incr").config("spark.sql.session.timeZone", "UTC").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
read = lambda n: spark.read.csv(f"data/source_night{n}.csv", header=True, inferSchema=True)

# Tuesday night: initial load + save the bookmark
target = read(1)
mark = target.agg(F.date_format(F.max("updated_at"), "yyyy-MM-dd HH:mm:ss")).first()[0]
print("Tuesday night: loaded", target.count(), "rows; high-water mark =", mark)

# Wednesday night: only what changed since the bookmark
new = read(2).filter(F.col("updated_at") > F.to_timestamp(F.lit(mark)))
print("Wednesday night: rows read from source =", new.count())
new.orderBy("updated_at").show()

w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
target = (target.unionByName(new).withColumn("rn", F.row_number().over(w))
                .filter("rn = 1").drop("rn"))

full = read(2)
target.agg(F.count("*").alias("orders"), F.sum("amount").alias("total")).show()
missing = full.join(target, "order_id", "left_anti")
print("Orders in source but missing from target:")
missing.show()
spark.stop()
