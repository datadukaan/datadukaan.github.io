# Day 9 · Schema drift: code

Sample data: Raju's supplier bills.

- `data/bill_october.csv`: `item, qty, price` (total ₹18,000).
- `data/bill_november.csv`: a new `discount` column appears **before** `price`.
- `data/bill_december_breaking.csv`: `price` is renamed to `amount` (a breaking change).
- `contract_supplier_bill.json`: the agreed columns, types and rules.

| File | Shows | Expected result |
|---|---|---|
| `01_read_by_position.py` | The problem: "column 3" (PySpark) | October ₹18,000; November ₹1,800, silently wrong |
| `02_read_by_name.py` | Fix 1: `select("price")` | ₹18,000 both months; December fails loudly |
| `03_schema_evolution.py` | Fix 2: `mergeSchema`, `unionByName(allowMissingColumns=True)` | both months in one table, October discount = null |
| `04_data_contract.py` | Fix 3: check files against the contract before loading | Oct PASS, Nov PASS (new column allowed), Dec BLOCKED |
| `platform_notes.sql` | Delta enforcement/evolution, column mapping, Auto Loader, Snowflake, dbt contracts | (notes, not run) |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run every script from this folder.
