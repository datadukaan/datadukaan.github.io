"""Why bronze matters: silver v1 shipped with a bug (forgot to convert grams). Because bronze kept every
raw row, we fix the code and rebuild silver and gold from bronze. No re-asking the supplier."""
import duckdb
con = duckdb.connect("medallion.duckdb")

def build(convert_units):
    qty = "CASE unit WHEN 'g' THEN TRY_CAST(qty AS DOUBLE) / 1000 ELSE TRY_CAST(qty AS DOUBLE) END" if convert_units else "TRY_CAST(qty AS DOUBLE)"
    con.sql(f"""CREATE OR REPLACE TABLE silver_slips AS
                SELECT slip_id, item, {qty} AS qty FROM bronze_slips
                WHERE TRY_CAST(qty AS DOUBLE) IS NOT NULL
                QUALIFY row_number() OVER (PARTITION BY slip_id ORDER BY _load_time) = 1""")
    con.sql("CREATE OR REPLACE TABLE gold_stock_by_item AS SELECT item, sum(qty) AS qty FROM silver_slips GROUP BY item")
    return con.sql("SELECT qty FROM gold_stock_by_item WHERE item = 'onion'").fetchall()[0][0]

print(f"silver v1 (bug: no unit conversion) -> gold onions: {build(False):,.0f} kg")
print(f"bronze rows still available        : {con.sql('SELECT count(*) FROM bronze_slips').fetchall()[0][0]}")
print(f"silver v2 replayed from bronze      -> gold onions: {build(True):,.0f} kg")
