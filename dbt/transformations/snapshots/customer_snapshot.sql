{% snapshot customer_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',

        strategy='timestamp',
        updated_at='created_ts'
    )
}}

select
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    created_ts

from {{ ref('stg_customers') }}

{% endsnapshot %}