# app.py
import streamlit as st
import pandas as pd
import sys
import torch

from src.data_fetcher import fetch_intraday
from src.indicators import add_sma, add_ema, add_macd
from src.predictor import train_predictor
from src.sentiment import analyze_headlines
from src.summarizer import generate_summary
from src.logger import log_timing
from src.trend_forecast import fetch_stock_data, train_forecast_model, get_forecast_plot
from src.impact_scorer import predict_impact
from src.report_generator import export_summary_to_word, export_plot_to_pdf

# Torch Streamlit watcher workaround
if "torch.classes" in sys.modules:
    del sys.modules["torch.classes"]

# Page config
st.set_page_config(page_title="📈 Real-time Stock Dashboard", layout="wide")
st.title("📈 Real-time Stock Analytics Dashboard")
st.markdown("Get real-time stock data with moving averages, predictions, forecasts, and sentiment insights.")

# Define Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Realtime Indicators", 
    "📰 News & Sentiment", 
    "📈 Historical Trends", 
    "🧠 Executive Summary"
])

# ----------------------------- TAB 1 -----------------------------
with tab1:
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

    with st.spinner("Loading stock data..."):
        df = load_data()

    st.subheader(f"📈 Price & Averages: {symbol}")
    st.line_chart(df[["close", f"SMA_{sma_window}", f"EMA_{ema_window}"]])

    st.subheader("📊 MACD Indicator")
    st.line_chart(df[["MACD", "Signal"]])

    st.subheader("🤖 ML Prediction")
    predicted_price = train_predictor(df)
    st.metric(label="Predicted Next Close", value=f"${predicted_price}")

    st.download_button("📤 Export Data as CSV", data=df.to_csv().encode(), file_name=f"{symbol}_data.csv")

# ----------------------------- TAB 2 -----------------------------
with tab2:
    st.subheader("📰 News Sentiment & Impact")
    sample_headlines = [
        f"{symbol} stock climbs after earnings beat expectations",
        f"Analysts concerned over {symbol}'s slowing growth",
    ]
    sentiments = analyze_headlines(sample_headlines)
    for i, s in enumerate(sentiments):
        headline = sample_headlines[i]
        sentiment = s['label']
        sentiment_emoji = "🟢" if sentiment == "POSITIVE" else "🔴" if sentiment == "NEGATIVE" else "⚪"
        impact = predict_impact(headline)
        st.write(f"{sentiment_emoji} **{headline}** → *{sentiment}* | 💥 **Impact: {impact}**")

# ----------------------------- TAB 3 -----------------------------
with tab3:
    st.subheader("📈 Stock Trend Forecast")
    forecast_symbol = st.selectbox("Choose a stock symbol", ["AAPL", "TSLA", "GOOGL", "MSFT"])
    hist_df = fetch_stock_data(forecast_symbol)
    forecast = train_forecast_model(hist_df)
    fig = get_forecast_plot(hist_df, forecast)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------- TAB 4 -----------------------------
with tab4:
    st.subheader("🧠 Executive Summary")
    text_to_summarize = (
        f"{symbol} stock shows a {sma_window}-day SMA trend of {round(df[f'SMA_{sma_window}'].iloc[-1], 2)}, "
        f"an EMA of {round(df[f'EMA_{ema_window}'].iloc[-1], 2)}, and a predicted next price of ${predicted_price}. "
        f"Recent news headlines indicate sentiment leaning toward {sentiments[0]['label']}."
    )
    summary = generate_summary(text_to_summarize)
    st.info(summary)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Export Summary to Word"):
            doc_path = export_summary_to_word(summary)
            with open(doc_path, "rb") as f:
                st.download_button("📥 Download Word Doc", f, file_name="summary.docx")

    with col2:
        if st.button("📊 Export Chart to PDF"):
            pdf_path = export_plot_to_pdf(df)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Chart PDF", f, file_name="chart.pdf")

# Footer
st.caption("🚀 Built with Alpha Vantage, Streamlit, Prophet, and 💡 AI-powered analytics.")
