"""Fix 3: auto compaction - after each write, check for small files and merge them right away."""
import os, shutil, random
import pyarrow as pa, pyarrow.dataset as ds, pyarrow.parquet as pq

FOLDER, THRESHOLD = "data/sales_auto", 50          # "when the box hits 50 slips"
shutil.rmtree(FOLDER, ignore_errors=True); os.makedirs(FOLDER)
random.seed(4); seq = 0; compactions = 0

def small_files():
    return sorted(n for n in os.listdir(FOLDER) if n.startswith("small-"))

def auto_compact():
    global seq, compactions
    small = small_files()
    if len(small) < THRESHOLD: return
    table = ds.dataset([os.path.join(FOLDER, n) for n in small]).to_table()
    pq.write_table(table, f"{FOLDER}/big-{compactions:03d}.parquet")
    for n in small: os.remove(os.path.join(FOLDER, n))
    compactions += 1

for write in range(1, 2001):                       # 2,000 small appends, like make_data.py
    rows = [{"item": random.choice(["rice", "dal", "oil"]), "qty_kg": random.randint(1, 25)} for _ in range(250)]
    pq.write_table(pa.Table.from_pylist(rows), f"{FOLDER}/small-{seq:05d}.parquet"); seq += 1
    auto_compact()                                 # runs after every write
    if write in (49, 50, 51, 500, 1000, 2000):
        print(f"after write {write:>4}: {len(os.listdir(FOLDER)):>3} files ({len(small_files())} small)")
print(f"compactions run: {compactions}; files left: {len(os.listdir(FOLDER))} instead of 2,000")
