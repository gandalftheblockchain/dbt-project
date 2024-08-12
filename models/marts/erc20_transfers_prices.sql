{{ config(materialized='view') }}

with prices as (

    select *
    from {{ ref('stg_token_prices') }}

)

, transfers as (

    select *
    from {{ ref('stg_erc20_transfers') }}
    
)

select
    unique_id
    , block_num
    , tx_hash
    , tx_from
    , tx_to
    , value_decimal
    , value_decimal * usd_price as value_usd
    , asset
    , value
    , transfers.contract_address
    , decimal
    , block_timestamp
from transfers
left join prices
on date_trunc('hour', transfers.block_timestamp) = date_trunc('hour', prices.timestamp_price)
and transfers.contract_address = prices.contract_address