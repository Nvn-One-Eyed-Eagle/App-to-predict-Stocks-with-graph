import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import io, base64
import os
from django.conf import settings

# Lazy model loading to avoid failing at import-time when the .keras file
# is not present on the host. This lets the app start and fall back to a
# simple historical plot if the trained model isn't available.
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml", "stock_prediction_model.keras")
_model = None

def _load_model_if_needed():
    global _model
    if _model is not None:
        return True
    try:
        from keras.models import load_model
        _model = load_model(MODEL_PATH)
        return True
    except Exception:
        _model = None
        return False

def get_stock_plot(ticker="AAPL"):
    try:
        now = datetime.now()
        start = datetime(now.year-10, now.month, now.day)
        end = now

        # try to fetch data
        df = yf.download(ticker, start, end)
        if df.empty:
            return None, f"Ticker '{ticker}' not found or no data available."

        df = df.reset_index()
        df["MA_100"] = df["Close"].rolling(100).mean()

        data_training = pd.DataFrame(df["Close"][0:int(len(df)*0.7)])
        data_testing = pd.DataFrame(df["Close"][int(len(df)*0.7):])

        scaler = MinMaxScaler(feature_range=(0,1))
        data_training_array = scaler.fit_transform(data_training)

        x_train, y_train = [], []
        for i in range(100, data_training_array.shape[0]):
            x_train.append(data_training_array[i-100:i])
            y_train.append(data_training_array[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        # Try to load the ML model; if it's not present, return a simple
        # historical-only plot as a graceful fallback instead of crashing.
        if not _load_model_if_needed():
            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(df['Date'], df['Close'], color='tab:blue', label='Close')
            ax.set_title(f"{ticker} — Historical Prices (model unavailable)")
            ax.set_xlabel('Date')
            ax.set_ylabel('Price (USD)')
            ax.legend()
            fig.autofmt_xdate()
            fig.tight_layout()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=120)
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plt.close(fig)
            return base64.b64encode(image_png).decode('utf-8'), None
        model = _model

        past_100_days = data_training.tail(100)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = scaler.transform(final_df)

        x_test, y_test = [], []
        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i-100:i])
            y_test.append(input_data[i, 0])
        x_test, y_test = np.array(x_test), np.array(y_test)

        y_predicted = model.predict(x_test)
        y_predicted = scaler.inverse_transform(y_predicted.reshape(-1,1)).flatten()
        y_test = scaler.inverse_transform(y_test.reshape(-1,1)).flatten()

        # Plot
        plt.figure(figsize=(10,5))
        plt.plot(y_test, "b", label="Original Price")
        plt.plot(y_predicted, "r", label="Predicted Price")
        plt.title(f"{ticker} Stock Prediction")
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode('utf-8'), None

    except Exception as e:
        return None, f"Error while processing ticker '{ticker}': {str(e)}"
