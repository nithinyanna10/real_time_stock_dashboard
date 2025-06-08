# src/trend_forecast.py

import yfinance as yf
import pandas as pd
from prophet import Prophet

def fetch_stock_data(symbol="AAPL", period="6mo"):
    df = yf.download(symbol, period=period)
    df = df.reset_index()[["Date", "Close"]]
    df.columns = ["ds", "y"]
    return df

def train_forecast_model(df):
    model = Prophet(daily_seasonality=True)
    model.fit(df)
    future = model.make_future_dataframe(periods=1)  # 1-day prediction
    forecast = model.predict(future)
    return forecast

def get_forecast_plot(df, forecast):
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="Actual"))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name="Predicted"))
    fig.update_layout(title="📈 1-Day Stock Price Forecast", xaxis_title="Date", yaxis_title="Price")
    return fig
