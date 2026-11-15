"""Fix 3: a small table (the tea stall) needs no partitions - one file, sorted by date."""
import os, shutil, random, datetime as dt
import pyarrow as pa, pyarrow.dataset as ds, pyarrow.parquet as pq
random.seed(4)
rows = [{"bill_date": dt.date(2026, 1, 1) + dt.timedelta(days=random.randrange(365)), "item": random.choice(["chai", "bun", "biscuit"]),
         "qty": random.randint(1, 6)} for _ in range(20_000)]
t = pa.Table.from_pylist(rows)

shutil.rmtree("data/tea_partitioned", ignore_errors=True)
ds.write_dataset(t, "data/tea_partitioned", format="parquet", partitioning=["bill_date"], partitioning_flavor="hive", max_partitions=1000)
n_part = sum(len(fs) for _, _, fs in os.walk("data/tea_partitioned"))

os.makedirs("data", exist_ok=True)
pq.write_table(t.sort_by("bill_date"), "data/tea_clustered.parquet", row_group_size=2_000)   # sort = cluster
md = pq.ParquetFile("data/tea_clustered.parquet").metadata; di = md.schema.names.index("bill_date")
oct_ = dt.date(2026, 10, 1); nov = dt.date(2026, 10, 31)
read = sum(1 for g in range(md.num_row_groups)
           if md.row_group(g).column(di).statistics.max >= oct_ and md.row_group(g).column(di).statistics.min <= nov)
part_kb = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk("data/tea_partitioned") for f in fs) / n_part / 1e3
print(f"partitioned by day : {n_part} files, avg {part_kb:.1f} KB each")
print(f"clustered          : 1 file ({os.path.getsize('data/tea_clustered.parquet')/1e3:.0f} KB), {md.num_row_groups} row groups sorted by date")
print(f"October query      : reads {read} of {md.num_row_groups} row groups (min/max skipping, Day 11)")
