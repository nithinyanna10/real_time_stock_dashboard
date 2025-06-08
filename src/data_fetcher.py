# src/data_fetcher.py
import requests
import pandas as pd
import time

from config import ALPHA_VANTAGE_API_KEY

def fetch_intraday(symbol, interval="5min"):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(url, params=params)
    data = response.json()

    key = f"Time Series ({interval})"
    if key not in data:
        raise ValueError("Invalid API response or limit reached")

    df = pd.DataFrame.from_dict(data[key], orient='index').sort_index()
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df

# Test
if __name__ == "__main__":
    df = fetch_intraday("AAPL")
    print(df.head())
