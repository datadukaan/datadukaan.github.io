"""Day 8 - Fix 1: write to a hidden temp name, then rename in one step.

The writer packs into out/_tmp/boxes.csv.part (the back room). Only when it
is complete does it call os.replace() to move it to out/boxes.csv. A rename
within one filesystem is atomic: a reader sees either no file or the whole file.
"""
import csv, os, threading, time, shutil

shutil.rmtree("out", ignore_errors=True)
os.makedirs("out/_tmp", exist_ok=True)
SRC, TMP, DST = "data/diwali_boxes.csv", "out/_tmp/boxes.csv.part", "out/boxes.csv"
rows = list(csv.reader(open(SRC)))
header, data = rows[0], rows[1:]

def writer():
    with open(TMP, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header)
        for r in data:
            w.writerow(r); f.flush(); time.sleep(0.01)
        os.fsync(f.fileno())                     # make sure bytes are on disk
    os.replace(TMP, DST)                         # atomic: all or nothing

seen = []
def reader():
    for _ in range(30):                          # the driver checks every 0.1 s
        if os.path.exists(DST):
            with open(DST) as f: seen.append(len(list(csv.DictReader(f))))
        else:
            seen.append(0)
        time.sleep(0.1)

tw = threading.Thread(target=writer); tr = threading.Thread(target=reader)
tw.start(); tr.start(); tw.join(); tr.join()
print("what the reader saw on each check:", sorted(set(seen)))
print("=> only 0 (not there yet) or 200 (complete). Never a partial file.")
