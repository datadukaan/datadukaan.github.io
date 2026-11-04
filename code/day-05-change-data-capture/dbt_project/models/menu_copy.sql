-- Day 5 in dbt: rebuild the current copy from snapshot + change log.
-- Each key takes its latest event by log position; deletes drop the row.
{{ config(materialized='table') }}

with events as (
    select item_id, item, price, op, lsn
    from {{ ref('change_log') }}
    where lsn <= {{ var('up_to_lsn') }}
    union all
    select item_id, item, price, 'snapshot' as op, 0 as lsn    -- the midnight copy counts as position 0
    from {{ ref('menu_snapshot') }}
),
latest as (
    select * from events
    qualify row_number() over (partition by item_id order by lsn desc) = 1
)
select item_id, item, price
from latest
where op != 'd'
