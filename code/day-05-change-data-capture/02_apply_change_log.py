"""Day 5 - Fix 1 + 2: read the change log and apply it to the copy (CDC).

Every database already writes each insert (c), update (u) and delete (d) to its
log. A CDC tool (Debezium, Fivetran, Azure Data Factory, Databricks...) reads
that log and emits one event per change. The copy applies them in log order (lsn).
Only 4 events are read - not the whole table - and deletes come through too.
"""
from pyspark.sql import SparkSession, functions as F, Window

spark = SparkSession.builder.master("local[1]").appName("day05-cdc").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
read = lambda f: spark.read.csv(f"data/{f}", header=True, inferSchema=True)

copy = read("menu_snapshot_midnight.csv")
log = read("change_log.csv")
print("Change log events:")
log.orderBy("lsn").show()

# Latest event per key wins (lsn order), then: c/u -> upsert, d -> delete
w = Window.partitionBy("item_id").orderBy(F.col("lsn").desc())
latest = log.withColumn("rn", F.row_number().over(w)).filter("rn = 1")

untouched = copy.join(latest, "item_id", "left_anti")
upserts = latest.filter("op in ('c', 'u')").select("item_id", "item", "price")
copy = untouched.unionByName(upserts)

print("Copy after applying the log:")
copy.orderBy("item_id").show()
source = read("menu_source_noon.csv")
same = copy.exceptAll(source).count() == 0 and source.exceptAll(copy).count() == 0
print("copy == source:", same)
spark.stop()
