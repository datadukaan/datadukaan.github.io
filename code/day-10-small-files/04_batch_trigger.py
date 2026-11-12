"""Fix 3: Spark Structured Streaming caps each batch: at most 50 files per trigger."""
import os, shutil
from pyspark.sql import SparkSession
from common import drop_slips, fresh

LANDING, CKPT = "landing", "_checkpoint"
fresh(LANDING); shutil.rmtree(CKPT, ignore_errors=True)
drop_slips(LANDING, 230)

spark = (SparkSession.builder.master("local[2]").appName("day10")
         .config("spark.ui.enabled", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

batches = []
def handle(df, batch_id):
    batches.append((batch_id, df.count()))

q = (spark.readStream.schema("order_id INT, item STRING, qty INT, amount INT")
     .option("maxFilesPerTrigger", 50)       # "50 slips..."
     .json(LANDING)
     .writeStream.foreachBatch(handle)
     .option("checkpointLocation", CKPT)
     .trigger(availableNow=True)             # in production: .trigger(processingTime="5 minutes")
     .start())
q.awaitTermination()
for b, n in batches:
    print(f"batch {b}: {n} files")
print(f"230 files -> {len(batches)} jobs, never more than 50 files each")
spark.stop()
