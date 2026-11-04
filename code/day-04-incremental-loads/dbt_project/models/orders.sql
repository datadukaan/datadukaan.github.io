-- Day 4 in dbt: incremental model = high-water mark + lookback + merge on order_id.
-- {{ this }} is the table built by the previous run; its max(updated_at) is the bookmark.
{{ config(materialized='incremental', unique_key='order_id', incremental_strategy='delete+insert') }}

select order_id, amount, created_at, updated_at
from {{ ref('source_night' ~ var('night')) }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }}) - interval {{ var('lookback_hours') }} hour
{% endif %}
