"""Layer 1, bronze: land every file exactly as it arrived. Append-only, all text, plus lineage columns."""
import duckdb, glob
con = duckdb.connect("medallion.duckdb")
con.sql("""CREATE OR REPLACE TABLE bronze_slips (slip_id VARCHAR, item VARCHAR, qty VARCHAR, unit VARCHAR,
           received_at VARCHAR, _load_time TIMESTAMP, _source_file VARCHAR)""")
for f in sorted(glob.glob("landing/*.csv")):
    con.sql(f"""INSERT INTO bronze_slips
                SELECT *, now()::TIMESTAMP, '{f.split('/')[-1]}' FROM read_csv('{f}', all_varchar=true)""")
print(con.sql("SELECT slip_id, item, qty, unit, _source_file FROM bronze_slips"))
print(f"bronze rows: {con.sql('SELECT count(*) FROM bronze_slips').fetchall()[0][0]} (duplicates and bad rows kept on purpose)")
