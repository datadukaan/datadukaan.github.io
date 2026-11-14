"""Fix 2: optimized writes - group rows by partition BEFORE writing, so each partition gets one file."""
import os, shutil
from pyspark.sql import SparkSession, functions as F
spark = (SparkSession.builder.master("local[4]").appName("day12").config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false")
         .config("spark.sql.shuffle.partitions", 50).getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
df = spark.read.parquet("data/sales_small").withColumn("month", F.date_format("bill_date", "yyyy-MM"))
df = df.repartition(50)        # data spread over 50 tasks, like after any shuffle or join

def count_files(path):
    return sum(1 for root, _, fs in os.walk(path) for f in fs if f.endswith(".parquet"))

shutil.rmtree("data/out_naive", ignore_errors=True); shutil.rmtree("data/out_optimized", ignore_errors=True)
df.write.partitionBy("month").parquet("data/out_naive")                          # every task writes to every month
df.repartition("month").write.partitionBy("month").parquet("data/out_optimized")  # one task per month
print(f"naive write     : {count_files('data/out_naive'):>4} files for 11 months")
print(f"optimized write : {count_files('data/out_optimized'):>4} files for 11 months")
spark.stop()
