"""Day 5 - Fix 3: a checkpoint - remember where you stopped in the log.

The CDC consumer applies events one at a time and saves the last lsn it applied.
We make it crash after event 102, then restart it three ways:
  - from the checkpoint          -> continues at 103, copy matches the source
  - from the latest event ("now") -> skips 103, the deleted Vada lives on
  - from the very beginning       -> safe only because every apply is idempotent
"""
import duckdb, shutil

def apply(con, lsn, op, item_id, item, price):
    if op == "d":
        con.execute("delete from copy where item_id = ?", [item_id])
    else:
        con.execute("""insert into copy values (?, ?, ?)
                       on conflict (item_id) do update set item = excluded.item, price = excluded.price""",
                    [item_id, item, price])

def run(start_after, label):
    con = duckdb.connect()
    con.execute("create table copy (item_id int primary key, item varchar, price int)")
    con.execute("insert into copy select * from read_csv_auto('data/menu_snapshot_midnight.csv')")
    con.execute("create table checkpoint (last_lsn int)")
    con.execute("insert into checkpoint values (0)")
    log = con.execute("select lsn, op, item_id, item, price from read_csv_auto('data/change_log.csv') order by lsn").fetchall()

    # first run: crash after lsn 102
    for e in log:
        if e[0] > 102: break
        apply(con, *e)
        con.execute("update checkpoint set last_lsn = ?", [e[0]])
    saved = con.execute("select last_lsn from checkpoint").fetchall()[0][0]

    # restart
    start = {"checkpoint": saved, "latest": log[-1][0] - 1, "beginning": 0}[start_after]
    for e in log:
        if e[0] > start:
            apply(con, *e)
            con.execute("update checkpoint set last_lsn = ?", [e[0]])

    copy = con.execute("select * from copy order by item_id").fetchall()
    src = con.execute("select * from read_csv_auto('data/menu_source_noon.csv') order by item_id").fetchall()
    items = ", ".join(f"{i} {p}" for _, i, p in copy)
    print(f"restart from {label:<22} checkpoint was {saved}  ->  {items:<38} matches source: {copy == src}")

run("checkpoint", "the checkpoint")
run("latest", "the latest event")
run("beginning", "the beginning")
