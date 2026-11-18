"""The same guarantees in a real engine (DuckDB): rollback on failure, and a write-write conflict
between two concurrent transactions is rejected instead of silently overwriting."""
import duckdb, os
if os.path.exists("data/irctc.duckdb"): os.remove("data/irctc.duckdb")
os.makedirs("data", exist_ok=True)
con = duckdb.connect("data/irctc.duckdb")
con.execute("CREATE TABLE berths (berth INT PRIMARY KEY, passenger VARCHAR)")
con.execute("INSERT INTO berths VALUES (72, NULL)")

# 1) atomic: debit + booking in one transaction; failure rolls back both
con.execute("CREATE TABLE wallet (who VARCHAR, balance INT)"); con.execute("INSERT INTO wallet VALUES ('Raju', 5000)")
try:
    con.execute("BEGIN")
    con.execute("UPDATE wallet SET balance = balance - 3000 WHERE who = 'Raju'")
    raise RuntimeError("booking service timed out")
except RuntimeError as e:
    con.execute("ROLLBACK"); print(f"failed: {e} -> rolled back")
print("Raju's balance:", con.execute("SELECT balance FROM wallet").fetchall()[0][0], "(no paisa kat gaya)")

# 2) concurrency: two transactions update the same berth
a, b = con.cursor(), con.cursor()
a.execute("BEGIN"); b.execute("BEGIN")
a.execute("UPDATE berths SET passenger = 'Raju' WHERE berth = 72 AND passenger IS NULL")
try:
    b.execute("UPDATE berths SET passenger = 'stranger' WHERE berth = 72 AND passenger IS NULL")
    b.execute("COMMIT")
except duckdb.TransactionException as e:
    print("stranger's transaction:", str(e).split("\n")[0][:90]); b.execute("ROLLBACK")
a.execute("COMMIT")
print("berth 72:", con.execute("SELECT passenger FROM berths").fetchall()[0][0])
