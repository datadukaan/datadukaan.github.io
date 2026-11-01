-- Orders that had ARRIVED by the time the job runs (simulates data landing over time).
select *
from {{ ref('raw_orders') }}
where ingest_time <= timestamp '{{ var("as_of") }}'
