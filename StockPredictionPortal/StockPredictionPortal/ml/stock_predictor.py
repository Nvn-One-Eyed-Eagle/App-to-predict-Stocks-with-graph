import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import io, base64
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml", "stock_prediction_model.keras")
model = load_model(MODEL_PATH)

def get_stock_plot(ticker="AAPL"):
    try:
        now = datetime.now()
        start = datetime(now.year - 10, now.month, now.day)
        end = now

        df = yf.download(ticker, start, end)
        if df.empty:
            return None, f"Ticker '{ticker}' not found or no data available."

        df = df.reset_index()
        df["MA_100"] = df["Close"].rolling(100).mean()

        data_training = pd.DataFrame(df["Close"][0:int(len(df) * 0.7)])
        data_testing  = pd.DataFrame(df["Close"][int(len(df) * 0.7):])

        scaler = MinMaxScaler(feature_range=(0, 1))
        data_training_array = scaler.fit_transform(data_training)

        # ── Test set (historical prediction) ──────────────────────────────────
        past_100_days = data_training.tail(100)
        final_df      = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data    = scaler.transform(final_df)

        x_test, y_test = [], []
        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i - 100:i])
            y_test.append(input_data[i, 0])
        x_test, y_test = np.array(x_test), np.array(y_test)

        y_predicted = model.predict(x_test)
        y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
        y_test      = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

        # ── 30-day future forecast ────────────────────────────────────────────
        # Seed with the last 100 scaled closing prices
        last_100_scaled = scaler.transform(
            pd.DataFrame(df["Close"].values[-100:])
        )  # shape (100, 1)

        future_input    = list(last_100_scaled.flatten())
        future_preds    = []

        for _ in range(30):
            window = np.array(future_input[-100:]).reshape(1, 100, 1)
            next_scaled = model.predict(window, verbose=0)[0, 0]
            future_preds.append(next_scaled)
            future_input.append(next_scaled)

        future_prices = scaler.inverse_transform(
            np.array(future_preds).reshape(-1, 1)
        ).flatten()

        # Build future date axis (skip weekends for realism)
        last_date    = df["Date"].iloc[-1]
        future_dates = []
        day = last_date
        while len(future_dates) < 30:
            day += timedelta(days=1)
            if day.weekday() < 5:           # Mon–Fri only
                future_dates.append(day)

        # ── Plot ──────────────────────────────────────────────────────────────
        # X-axis for historical section
        test_start_date = df["Date"].iloc[int(len(df) * 0.7)]
        test_dates      = pd.date_range(
            start=test_start_date,
            periods=len(y_test),
            freq="B"            # business days
        )

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(test_dates,    y_test,       color="#4C9BE8", linewidth=1.5,
                label="Original Price")
        ax.plot(test_dates,    y_predicted,  color="#E84C4C", linewidth=1.5,
                label="Predicted Price")

        # Vertical divider between history and forecast
        ax.axvline(x=last_date, color="#888888", linestyle="--", linewidth=1)

        ax.plot(future_dates,  future_prices, color="#2ECC71", linewidth=2,
                linestyle="--", label="30-Day Forecast")

        # Shaded confidence band (±3 % around the forecast line)
        confidence = future_prices * 0.03
        ax.fill_between(
            future_dates,
            future_prices - confidence,
            future_prices + confidence,
            color="#2ECC71", alpha=0.15,
            label="Forecast ±3 % band"
        )

        # Annotate last actual price and final forecast price
        ax.annotate(
            f"  ${future_prices[-1]:.2f}",
            xy=(future_dates[-1], future_prices[-1]),
            fontsize=9, color="#2ECC71", va="center"
        )

        ax.set_title(f"{ticker} — Historical Prediction & 30-Day Forecast",
                     fontsize=13, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        fig.autofmt_xdate()
        fig.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=120)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)

        return base64.b64encode(image_png).decode("utf-8"), None

    except Exception as e:
        return None, f"Error while processing ticker '{ticker}': {str(e)}"