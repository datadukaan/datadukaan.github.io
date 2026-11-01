#!/usr/bin/env bash
# Replays two nights: Monday (late orders not here yet) and Tuesday (they arrive).
set -e
cd "$(dirname "$0")"
rm -f day01.duckdb
dbt seed --profiles-dir . -q
dbt run --profiles-dir . -q --full-refresh --vars '{as_of: "2026-10-26 23:59:59"}'
echo "Monday night:";  python3 -c "import duckdb; print(duckdb.connect('day01.duckdb').sql('select * from daily_sales order by 1'))"
dbt run --profiles-dir . -q --vars '{as_of: "2026-10-27 23:59:59"}'
echo "Tuesday night (late Sunday orders merged in):"; python3 -c "import duckdb; print(duckdb.connect('day01.duckdb').sql('select * from daily_sales order by 1'))"
