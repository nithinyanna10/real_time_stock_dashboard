# app.py
import streamlit as st
import pandas as pd

from src.data_fetcher import fetch_intraday
from src.indicators import add_sma, add_ema, add_macd
from src.predictor import train_predictor
from src.sentiment import analyze_headlines
from src.summarizer import generate_summary
from src.logger import log_timing
import sys
import torch

# Workaround for Streamlit trying to inspect torch.classes
if "torch.classes" in sys.modules:
    del sys.modules["torch.classes"]

st.set_page_config(page_title="📈 Real-time Stock Dashboard", layout="wide")

st.title("📈 Real-time Stock Analytics Dashboard")
st.markdown("Get real-time stock data with moving averages, predictions, and sentiment insights.")

# Sidebar
st.sidebar.header("⚙️ Settings")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
interval = st.sidebar.selectbox("Interval", ["1min", "5min", "15min", "30min", "60min"])
sma_window = st.sidebar.slider("SMA Window", 5, 50, 20)
ema_window = st.sidebar.slider("EMA Window", 5, 50, 20)

@log_timing("Total Fetch + Feature Time")
def load_data():
    df = fetch_intraday(symbol, interval)
    df = add_sma(df, sma_window)
    df = add_ema(df, ema_window)
    df = add_macd(df)
    return df

st.spinner("Loading data...")
df = load_data()

# Display Data
st.subheader(f"🔍 Stock Data for {symbol}")
st.line_chart(df[["close", f"SMA_{sma_window}", f"EMA_{ema_window}"]])

# Display MACD
st.subheader("📊 MACD Indicator")
st.line_chart(df[["MACD", "Signal"]])

# Prediction
st.subheader("🤖 ML Prediction")
predicted_price = train_predictor(df)
st.metric(label="Predicted Next Close", value=f"${predicted_price}")

# Export
st.download_button("📤 Export Data as CSV", data=df.to_csv().encode(), file_name=f"{symbol}_data.csv")

# Sentiment Analysis (Simulated headlines)
st.subheader("📰 News Sentiment (Sample)")
sample_headlines = [
    f"{symbol} stock climbs after earnings beat expectations",
    f"Analysts concerned over {symbol}'s slowing growth",
]
sentiments = analyze_headlines(sample_headlines)
for i, s in enumerate(sentiments):
    st.write(f"- {sample_headlines[i]} → **{s['label']}** ({round(s['score'], 2)})")

# Summary
st.subheader("🧠 Executive Summary")
text_to_summarize = (
    f"{symbol} stock shows a {sma_window}-day SMA trend of {round(df[f'SMA_{sma_window}'].iloc[-1],2)}, "
    f"an EMA of {round(df[f'EMA_{ema_window}'].iloc[-1],2)}, and a predicted next price of ${predicted_price}. "
    f"Recent news headlines indicate sentiment leaning toward {sentiments[0]['label']}."
)
summary = generate_summary(text_to_summarize)
st.info(summary)

# Footer
st.caption("🚀 Built with Alpha Vantage, Streamlit, and 💡 AI-driven analysis.")
