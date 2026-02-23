# 📈 Stock Predictor Portal

> An intelligent full-stack web application powered by LSTM neural networks for real-time stock price predictions and 30-day forecasts.

<br>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.6-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

---

## ✨ Overview

**Stock Predictor Portal** combines the power of deep learning with real-time financial data to deliver actionable stock predictions. Users can register, authenticate, and instantly access AI-generated price forecasts backed by 10 years of historical market data — all through a sleek, dark-themed interface.

---

## 🎯 Key Features

### 🔐 User Authentication
- Secure registration and login via Django's built-in auth system
- Session-based user management
- Protected prediction routes — authenticated users only
- Public AAPL preview available without login

### 🧠 LSTM-Powered Prediction Engine
- **Deep Learning Model** trained on 10 years of historical stock data
- **Dual Predictions:**
  - Historical backtesting to validate model accuracy
  - 30-day forward price forecast
- **100-day rolling window** analysis for next-day price estimation
- MinMaxScaler normalization (0–1) for neural network compatibility
- 70% training / 30% testing data split

### 📡 Real-Time Data Integration
- Live stock data via the **yfinance** API (Yahoo Finance)
- Supports any global ticker — `AAPL`, `TSLA`, `INFY.NS`, and more
- 10-year historical OHLCV data retrieval

### 📊 Interactive Visualizations
- Server-side **Matplotlib** charts rendered as embedded base64 PNGs
- Displays:
  - Historical closing prices
  - Model predictions vs. actual prices
  - ±3% prediction confidence bands
  - 30-day future forecast with trend lines
  - 100-day moving average overlay

### 🖥️ Modern UI
- Dark-themed responsive interface with smooth animations
- Stock ticker search with autocomplete
- Live real-time price ticker

### ⚡ Graceful Error Handling
- Lazy model loading — no crash on startup if model is missing
- Fallback to historical-only plots if ML model is unavailable
- User-friendly error messages for invalid ticker symbols

---

## 🛠️ Tech Stack

### Backend
| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Web Framework | Django 5.2.6 |
| WSGI Server | Gunicorn 25.1.0 |
| Static Files | WhiteNoise 6.11.0 |

### Machine Learning & Data Science
| Component | Library | Purpose |
|-----------|---------|---------|
| Deep Learning | TensorFlow 2.20.0 | LSTM neural network framework |
| Neural Networks | Keras 3.13.2 | Model architecture & prediction |
| Data Manipulation | Pandas 3.0.1 | Stock data processing |
| Numerical Computing | NumPy 2.4.2 | Array operations & reshaping |
| Data Scaling | scikit-learn 1.8.0 | MinMaxScaler normalization |
| Visualization | Matplotlib 3.10.8 | Chart generation |
| Stock Data | yfinance 1.2.0 | Real-time & historical prices |

### Frontend & Deployment
| Component | Technology |
|-----------|------------|
| Templating | Django Templates + Jinja2 |
| Styling | Custom CSS (dark mode, flexbox, animations) |
| Charts | Matplotlib → base64 (server-side) |
| Images | Pillow 12.1.1 |
| Hosting | Render.com |
| Database | SQLite / PostgreSQL (optional) |

---

## 🏗️ Project Structure

```
stock predictor/
├── StockPredictionPortal/          # Django project root
│   ├── manage.py
│   ├── db.sqlite3
│   │
│   ├── StockPredictionPortal/      # Core Django config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── views.py                # Home view (renders predictions)
│   │   └── ml/
│   │       ├── stock_predictor.py  # ML engine (LSTM predictions)
│   │       └── stock_prediction_model.keras
│   │
│   ├── authentication/             # User auth app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── templates/
│   │       └── registration/
│   │
│   └── templates/
│       ├── base.html
│       ├── home.html
│       └── ...
│
├── requirements.txt
├── runtime.txt
├── build.sh
├── start.sh
└── .gitignore
```

---

## 🔄 Data Flow

```
1. User Request
       ↓
2. Django View  (views.py)
       ↓
3. ML Engine  (stock_predictor.py)
   ├── Fetch 10-year data  (yfinance)
   ├── Preprocess & scale  (MinMaxScaler)
   ├── Load LSTM model     (Keras)
   ├── Historical predictions + 30-day forecast
   └── Generate chart      (Matplotlib → base64)
       ↓
4. Render Chart in HTML Template
       ↓
5. HTTP Response to Browser
```

---

## 🧠 ML Model Details

| Property | Detail |
|----------|--------|
| **Model Type** | LSTM (Long Short-Term Memory) |
| **Input** | 100-day window of normalized closing prices |
| **Output** | Next day's predicted closing price |
| **Forecast Horizon** | 30-day forward prediction |
| **Training Data** | 10 years of daily OHLCV (Yahoo Finance) |
| **Normalization** | MinMaxScaler (0–1) |
| **Data Split** | 70% training / 30% validation |
| **Model Size** | ~10–50 MB (.keras file) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/stock-predictor-portal.git
cd stock-predictor-portal

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd StockPredictionPortal
python manage.py migrate

# Start the development server
python manage.py runserver
```

### Environment Variables

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## ☁️ Deployment (Render.com)

```bash
# Build command
bash build.sh   # Installs deps, runs migrations, collects static

# Start command
bash start.sh   # Gunicorn from StockPredictionPortal dir
```

**Required environment variables on Render:**

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Your Django secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Your Render domain |

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Dependencies | ~40 packages |
| Build Time | ~2 min (first deploy) |
| Prediction Latency | ~1–3 seconds per ticker |
| Static Files | 127 files |
| Database | SQLite (auto-migrated) |

---

## 🔮 Roadmap

- [ ] RSI, MACD, Bollinger Bands indicators
- [ ] Multi-symbol comparison dashboard
- [ ] Email alerts for price thresholds
- [ ] Transformer / Attention-based model improvements
- [ ] Real-time WebSocket price updates
- [ ] Mobile app
- [ ] Cryptocurrency price predictions

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using Django, TensorFlow, and yfinance
</p>
