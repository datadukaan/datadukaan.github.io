"""Fix 2: filter on the partition column and the engine reads only that folder."""
import pyarrow.dataset as ds, duckdb
d = ds.dataset("data/by_month", format="parquet", partitioning="hive")
all_files = len(d.files)
oct_files = len(list(d.get_fragments(filter=ds.field("month") == "2026-10")))
print(f"pyarrow : WHERE month = '2026-10' -> reads {oct_files} of {all_files} folders' files")

plan = duckdb.sql("""EXPLAIN ANALYZE SELECT sum(qty_kg) FROM read_parquet('data/by_month/**/*.parquet', hive_partitioning = true)
                     WHERE month = '2026-10' AND item = 'sugar'""").fetchall()[0][1]
line = next(l for l in plan.splitlines() if "Scanning Files" in l)
print("duckdb  :", " ".join(line.replace("│", "").split()))

from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.master("local[2]").config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
q = spark.read.parquet("data/by_month").where((F.col("month") == "2026-10") & (F.col("item") == "sugar")).agg(F.sum("qty_kg"))
scan = [l for l in q._jdf.queryExecution().executedPlan().toString().splitlines() if "FileScan" in l][0]
import re; print("spark   :", re.search(r"PartitionFilters: \[[^\]]*\]", scan).group(0))
print(f"sugar in Oct: {q.collect()[0][0]:,} kg")
spark.stop()
