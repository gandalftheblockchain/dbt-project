-- Create a warehouse for data transformation tasks
create warehouse transforming;

-- Create databases to organize data
create database raw;         -- Database for storing raw, unprocessed data
create database analytics;   -- Database for storing processed and analytics-ready data

-- Create schemas to categorize data within the raw database
create schema raw.coingecko; -- Schema for storing CoinGecko API data, like cryptocurrency token prices
create schema raw.erc20;     -- Schema for storing ERC20 token transfer data

-- Create a table for storing CoinGecko token prices
create or replace TABLE raw.COINGECKO.TOKEN_PRICES (
	ID VARCHAR(16777216) NOT NULL,            -- Unique identifier for each record, used as the primary key
	TOKEN_ID VARCHAR(16777216),               -- ID of the cryptocurrency token
	TOKEN_SYMBOL VARCHAR(16777216),           -- Symbol of the token (e.g., ETH, BTC)
	TOKEN_NAME VARCHAR(16777216),             -- Full name of the token
    BLOCKCHAIN VARCHAR,                       -- Blockchain where the token resides (e.g., Ethereum)
    CONTRACT_ADDRESS VARCHAR,                 -- Smart contract address of the token
	USD_PRICE DECIMAL(38,6),                  -- Price of the token in USD, stored with high precision
	TIMESTAMP_PRICE TIMESTAMP_NTZ(9),         -- Timestamp when the price was recorded, without timezone
	primary key (ID)                          -- Define ID as the primary key to ensure unique records
);

-- Create a table for storing ERC20 token transfers
create or replace TABLE raw.erc20.ERC20_TRANSFERS (
	UNIQUE_ID VARCHAR(16777216) NOT NULL,     -- Unique identifier for each transfer record, used as the primary key
	BLOCK_NUM VARCHAR(16777216),              -- Block number in the blockchain where the transaction occurred
	TX_HASH VARCHAR(16777216),                -- Unique transaction hash identifying the transaction
	TX_FROM VARCHAR(16777216),                -- Address sending the tokens
	TX_TO VARCHAR(16777216),                  -- Address receiving the tokens
	VALUE_DECIMAL DECIMAL(38,6),              -- Value of tokens transferred, stored with high precision
	ASSET VARCHAR(16777216),                  -- Asset (token) being transferred
	CATEGORY VARCHAR(16777216),               -- Category of the transaction (e.g., transfer type)
    VALUE VARCHAR,                            -- Value transferred, stored as a string
    CONTRACT_ADDRESS VARCHAR,                 -- Contract address governing the token
    DECIMAL VARCHAR,                          -- Number of decimal places for the token's denomination
	BLOCK_TIMESTAMP TIMESTAMP_NTZ(9),         -- Timestamp of the block when the transaction was recorded, without timezone
	primary key (UNIQUE_ID)                   -- Define UNIQUE_ID as the primary key to ensure unique records
);