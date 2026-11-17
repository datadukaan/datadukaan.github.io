"""Layer 2, silver: deduplicate, cast types, fix units. Bad rows go to quarantine, not the bin."""
import duckdb
con = duckdb.connect("medallion.duckdb")
con.sql("""CREATE OR REPLACE TEMP VIEW typed AS
           SELECT slip_id, item, TRY_CAST(qty AS DOUBLE) AS qty_num, qty AS qty_raw, unit,
                  received_at::TIMESTAMP AS received_at, _source_file,
                  row_number() OVER (PARTITION BY slip_id ORDER BY _load_time) AS rn
           FROM bronze_slips""")
con.sql("""CREATE OR REPLACE TABLE quarantine_slips AS
           SELECT slip_id, item, qty_raw, unit, _source_file, 'qty is not a number' AS reason
           FROM typed WHERE rn = 1 AND qty_num IS NULL""")
con.sql("""CREATE OR REPLACE TABLE silver_slips AS
           SELECT slip_id, item,
                  CASE unit WHEN 'g' THEN qty_num / 1000 ELSE qty_num END AS qty,
                  CASE unit WHEN 'g' THEN 'kg' ELSE unit END AS unit,
                  received_at
           FROM typed WHERE rn = 1 AND qty_num IS NOT NULL""")
print("silver:"); print(con.sql("SELECT * FROM silver_slips ORDER BY slip_id"))
print("quarantine:"); print(con.sql("SELECT slip_id, item, qty_raw, reason FROM quarantine_slips"))
