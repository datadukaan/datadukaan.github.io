#!/usr/bin/env bash
# Replays the change log up to lsn 101 (just the price change), then up to 104 (all changes).
set -e
cd "$(dirname "$0")"
rm -f day05.duckdb
dbt seed --profiles-dir . -q
show() { python3 -c "import duckdb; print(duckdb.connect('day05.duckdb').sql('select * from menu_copy order by 1'))"; }
dbt run --profiles-dir . -q --vars '{up_to_lsn: 101}'
echo "Copy after lsn 101 (thali price change):"; show
dbt run --profiles-dir . -q --vars '{up_to_lsn: 104}'
echo "Copy after lsn 104 (all changes, Vada deleted):"; show
