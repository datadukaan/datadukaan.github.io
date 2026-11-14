import os, time, duckdb

def files(folder):
    names = [n for n in os.listdir(folder) if n.endswith(".parquet")]
    return len(names), sum(os.path.getsize(os.path.join(folder, n)) for n in names)

def rice_query(folder, runs=3):
    """The caterer's question: how much rice this year? Best of 3 runs, fresh connection each time."""
    best = 1e9
    for _ in range(runs):
        con = duckdb.connect(); t = time.time()
        kg = con.sql(f"SELECT sum(qty_kg) FROM read_parquet('{folder}/*.parquet') WHERE item = 'rice'").fetchall()[0][0]
        best = min(best, time.time() - t); con.close()
    return kg, best
