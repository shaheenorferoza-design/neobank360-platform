{{ config(
    schema='datamart',
    materialized='incremental',
    unique_key='event_id'
) }}

with events as (

    select
        event_id,
        customer_id,
        account_id,
        event_type,
        amount,
        currency,
        merchant_name,
        merchant_category,
        device_id,
        ip_address,
        device_location,
        txn_ts,
        ingestion_ts,
        source_file_name

    from {{ ref('stg_transaction_events') }}

    where event_type in (
        'UPI_PAYMENT',
        'CARD_SWIPE',
        'ATM_WITHDRAWAL',
        'NETBANKING_TRANSFER'
    )

),

deduplicated_events as (

    select *

    from (

        select
            *,
            row_number() over (
                partition by event_id
                order by ingestion_ts desc
            ) as rn

        from events

    )

    where rn = 1

),

velocity_calc as (

    select
        event_id,
        customer_id,
        account_id,
        event_type,
        amount,
        merchant_name,
        device_id,
        device_location,
        txn_ts,
        ingestion_ts,
        source_file_name,

        count(*) over (
            partition by customer_id
            order by txn_ts
            range between interval '5 minutes' preceding and current row
        ) as txn_count_5_min,

        sum(amount) over (
            partition by customer_id
            order by txn_ts
            range between interval '5 minutes' preceding and current row
        ) as txn_amount_5_min

    from deduplicated_events

),

fraud_flags as (

    select
        *,

        case
            when txn_count_5_min >= 5 then 'Y'
            else 'N'
        end as high_velocity_flag,

        case
            when txn_amount_5_min >= 50000 then 'Y'
            else 'N'
        end as high_value_burst_flag,

        case
            when txn_count_5_min >= 5
              or txn_amount_5_min >= 50000
                then 'HIGH'
            when txn_count_5_min >= 3
                then 'MEDIUM'
            else 'LOW'
        end as fraud_risk_level,

        current_timestamp() as warehouse_insert_ts

    from velocity_calc

)

select *
from fraud_flags

where high_velocity_flag = 'Y'
   or high_value_burst_flag = 'Y'