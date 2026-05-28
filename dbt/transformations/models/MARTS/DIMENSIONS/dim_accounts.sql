{{ config(
    schema='datamart',
    materialized='table'
) }}

with accounts as (

    select
        account_id,
        customer_id,
        account_type,
        account_status,
        current_balance,
        warehouse_insert_ts

    from {{ ref('stg_accounts') }}

),

final as (

    select
        md5(account_id) as account_key,

        account_id,
        customer_id,

        account_type,
        account_status,

        current_balance,

        'Y' as current_flag,

        current_timestamp() as warehouse_insert_ts

    from accounts

    where account_id is not null

)

select *
from final