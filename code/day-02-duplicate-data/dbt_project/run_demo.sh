#!/usr/bin/env bash
# Runs the incremental model three times on the same data: the total never changes.
set -e
cd "$(dirname "$0")"
rm -f day02.duckdb
dbt seed --profiles-dir . -q
for run in 1 2 3; do
  if [ $run = 1 ]; then dbt run --profiles-dir . -q --full-refresh; else dbt run --profiles-dir . -q; fi
  echo "after run $run:"; python3 -c "import duckdb; print(duckdb.connect('day02.duckdb').sql('select sum(amount) as total, count(*) as orders from orders'))"
done
