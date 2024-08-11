# ERC20 Transfers and Token Prices DBT Project

## Overview

This dbt project integrates ERC20 token transfer data with token price information to provide a comprehensive view of token transactions and their USD value. The project includes the creation of Snowflake databases showing DDL commands, Python scripts for data extraction, and dbt models for data transformation and analysis.

## Project Highlights

- **Database Creation:** Set up Snowflake databases to store on-chain data.
- **Data Population Scripts:** Developed Python scripts to populate token prices and ERC20 transfers tables from Coingecko and Alchemy APIs.
- **dbt Models:**
  - **Staging Models:** Created staging models `stg_token_prices` and `stg_erc20_transfers` from raw dataset sources, including documentation and testing.
  - **Final Model:** Created the `erc20_transfers_prices` model to link token prices with ERC20 transfer data.

## Screenshots

- **Successful Runs:**  
  ![Successful Runs](https://github.com/user-attachments/assets/01c8d1a9-7a42-4cdc-aee1-939e35e5d1f2)

- **Output in Snowflake:**  
  ![Snowflake Output](https://github.com/user-attachments/assets/8fa919c6-1d0c-4abb-8988-c4ffea60515a)

## DDL Commands

- [DDL Commands File](https://github.com/gandalftheblockchain/dbt-project/blob/6532f3f5e565fe66cb2067ac040fc3cbf90abcd2/ddl_commants.sql)

## Python Scripts

- **Coingecko Token Prices:**  
  [token_prices.py](https://github.com/gandalftheblockchain/dbt-project/blob/6532f3f5e565fe66cb2067ac040fc3cbf90abcd2/scripts/token_prices.py)  
  Tracks token prices across multiple blockchains, handling different contract addresses and decimal places for the same token. Provides hourly snapshots for accurate and up-to-date price information.

- **Alchemy ERC20 Transfers:**  
  [erc20_transfers.py](https://github.com/gandalftheblockchain/dbt-project/blob/6532f3f5e565fe66cb2067ac040fc3cbf90abcd2/scripts/erc20_transfers.py)  
  Pulls the last 1,000 ERC20 transfers to demonstrate accurate joining with hourly price data. Ensures proper alignment by joining on token contract addresses and truncated timestamps.

## API Documentation

- [Alchemy Asset Transfers API](https://docs.alchemy.com/reference/alchemy-getassettransfers)
- [CoinGecko Market Chart API](https://docs.coingecko.com/reference/coins-id-market-chart-range)

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/gandalftheblockchain/dbt-project.git
