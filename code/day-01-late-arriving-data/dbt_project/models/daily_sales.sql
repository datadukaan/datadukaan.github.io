-- Day 1 - Fix 3 in dbt: an incremental model with a lookback window.
-- Every run recounts the last N days by EVENT time and merges them in,
-- so late orders land on the day they actually happened.
{{ config(materialized='incremental', unique_key='sale_date', incremental_strategy='delete+insert') }}

select
    cast(event_time as date) as sale_date,
    sum(amount)              as total,
    count(*)                 as orders
from {{ ref('arrived_orders') }}
{% if is_incremental() %}
where cast(event_time as date) >= cast(timestamp '{{ var("as_of") }}' as date) - interval {{ var('lookback_days') - 1 }} day
{% endif %}
group by 1
