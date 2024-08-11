import pandas as pd
import requests
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas
from datetime import datetime

# Retrieve the Alchemy API key from environment variables
api_key = env_var('DBT_ENV_SECRET_ALCHEMY_API')

# Define the Alchemy API endpoint
url = f'https://eth-mainnet.g.alchemy.com/v2/{api_key}'

# Define the payload for the API request to get ERC20 asset transfers
payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [
        {
            "fromBlock": "0x0",               # Start from the first block
            "toBlock": "latest",              # Up to the latest block
            "order": "desc",                  # Order results in descending order
            "withMetadata": True,             # Include metadata
            "excludeZeroValue": True,         # Exclude transfers with zero value
            "maxCount": "0x3e8",              # Limit the number of results (1000 in hex)
            "category": ["erc20"]             # Filter by ERC20 token transfers
        }
    ]
}

# Define the headers for the API request
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

# Make the API request and convert the response to a DataFrame
response = requests.post(url, json=payload, headers=headers)
df_alc = pd.DataFrame(response.json())

# Extract the 'result' field from the response into a DataFrame
df_api = pd.DataFrame.from_dict(df_alc['result'][0])

# Flatten the 'metadata' column into separate columns
df_erc20 = pd.concat([df_api.drop(['metadata'], axis=1), df_api['metadata'].apply(pd.Series)], axis=1)
df_erc20.rename(columns={'value': 'valueDecimal'}, inplace=True)

# Flatten the 'rawContract' column into separate columns
df_erc20 = pd.concat([df_erc20.drop(['rawContract'], axis=1), df_erc20['rawContract'].apply(pd.Series)], axis=1)

# Convert camelCase column names to snake_case and then to uppercase
df_erc20.columns = df_erc20.columns.str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True).str.upper()
df_erc20.rename(columns={'HASH': 'TX_HASH', 'FROM': 'TX_FROM', 'TO': 'TX_TO', 'ADDRESS': 'CONTRACT_ADDRESS'}, inplace=True)

# Reorder columns to match the desired output format
df_erc20 = df_erc20[['UNIQUE_ID', 'BLOCK_NUM', 'TX_HASH', 'TX_FROM', 'TX_TO', 'VALUE_DECIMAL', 
                     'ASSET', 'VALUE', 'CONTRACT_ADDRESS', 'DECIMAL', 'BLOCK_TIMESTAMP']]

# Connect to Snowflake using credentials stored in environment variables
conn = snow.connect(
    user=env_var('DBT_ENV_SECRET_SF_USER'),
    password=env_var('DBT_ENV_SECRET_SF_PASSWORD'),
    account=env_var('DBT_ENV_SECRET_SF_ACCOUNT'),
    warehouse=env_var('DBT_WAREHOUSE'),
    database=env_var('DBT_DATABASE'),
    schema=env_var('DBT_ALCHEMY_SCHEMA')
)

# Write the ERC20 transfer data to the Snowflake table 'ERC20_TRANSFERS'
success, nchunks, nrows, _ = write_pandas(conn, df_erc20, "ERC20_TRANSFERS", auto_create_table=True)

#  Print the results of the write operation
print(success, nchunks, nrows)