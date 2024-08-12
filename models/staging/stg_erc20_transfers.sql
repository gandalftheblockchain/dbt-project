{{ config(materialized='view') }}

with source_data as (

    select
        unique_id
        , block_num
        , tx_hash
        , tx_from
        , tx_to
        , value_decimal
        , asset
        , value
        , contract_address
        , decimal
        , block_timestamp
    from {{ source('erc20', 'erc20_transfers') }}

)

select *
from source_data