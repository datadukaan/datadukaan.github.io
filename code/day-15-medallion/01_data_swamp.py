"""The problem: raw slips loaded straight into the dashboard table, overwriting it each time."""
import duckdb
con = duckdb.connect()
for f in ["landing/slips_2026-11-16.csv", "landing/slips_2026-11-17.csv"]:
    # each load replaces the table: yesterday's raw data is gone
    con.sql(f"CREATE OR REPLACE TABLE dashboard_stock AS SELECT item, qty, unit FROM read_csv('{f}', all_varchar=true)")
print(con.sql("SELECT * FROM dashboard_stock"))
# what a naive dashboard does with yesterday's file: sums 'qty' ignoring units and duplicates
naive = duckdb.sql("""SELECT sum(TRY_CAST(qty AS DOUBLE)) FROM read_csv('landing/slips_2026-11-16.csv', all_varchar=true)
                      WHERE item = 'onion'""").fetchall()[0][0]
print(f"onions on the dashboard: {naive:,.0f} 'kg'  (grams read as kg + a duplicate slip; real stock: 50 kg)")
print("and the 16-Nov raw rows no longer exist in dashboard_stock, so they can't be re-checked")
