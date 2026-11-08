"""Day 8 - Fix 3: a manifest check - count the boxes before the van leaves.

The writer also writes manifest.json: how many rows, which files, and a
checksum of each. The reader recounts and refuses to load if anything
doesn't match - e.g. a file cut short by a network drop during upload.
"""
import csv, hashlib, json, os, shutil

shutil.rmtree("out/delivery", ignore_errors=True)
os.makedirs("out/delivery")
SRC = "data/diwali_boxes.csv"

def sha256(path): return hashlib.sha256(open(path, "rb").read()).hexdigest()
def rows_in(path): return sum(1 for _ in csv.DictReader(open(path)))

# Writer: copy the file and describe it in a manifest
shutil.copy(SRC, "out/delivery/boxes.csv")
manifest = {"files": {"boxes.csv": {"rows": rows_in(SRC), "sha256": sha256(SRC)}}}
json.dump(manifest, open("out/delivery/manifest.json", "w"), indent=2)

def check(folder):
    m = json.load(open(os.path.join(folder, "manifest.json")))
    for name, exp in m["files"].items():
        p = os.path.join(folder, name)
        rows, digest = rows_in(p), sha256(p)
        ok = rows == exp["rows"] and digest == exp["sha256"]
        print(f"  {name}: rows {rows}/{exp['rows']}, checksum {'match' if digest == exp['sha256'] else 'MISMATCH'} -> {'LOAD' if ok else 'REJECT'}")
        if not ok: return False
    return True

print("Delivery 1 (complete):"); check("out/delivery")

# Delivery 2: the upload got cut off after 120 rows
lines = open(SRC).read().splitlines()[:121]
open("out/delivery/boxes.csv", "w").write("\n".join(lines) + "\n")
print("Delivery 2 (upload cut short):"); check("out/delivery")
