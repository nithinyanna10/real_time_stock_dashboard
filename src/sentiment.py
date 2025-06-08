# src/sentiment.py
import requests
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_headlines(headlines):
    return [sentiment_pipeline(h)[0] for h in headlines]

# Dummy headlines test
if __name__ == "__main__":
    headlines = [
        "Apple stock rises after new iPhone launch",
        "Investors worry about inflation"
    ]
    results = analyze_headlines(headlines)
    for r in results:
        print(r)
