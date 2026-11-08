"""Day 8 - Fix 2: a _SUCCESS marker - light the diya when the order is ready.

A dataset is often a FOLDER of many part files, and they can't all be renamed
at once. Spark (and Hadoop) write an empty _SUCCESS file into the folder only
after every part file has been committed. Readers wait for it.
"""
import os, shutil, time
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[2]").appName("day08-success").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
OUT = "out/sweets/dt=2026-11-08"
shutil.rmtree("out/sweets", ignore_errors=True)

df = spark.read.csv("data/diwali_boxes.csv", header=True, inferSchema=True)
df.repartition(2).write.mode("overwrite").parquet(OUT)

print("folder after Spark's write:")
for f in sorted(os.listdir(OUT)):
    if not f.startswith("."):
        print(f"  {f:<45} {os.path.getsize(os.path.join(OUT, f)):>6} bytes")

def wait_for_success(path, timeout_s=10, every_s=0.5):
    """What a downstream job (or an Airflow sensor) does before reading."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if os.path.exists(os.path.join(path, "_SUCCESS")):
            return True
        time.sleep(every_s)
    return False

if wait_for_success(OUT):
    got = spark.read.parquet(OUT)
    print(f"_SUCCESS found -> read {got.count()} boxes")
spark.stop()
