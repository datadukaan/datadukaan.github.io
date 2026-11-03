#!/usr/bin/env bash
# Replays two runs: at 09:02:45 only the 9:02 change (seq 2) has arrived;
# by the end of the day the old 9:00 order (seq 1) and the other orders arrive too.
set -e
cd "$(dirname "$0")"
rm -f day03.duckdb
dbt seed --profiles-dir . -q
show() { python3 -c "import duckdb; print(duckdb.connect('day03.duckdb').sql('select order_id, seq, amount from orders_current order by 1'))"; }
dbt run --profiles-dir . -q --full-refresh --vars '{received_until: "2026-11-03 09:02:45"}'
echo "Run at 09:02:45 (only the change has arrived):"; show
dbt run --profiles-dir . -q --vars '{received_until: "2026-11-03 23:59:59"}'
echo "Run at end of day (old order arrived late, ignored):"; show
