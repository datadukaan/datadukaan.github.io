-- Day 3 in dbt: latest version wins, even when an old message arrives in a later run.
-- Each run takes the newly received messages, puts them next to the rows already in
-- the table, and keeps the highest seq per order. A late seq 1 can never replace seq 2.
{{ config(materialized='incremental', unique_key='order_id', incremental_strategy='delete+insert') }}

with arrived as (
    select order_id, seq, amount, event_time, received_at
    from {{ ref('raw_order_messages') }}
    where received_at <= timestamp '{{ var("received_until") }}'
    {% if is_incremental() %}
      and received_at > (select max(received_at) from {{ this }})
    {% endif %}
),
candidates as (
    select * from arrived
    {% if is_incremental() %}
    union all
    select order_id, seq, amount, event_time, received_at
    from {{ this }}
    where order_id in (select order_id from arrived)
    {% endif %}
)
select order_id, seq, amount, event_time, received_at
from candidates
qualify row_number() over (partition by order_id order by seq desc) = 1
