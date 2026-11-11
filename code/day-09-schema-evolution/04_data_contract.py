"""Day 9 - Fix 3: a data contract - agree before you change.

contract_supplier_bill.json says which columns consumers rely on, their
types, and whether new columns are allowed. Every file is checked BEFORE
loading: additive changes pass, breaking ones are stopped with a clear message.
"""
import csv, json

contract = json.load(open("contract_supplier_bill.json"))
types = {"integer": int, "string": str}

def check(path):
    rows = list(csv.DictReader(open(path)))
    cols = list(rows[0].keys())
    problems = []
    for name, spec in contract["columns"].items():
        if name not in cols:
            if spec["required"]: problems.append(f"missing required column '{name}'")
            continue
        for r in rows:
            try: types[spec["type"]](r[name])
            except ValueError: problems.append(f"'{name}' = {r[name]!r} is not {spec['type']}"); break
    extra = [c for c in cols if c not in contract["columns"]]
    if extra and not contract["allow_new_columns"]:
        problems.append(f"new columns not allowed: {extra}")
    status = "PASS" if not problems else "BLOCKED"
    note = f"(new columns {extra} allowed)" if extra and not problems else ""
    print(f"{path:<34} {status} {note}")
    for p in problems: print(f"    - {p}")
    return not problems

for f in ("data/bill_october.csv", "data/bill_november.csv", "data/bill_december_breaking.csv"):
    check(f)
