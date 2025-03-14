from binance.client import Client
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pandas_ta as ta

# ✅ Binance API Credentials (Replace with actual keys)
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
client = Client(API_KEY, API_SECRET, tld='us')

# ✅ Fetch Price Data from Binance API
def get_price_data(symbol, interval="1h", limit=100):
    """Fetch price data from Binance API and return a DataFrame."""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    
    # ✅ Convert API response to DataFrame
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    # ✅ Convert numeric columns to float
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_asset_volume", "taker_buy_base", "taker_buy_quote"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# ✅ Add Technical Indicators (RSI, MACD, SMA)
def add_indicators(df):
    """Add RSI, MACD, and SMA indicators to the DataFrame."""
    df["RSI"] = df.ta.rsi(length=14)
    macd = df.ta.macd(fast=12, slow=26, signal=9)
    df["MACD"] = macd["MACD_12_26_9"]
    df["Signal"] = macd["MACDs_12_26_9"]
    df["SMA50"] = df.ta.sma(length=50)
    return df

# ✅ Build LSTM Model for Price Prediction
def build_model():
    """Create and return an LSTM model for price prediction."""
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(10, 1)),
        LSTM(64),
        Dense(32, activation="relu"),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(loss="mse", optimizer="adam")
    return model

# ✅ Train LSTM Model
def train_model(data):
    """Train an LSTM model with price data."""
    scaler = MinMaxScaler(feature_range=(0, 1))
    data["close"] = scaler.fit_transform(data["close"].values.reshape(-1, 1))
    
    X, Y = [], []
    look_back = 10
    for i in range(len(data) - look_back):
        X.append(data["close"].values[i:i+look_back])
        Y.append(data["close"].values[i+look_back])
    
    X, Y = np.array(X), np.array(Y)

    model = build_model()
    model.fit(X.reshape(-1, look_back, 1), Y, epochs=20, batch_size=16)

    return model, scaler

# ✅ AI Price Prediction Function
def predict_price(symbol):
    """Predict future price using AI model."""
    data = get_price_data(symbol)
    last_10 = np.array([data["close"].values[-10:]])

    model = build_model()
    try:
        model.load_weights("backend/models/ai_trading_model.weights.h5")
    except:
        print("⚠️ No existing model found, training a new one...")
        model.fit(last_10.reshape(-1, 10, 1), np.array([data["close"].values[-1]]), epochs=1, batch_size=1)
        model.save_weights("backend/models/ai_trading_model.weights.h5")

    prediction = model.predict(last_10.reshape(1, 10, 1))
    print(f"🔮 AI Predicted Price for {symbol}: {prediction[0][0]}")
    return prediction[0][0]

