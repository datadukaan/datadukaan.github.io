"""Step 2 + 3: the Driver plans tasks, Executors run them in parallel.

Same job on 1 core vs all cores of this machine. On a cluster, 'all cores'
becomes 50 machines x 4 cores = 200 tasks at once.
"""
import os, time
from pyspark.sql import functions as F
from _spark import spark

def run(cores):
    s = spark(cores, **{"spark.sql.files.maxPartitionBytes": "2m"})
    df = s.read.parquet("data/sales")
    heavy = df.withColumn("h", F.sha2(F.concat_ws("|", "order_id", "city", "item"), 256))   # CPU work per row
    heavy.agg(F.count("h")).collect()                      # warm-up (JVM, file listing)
    t = time.time(); heavy.agg(F.count("h")).collect(); dt = time.time() - t
    n = df.rdd.getNumPartitions(); s.stop(); return n, dt

cores = os.cpu_count()
n1, t1 = run(1); nN, tN = run(cores)
print(f"tasks per run      : {n1}")
print(f"1 core             : {t1:5.2f} s  (tasks run one after another)")
print(f"{cores} cores            : {tN:5.2f} s  ({cores} tasks at a time)")
print(f"speed-up           : {t1 / tN:.1f}x")
