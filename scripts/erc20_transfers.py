import pandas as pd
import requests
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas
from datetime import datetime
import os

# Retrieve the API key from environment variables
api_key = env_var('DBT_ENV_SECRET_COINGECKO_API')

# Define the API endpoint and parameters for the initial request
url = "https://api.coingecko.com/api/v3/coins/list"
params = {
    'include_platform': 'true',  # Include platform information in the response
    'status': 'active'           # Filter for active tokens only
}
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": api_key  # Pass the API key in the headers for authentication
}

# Make the initial API request to retrieve the list of tokens
response = requests.get(url, params=params, headers=headers)
tokenlist = pd.DataFrame(response.json())  # Convert the JSON response to a pandas DataFrame

# Explode the 'platforms' column into separate rows for each platform
df_exploded = tokenlist['platforms'].apply(pd.Series).stack().reset_index(level=1)
df_exploded.columns = ['blockchain', 'contract_address']  # Rename the exploded columns

# Merge the exploded platforms back with the original token list
tokenlist_cleaned = tokenlist.join(df_exploded, how='left')
tokenlist_cleaned.drop(columns=['platforms'], inplace=True)  # Drop the original 'platforms' column

# Filter tokens to include only specific tokens of interest
tokenlist_selected = tokenlist_cleaned[tokenlist_cleaned.id.isin(['weth', 'ethereum', 'bitcoin'])]

# Initialize an empty DataFrame to store final results
df_final = pd.DataFrame()

# Loop through each selected token and retrieve market data
for _, token_row in tokenlist_selected.iterrows():
    # Define the API endpoint for the market data of the current token
    url = f'https://api.coingecko.com/api/v3/coins/{token_row["id"]}/market_chart'
    params = {
        'vs_currency': 'usd',  # Currency for price data
        'days': '50'           # Number of days of data to retrieve
    }

    # Make the API request for market data
    res = requests.get(url, params=params, headers=headers)

    # If the request is successful, process the response data
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        list_price = [row[0] for _, row in df.iterrows()]  # Extract price data
        df_price = pd.DataFrame(list_price, columns=['TIMESTAMP_PRICE', 'USD_PRICE'])

        # Convert the timestamp to a readable datetime format
        df_price['TIMESTAMP_PRICE'] = df_price['TIMESTAMP_PRICE'].apply(
            lambda x: datetime.utcfromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S')
        )

        # Add additional token information to the DataFrame
        df_price['TOKEN_ID'] = token_row['id']
        df_price['TOKEN_NAME'] = token_row['name']
        df_price['TOKEN_SYMBOL'] = token_row['symbol']
        df_price['BLOCKCHAIN'] = token_row['blockchain']
        df_price['CONTRACT_ADDRESS'] = token_row['contract_address']

        # Append the processed data to the final DataFrame
        df_final = pd.concat([df_final, df_price])

# Add a unique identifier column to the final DataFrame
df_final['ID'] = df_final.reset_index().index

# Reorder the columns in the final DataFrame
df_final = df_final[['ID', 'TOKEN_ID', 'TOKEN_SYMBOL', 'TOKEN_NAME', 'BLOCKCHAIN', 'CONTRACT_ADDRESS', 'USD_PRICE', 'TIMESTAMP_PRICE']]

# Retrieve Snowflake credentials from environment variables
conn = snow.connect(
    user=env_var('DBT_ENV_SECRET_SF_USER'),
    password=env_var('DBT_ENV_SECRET_SF_PASSWORD'),
    account=env_var('DBT_ENV_SECRET_SF_ACCOUNT'),
    warehouse=env_var('DBT_WAREHOUSE'),
    database=env_var('DBT_DATABASE'),
    schema=env_var('DBT_CG_SCHEMA')
)

# Write the final DataFrame to the Snowflake table
success, nchunks, nrows, _ = write_pandas(conn, df_final, "TOKEN_PRICES", auto_create_table=True)

# Print the results of the write operation
print(success, nchunks, nrows)