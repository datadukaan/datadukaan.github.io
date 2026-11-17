"""Layer 3, gold: business-ready tables. This is what dashboards read."""
import duckdb
con = duckdb.connect("medallion.duckdb")
con.sql("""CREATE OR REPLACE TABLE gold_stock_by_item AS
           SELECT item, sum(qty) AS qty, any_value(unit) AS unit, count(*) AS slips
           FROM silver_slips GROUP BY item ORDER BY item""")
print(con.sql("SELECT * FROM gold_stock_by_item"))
