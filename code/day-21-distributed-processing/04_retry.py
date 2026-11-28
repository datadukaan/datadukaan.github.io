"""3 AM: one task fails. Spark re-runs just that task (lineage), not the whole job.

local[2,3] = 2 cores, and each task may be attempted up to 3 times.
Task for partition 3 crashes on its first attempt only.
"""
import os
os.environ.setdefault("PYSPARK_PYTHON", "python3")
from pyspark import TaskContext
from pyspark.sql import SparkSession

s = (SparkSession.builder.master("local[2,3]").appName("retry")
     .config("spark.ui.enabled", "false").config("spark.ui.showConsoleProgress", "false").getOrCreate())
s.sparkContext.setLogLevel("OFF")
sc = s.sparkContext

def work(it):
    tc = TaskContext.get()
    if tc.partitionId() == 3 and tc.attemptNumber() == 0:
        raise RuntimeError("machine died at 3 AM")
    yield (tc.partitionId(), tc.attemptNumber(), sum(it))

out = sc.parallelize(range(1, 8001), 8).mapPartitions(work).collect()
for pid, attempt, total in out:
    note = "  <- re-run (attempt 2)" if attempt else ""
    print(f"partition {pid}: attempt {attempt + 1}, sum {total:>9,}{note}")
print(f"\ngrand total {sum(t for *_, t in out):,} (correct: {sum(range(1, 8001)):,})")
s.stop()
