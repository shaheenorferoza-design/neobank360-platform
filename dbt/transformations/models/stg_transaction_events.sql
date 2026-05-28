{{ config(
    materialized='incremental',
    unique_key='event_id'
) }}

with source_data as (

    select *
    from {{ source('raw', 'raw_transaction_events') }}

),

parsed as (

    select
        event_payload:event_id::string as event_id,
        event_payload:customer_id::string as customer_id,
        event_payload:account_id::string as account_id,
        upper(event_payload:event_type::string) as event_type,
        round(event_payload:amount::number, 2) as amount,
        upper(event_payload:currency::string) as currency,
        upper(event_payload:merchant.name::string) as merchant_name,
        upper(event_payload:merchant.category::string) as merchant_category,
        upper(event_payload:device.device_id::string) as device_id,
        event_payload:device.ip_address::string as ip_address,
        initcap(event_payload:device.location::string) as device_location,
        event_payload:txn_ts::timestamp_ntz as txn_ts,
        ingestion_ts,
        source_file_name,
        source_row_number,
        current_timestamp() as warehouse_insert_ts

    from source_data

    {% if is_incremental() %}
    where ingestion_ts > (
        select coalesce(max(ingestion_ts), '1900-01-01')
        from {{ this }}
    )
    {% endif %}

),

valid_records as (

    select *
    from parsed
    where event_id is not null

),

deduplicated as (

    select *
    from valid_records
    qualify row_number() over (
        partition by event_id
        order by ingestion_ts desc
    ) = 1

)

select *
from deduplicated