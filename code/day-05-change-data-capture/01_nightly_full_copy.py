"""Day 5 - The problem: a nightly full copy goes stale.

The son's counter (the copy) was refreshed with a full copy at midnight.
By noon the master (source) has changed 4 times. Until tonight's copy runs,
every read of the copy is wrong - and tonight it copies all rows again
to pick up a handful of changes.
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day05-full-copy").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
read = lambda f: spark.read.csv(f"data/{f}", header=True, inferSchema=True)

copy = read("menu_snapshot_midnight.csv")     # last night's full copy
source = read("menu_source_noon.csv")          # the master right now

diff = (source.alias("s").join(copy.alias("c"), "item_id", "full_outer")
        .select("item_id", F.coalesce("s.item", "c.item").alias("item"),
                F.col("s.price").alias("source_price"), F.col("c.price").alias("copy_price"))
        .filter("source_price is null or copy_price is null or source_price != copy_price"))
print("At noon, rows where the copy disagrees with the source:")
diff.orderBy("item_id").show()

thali_gap = 150 - 120
print(f"40 thalis sold at the copy's price: lost Rs {40 * thali_gap:,}")
spark.stop()
