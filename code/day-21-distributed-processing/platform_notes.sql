-- Day 21 · Distributed processing: platform notes (not run in this repo)

-- ── Piece size (partitions = tasks) ──────────────────────────────
SET spark.sql.files.maxPartitionBytes = 134217728;   -- 128 MB per input piece (default)
SET spark.sql.shuffle.partitions = 400;              -- tasks after a shuffle (default 200)
SET spark.sql.adaptive.enabled = true;               -- AQE: merges tiny shuffle partitions, splits skewed ones

-- ── Cluster size (executors × cores = tasks at once) ─────────────
-- spark-submit --num-executors 50 --executor-cores 4 --executor-memory 16g job.py
-- Databricks: a cluster with 50 workers of 4 cores; or autoscaling min/max workers

-- ── See the shuffle before you run it ────────────────────────────
EXPLAIN FORMATTED
SELECT city, SUM(amount) AS total FROM sales GROUP BY city;   -- look for "Exchange hashpartitioning"

-- ── Retries ──────────────────────────────────────────────────────
SET spark.task.maxFailures = 4;   -- attempts per task before the job fails (default 4)
