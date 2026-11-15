import os, time, duckdb

def layout(path):
    folders = sum(1 for _, ds_, fs in os.walk(path) if fs)
    files = sum(len(fs) for _, _, fs in os.walk(path))
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(path) for f in fs)
    return folders, files, size

def sugar_last_month(path, runs=3):
    """The supplier's question: how much sugar in October 2026?"""
    best = 1e9
    for _ in range(runs):
        con = duckdb.connect(); t = time.time()
        kg = con.sql(f"""SELECT sum(qty_kg) FROM read_parquet('{path}/**/*.parquet', hive_partitioning = true)
                          WHERE item = 'sugar' AND bill_date BETWEEN DATE '2026-10-01' AND DATE '2026-10-31'""").fetchall()[0][0]
        best = min(best, time.time() - t); con.close()
    return kg, best
