"""Day 9 - Fix 2: schema evolution - add the new column, keep going.

October and November are stored as Parquet in the same table folder.
Without schema merging, Spark picks one file's schema; with mergeSchema
the table gets the union of columns, and old rows show discount = null.
On Delta Lake the same switch is .option("mergeSchema", "true") on write.
"""
import shutil
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[1]").appName("day09-evolve").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
shutil.rmtree("out/bills", ignore_errors=True)

for month in ("october", "november"):
    (spark.read.csv(f"data/bill_{month}.csv", header=True, inferSchema=True)
          .write.mode("overwrite").parquet(f"out/bills/month={month}"))

merged = spark.read.option("mergeSchema", "true").parquet("out/bills")
print("columns with mergeSchema:", merged.columns)
merged.orderBy("month", "item").show()

# DataFrames from different schemas: union by NAME and allow missing columns
oct_ = spark.read.csv("data/bill_october.csv", header=True, inferSchema=True)
nov = spark.read.csv("data/bill_november.csv", header=True, inferSchema=True)
print("unionByName(allowMissingColumns=True) rows:", oct_.unionByName(nov, allowMissingColumns=True).count())
spark.stop()
