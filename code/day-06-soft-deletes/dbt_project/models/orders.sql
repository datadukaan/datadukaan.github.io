-- Day 6 in dbt: the copy keeps every row, including soft-deleted ones.
{{ config(materialized='incremental', unique_key='order_id', incremental_strategy='delete+insert') }}

select order_id, amount, created_at, updated_at, is_deleted
from {{ ref('orders_night' ~ var('night')) }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
