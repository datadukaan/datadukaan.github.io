# Day 11 · Columnar formats: code

Sample data: Raju's register, 1,000,000 bills (Jan 2025 to Nov 2026), created by `make_data.py` as `data/bills.csv` (~33 MB, not committed).

| File | Shows | Expected result |
|---|---|---|
| `make_data.py` | Creates the CSV register | 1,000,000 bills, 33 MB |
| `01_row_based_read.py` | The problem: SUM(tax) from CSV parses all 6 columns | 33 MB read for 1 column |
| `02_columnar_format.py` | Fix 1: Parquet, read only `tax` | 0.6 MB read |
| `03_compression.py` | Fix 2: dictionary/RLE encoding + snappy/zstd | ~13x smaller than CSV |
| `04_predicate_pushdown.py` | Fix 3: row-group min/max stats skip blocks (pyarrow + DuckDB) | 5 of 10 row groups read |
| `05_spark_parquet.py` | PySpark: column pruning + PushedFilters in the plan | `ReadSchema` has 2 columns |
| `platform_notes.sql` | Delta, Databricks, Snowflake, dbt notes | (notes, not run) |

Requirements: Python 3.10+, Java 17+ (for PySpark), `pip install -r ../../requirements.txt`.
Run `python make_data.py` first, then the scripts in order, from this folder.
