# src/indicators.py
import pandas as pd

def add_sma(df, window=20):
    df[f"SMA_{window}"] = df['close'].rolling(window=window).mean()
    return df

def add_ema(df, window=20):
    df[f"EMA_{window}"] = df['close'].ewm(span=window, adjust=False).mean()
    return df

def add_macd(df):
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

# Test
if __name__ == "__main__":
    from data_fetcher import fetch_intraday
    df = fetch_intraday("AAPL")
    df = add_sma(df)
    df = add_ema(df)
    df = add_macd(df)
    print(df.tail())
