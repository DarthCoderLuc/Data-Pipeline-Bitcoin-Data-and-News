import requests
import datetime as dt
from dotenv import load_dotenv
import os
import pandas as pd

def get_crypto_data(symbol, market):
    # Explicitly load the .env file
    load_dotenv()

    # Load environment variables from the .env file
    api_key = os.getenv('api_key_alpha')
    database_url = os.getenv('Database_URL_alpha')
    function = 'DIGITAL_CURRENCY_DAILY'

    url = f"{database_url}function={function}&symbol={symbol}&market={market}&apikey={api_key}"

    response = requests.get(url).json()

    # Check if the expected key is in the response
    if 'Time Series (Digital Currency Daily)' not in response:
        print(response)
        return None

    # Extract time series data
    time_series = response['Time Series (Digital Currency Daily)']

    # Create a DataFrame
    data = pd.DataFrame.from_dict(time_series, orient='index')

    # Rename the columns
    data.columns = ['open', 'high', 'low', 'close', 'volume']

    # Convert columns to appropriate data types
    data = data.astype(float)

    # Convert index to datetime
    data.index = pd.to_datetime(data.index)

    #data = data.reset_index()

    # Rename the date column
    #data = data.rename(columns={'index': 'date'})

    # Set the date column as the index
    #data = data.set_index()

    # If the date column is not in datetime format, you may need to convert it
    #data.index = pd.to_datetime(data.index)

    data = data.sort_index()

    return data

# Example usage
symbol = 'BTC'
market = 'USD'
data = get_crypto_data(symbol, market)

if data is not None:
    print(data)
else:
    print("Data could not be retrieved.")
