"""Local Spark session helper: 'local[n]' = n worker threads on this laptop."""
import os
os.environ.setdefault("PYSPARK_PYTHON", "python3")
from pyspark.sql import SparkSession
def spark(cores="*", **conf):
    b = (SparkSession.builder.master(f"local[{cores}]").appName("day21")
         .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false").config("spark.sql.shuffle.partitions", "8"))
    for k, v in conf.items(): b = b.config(k, v)
    s = b.getOrCreate(); s.sparkContext.setLogLevel("ERROR"); return s
