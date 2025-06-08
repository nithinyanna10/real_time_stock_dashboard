# src/predictor.py
import numpy as np
from sklearn.linear_model import LinearRegression

def train_predictor(df, target_col='close', days=5):
    df = df.copy().tail(30)
    df['target'] = df[target_col].shift(-1)
    df = df.dropna()

    X = np.arange(len(df)).reshape(-1, 1)
    y = df['target'].values

    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(np.array([[len(df)]]))[0]

    return round(pred, 2)

# Test
if __name__ == "__main__":
    from data_fetcher import fetch_intraday
    df = fetch_intraday("AAPL")
    pred = train_predictor(df)
    print(f"Predicted next close: {pred}")
