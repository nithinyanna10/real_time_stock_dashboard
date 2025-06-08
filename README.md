
# 📈 Real-time Stock Analytics Dashboard

This project is a **Streamlit-powered dashboard** that provides **real-time stock insights**, **AI-generated summaries**, and **financial forecasts** using machine learning and NLP. It integrates technical indicators, trend prediction, sentiment analysis, impact scoring, and automated report generation.

---

## 🚀 Features

### 📊 Realtime Indicators
- Live intraday stock prices via Alpha Vantage
- Technical indicators: SMA, EMA, MACD
- ML-based close price prediction

### 📰 News & Sentiment
- News headline sentiment analysis using NLP
- Impact score prediction (Low / Medium / High)
- Emoji-coded visual indicators

### 📈 Historical Trends
- 1-day price forecast using Facebook Prophet
- Plotly interactive chart with trend overlay

### 🧠 Executive Summary
- Automatic AI summary (BART model)
- Export reports to:
  - 📄 PDF (trend plot)
  - 🧾 Word doc (summary)

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Data:** Alpha Vantage (via yfinance), synthetic news
- **NLP Models:** BART, FinBERT, Sentence Transformers
- **ML Models:** Prophet, RandomForest
- **Visualization:** Plotly, Matplotlib
- **Export:** `python-docx`, PDF via Matplotlib

---

## 📂 Folder Structure

```
real_time_stock_dashboard/
├── app.py
├── src/
│   ├── data_fetcher.py
│   ├── indicators.py
│   ├── predictor.py
│   ├── sentiment.py
│   ├── summarizer.py
│   ├── logger.py
│   ├── trend_forecast.py
│   ├── impact_scorer.py
│   ├── report_generator.py
```

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

Make sure to include:
```txt
streamlit
yfinance
prophet
scikit-learn
transformers
torch
plotly
python-docx
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧠 Example Use Case

- Monitor a stock like `AAPL`
- Analyze how recent headlines affect the price
- View predictions, trends, and export insights for reporting

---

## 📝 Future Additions

- [ ] FAISS-based semantic news retrieval
- [ ] Sector and macroeconomic filters
- [ ] Scheduled report automation

---

## 📌 Author

**Nithin Reddy Yanna**

Made with ❤️ using AI, ML, and a love for finance-tech.
