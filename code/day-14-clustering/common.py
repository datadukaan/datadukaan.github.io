import glob
import pyarrow.parquet as pq

def blocks_read(folder, column, value):
    """Count row groups whose min/max range could contain `value` (what data skipping does)."""
    read = total = 0
    for f in sorted(glob.glob(f"{folder}/*.parquet")):
        md = pq.ParquetFile(f).metadata; ci = md.schema.names.index(column)
        for g in range(md.num_row_groups):
            st = md.row_group(g).column(ci).statistics; total += 1
            if st.min <= value <= st.max: read += 1
    return read, total

def show(label, folder, column, value):
    r, t = blocks_read(folder, column, value)
    print(f"{label:34s}: reads {r:>3} of {t} blocks ({100*r/t:.0f}%)")
