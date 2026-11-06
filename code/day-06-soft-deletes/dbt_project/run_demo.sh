#!/usr/bin/env bash
# Night 1: build the copy. Night 2: order 7 is soft-deleted; the view drops it, the table keeps it.
set -e
cd "$(dirname "$0")"
rm -f day06.duckdb
dbt seed --profiles-dir . -q
show() { python3 -c "
import duckdb; c = duckdb.connect('day06.duckdb')
for t in ('orders', 'orders_active'):
    n, s = c.execute(f'select count(*), sum(amount) from {t}').fetchall()[0]; print(f'  {t:<14} {n} orders, total {s:,}')"; }
dbt run --profiles-dir . -q --full-refresh --vars '{night: 1}'
echo "Night 1:"; show
dbt run --profiles-dir . -q --vars '{night: 2}'
echo "Night 2 (order 7 cancelled):"; show
