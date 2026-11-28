"""Step 1: Spark breaks input into partitions (one task each), ~maxPartitionBytes per piece.

Real clusters use 128 MB pieces: 1 TB / 128 MB = 8,192 tasks. Our file is tiny,
so we shrink the piece size to see the same effect.
"""
from _spark import spark

for piece_mb in (128, 4, 1):
    s = spark(**{"spark.sql.files.maxPartitionBytes": f"{piece_mb}m"})
    df = s.read.parquet("data/sales")
    print(f"piece size {piece_mb:>3} MB -> {df.rdd.getNumPartitions():>3} partitions (= tasks in the first stage)")
    s.stop()

print(f"\nAt real scale: 1 TB / 128 MB = {1024 * 1024 // 128:,} tasks")
