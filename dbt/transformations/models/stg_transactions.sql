{{ config(
    materialized='incremental',
    unique_key='transaction_id'
) }}

with source_data as (

    select *

    from {{ source('raw', 'transactions') }}

),

deduplicated as (


    select *

    from (

        select

            *,

            row_number() over (
                partition by transaction_id
                order by load_ts desc
            ) as rn

        from source_data

    )

    where rn = 1

),

standardized as (

    select

        upper(trim(transaction_id))
            as transaction_id,

       upper(trim(customer_id))
            as customer_id,

        case

            when upper(transaction_type) in ('UPI')
                then 'UPI'

            when upper(transaction_type) in ('ATM', 'ATM_WITHDRAWAL')
                then 'ATM_WITHDRAWAL'

            when upper(transaction_type) in ('POS', 'CARD')
                then 'CARD_PAYMENT'

            when upper(transaction_type) in ('NETBANKING')
                then 'NETBANKING'

            else 'OTHER'

        end as transaction_type,

        round(amount, 2)
            as transaction_amount,
        load_ts as transaction_ts,

         current_timestamp()
            as warehouse_insert_ts

    from deduplicated

)

select *
from standardized

{% if is_incremental() %}

where transaction_ts >
(
   select coalesce(max(transaction_ts), '1900-01-01')
from {{ this }}
)

{% endif %}