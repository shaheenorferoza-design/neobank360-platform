{{ config(
    schema='datamart',
    materialized='table'
) }}

with customers as (

    select
        customer_id,
        first_name,
        last_name,
        email,
        phone,
        city,
        created_ts

    from {{ ref('stg_customers') }}

),

final as (

    select
        md5(customer_id) as customer_key,

        customer_id,

        initcap(trim(first_name)) as first_name,
        initcap(trim(last_name)) as last_name,

        lower(trim(email)) as email,
        trim(phone) as phone,

        initcap(trim(city)) as city,

        created_ts as customer_since_date,

        'Y' as current_flag,

        current_timestamp() as warehouse_insert_ts

    from customers

    where customer_id is not null

)

select *
from final