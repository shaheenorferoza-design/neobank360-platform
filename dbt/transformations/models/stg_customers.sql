{{ config(
    materialized='table'
) }}


SELECT

    CUSTOMER_ID       AS customer_id,
    FIRST_NAME        AS first_name,
    LAST_NAME         AS last_name,
    EMAIL             AS email,
    PHONE             AS phone,
    CITY              AS city,
    CREATED_TS        AS created_ts

FROM NEOBANK360.RAW.CUSTOMERS