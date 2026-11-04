#!/usr/bin/env bash
# Tuesday night: first (full) build. Wednesday night: incremental run reads only recent rows.
set -e
cd "$(dirname "$0")"
rm -f day04.duckdb
dbt seed --profiles-dir . -q
show() { python3 -c "import duckdb; print(duckdb.connect('day04.duckdb').sql('select count(*) as orders, sum(amount) as total from orders'))"; }
dbt run --profiles-dir . -q --full-refresh --vars '{night: 1}'
echo "Tuesday night (full build):"; show
dbt run --profiles-dir . -q --vars '{night: 2}'
echo "Wednesday night (incremental + 1 hour lookback):"; show
