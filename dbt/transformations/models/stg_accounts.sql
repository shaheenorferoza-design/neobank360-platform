{{ config(
    materialized='table'
) }}

with source_data as (

    select *

    from {{ source('raw', 'accounts') }}

),

standardized as (

    select

        upper(trim(account_id)) as account_id,

        upper(trim(customer_id)) as customer_id,

        case
            when upper(coalesce(account_type,'UNKNOWN')) in ('SAV', 'SAVINGS')
                then 'SAVINGS'

            when upper(coalesce(account_type,'UNKNOWN')) in ('CURR', 'CURRENT')
                then 'CURRENT'

            when upper(coalesce(account_type,'UNKNOWN')) in ('LOAN')
                then 'LOAN'

            else 'OTHER'
        end as account_type,

        case
            when upper(status) in ('A', 'ACTIVE')
                then 'ACTIVE'

            when upper(status) in ('D', 'DORMANT')
                then 'DORMANT'

            when upper(status) in ('B', 'BLOCKED')
                then 'BLOCKED'

            when upper(status) in ('C', 'CLOSED')
                then 'CLOSED'

            else 'UNKNOWN'
        end as account_status,
       'CORE_BANKING' as source_system,
        round(coalesce(balance::number, 0), 2)
            as current_balance,
            current_date() as business_date,

        
        current_timestamp()
            as warehouse_insert_ts

    from source_data

)

select *
from standardized