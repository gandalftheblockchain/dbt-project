{{ config(materialized='view') }}

with source_data as (

    select
        id
        , token_id
        , token_symbol
        , token_name
        , blockchain
        , contract_address
        , usd_price
        , timestamp_price
    from {{ source('coingecko', 'token_prices') }}

)

select *
from source_data

