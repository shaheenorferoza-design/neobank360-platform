{{ config(
    schema='datamart',
    materialized='incremental',
    unique_key='transaction_id'
) }}

with transactions as (

    select
        transaction_id,
        customer_id,
        transaction_type,
        transaction_amount,
        transaction_ts,
        warehouse_insert_ts

    from {{ ref('stg_transactions') }}

    {% if is_incremental() %}

        where transaction_ts >
        (
            select coalesce(max(transaction_ts), '1900-01-01')
            from {{ this }}
        )

    {% endif %}

),

customers as (

    select
        customer_key,
        customer_id

    from {{ ref('dim_customer') }}

),

final as (

    select
        md5(t.transaction_id) as transaction_key,

        t.transaction_id,

        c.customer_key,

        t.customer_id,

        t.transaction_type,

        t.transaction_amount,

        t.transaction_ts,

        current_timestamp() as warehouse_insert_ts

    from transactions t

    left join customers c
        on t.customer_id = c.customer_id

)

select *
from final