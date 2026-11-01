-- Day 2 in dbt: dedupe + idempotent incremental model.
-- unique_key='order_id' makes dbt MERGE instead of append, so rerunning never double counts.
{{ config(materialized='incremental', unique_key='order_id', incremental_strategy='merge') }}

select order_id, customer_id, amount, event_time, received_at
from {{ ref('raw_messages') }}
qualify row_number() over (partition by order_id order by received_at) = 1
