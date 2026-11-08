"""Day 8 - The problem: reading a file while it's still being written.

A writer thread packs 200 Diwali boxes into out/boxes.csv, one row at a time
(2 hours in the story, 2 seconds here). A reader thread (the driver) shows up
halfway and reads whatever is there. No error is raised - it just gets less.
"""
import csv, os, threading, time

os.makedirs("out", exist_ok=True)
SRC, DST = "data/diwali_boxes.csv", "out/boxes.csv"
rows = list(csv.reader(open(SRC)))
header, data = rows[0], rows[1:]

def writer():
    with open(DST, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); f.flush()
        for r in data:
            w.writerow(r); f.flush()
            time.sleep(0.01)                     # packing takes time

def reader(result):
    time.sleep(0.8)                              # the driver arrives early
    with open(DST) as f:
        got = list(csv.DictReader(f))
    result["boxes"] = len(got)
    result["total"] = sum(int(r["price"]) for r in got if r.get("price"))

res = {}
tw = threading.Thread(target=writer); tr = threading.Thread(target=reader, args=(res,))
tw.start(); tr.start(); tw.join(); tr.join()
print(f"boxes ordered : {len(data)}  (Rs {len(data) * 500:,})")
print(f"boxes read    : {res['boxes']}  (Rs {res['total']:,})   <- partial read, no error")
