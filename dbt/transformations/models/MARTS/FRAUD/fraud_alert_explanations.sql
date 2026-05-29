{{ config(
    schema='datamart',
    materialized='incremental',
    unique_key='event_id'
) }}

with fraud_alerts as (

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
        txn_count_5_min,
        txn_amount_5_min,
        high_velocity_flag,
        high_value_burst_flag,
        fraud_risk_level,
        warehouse_insert_ts

    from {{ ref('fct_high_velocity_transactions') }}

    {% if is_incremental() %}
        where warehouse_insert_ts >
        (
            select coalesce(max(created_ts), '1900-01-01')
            from {{ this }}
        )
    {% endif %}

),

explanations as (

    select
        event_id,
        customer_id,
        account_id,
        fraud_risk_level,

        case
            when high_velocity_flag = 'Y'
             and high_value_burst_flag = 'Y'
                then 'HIGH_VELOCITY_AND_HIGH_VALUE_BURST'

            when high_velocity_flag = 'Y'
                then 'HIGH_VELOCITY_TRANSACTIONS'

            when high_value_burst_flag = 'Y'
                then 'HIGH_VALUE_BURST'

            else 'UNKNOWN'
        end as rule_triggered,

        concat(
            'Customer ', customer_id,
            ' triggered a ', fraud_risk_level,
            ' fraud alert because ',
            txn_count_5_min,
            ' transactions occurred within a 5-minute window with cumulative amount of INR ',
            txn_amount_5_min,
            '. The latest transaction was a ',
            event_type,
            ' of INR ',
            amount,
            ' at merchant ',
            coalesce(merchant_name, 'UNKNOWN'),
            ' from device ',
            coalesce(device_id, 'UNKNOWN'),
            ' in ',
            coalesce(device_location, 'UNKNOWN'),
            '.'
        ) as genai_explanation,

        case
            when fraud_risk_level = 'HIGH'
                then 'Recommend immediate fraud analyst review and temporary transaction hold.'

            when fraud_risk_level = 'MEDIUM'
                then 'Recommend manual review before escalation.'

            else 'Log for monitoring.'
        end as recommended_action,

        current_timestamp() as created_ts

    from fraud_alerts

)

select *
from explanations