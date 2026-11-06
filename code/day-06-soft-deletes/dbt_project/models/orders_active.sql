-- Day 6 in dbt: the filtered view every report should use.
{{ config(materialized='view') }}

select order_id, amount, created_at, updated_at
from {{ ref('orders') }}
where not is_deleted
