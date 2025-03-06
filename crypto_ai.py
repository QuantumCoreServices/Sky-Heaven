from binance.client import Client
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

api_key = "your_binance_api_key"
api_secret = "your_binance_api_secret"

client = Client(api_key, api_secret)

def get_all_coins():
    symbols = client.get_exchange_info()["symbols"]
    return [s["symbol"] for s in symbols if s["quoteAsset"] == "USDT"]

def get_price_data(symbol, interval="1h", limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume"])
    data["close"] = data["close"].astype(float)
    return data

def train_model(data):
    scaler = MinMaxScaler(feature_range=(0,1))
    data["close"] = scaler.fit_transform(data["close"].values.reshape(-1, 1))
    
    X, Y = [], []
    look_back = 10
    for i in range(len(data) - look_back):
        X.append(data["close"].values[i:i+look_back])
        Y.append(data["close"].values[i+look_back])
    
    X, Y = np.array(X), np.array(Y)

    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(look_back, 1)),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dense(1)
    ])
    
    model.compile(loss="mse", optimizer="adam")
    model.fit(X.reshape(-1, look_back, 1), Y, epochs=20, batch_size=16)
    
    return model, scaler

def predict_prices():
    coins = get_all_coins()[:10]  
    predictions = {}

    for coin in coins:
        try:
            data = get_price_data(coin)
            model, scaler = train_model(data)
            last_10 = data["close"].values[-10:]
            prediction = model.predict(last_10.reshape(1, 10, 1))
            predictions[coin] = scaler.inverse_transform(prediction)[0][0]
        except Exception as e:
            print(f"Error processing {coin}: {e}")

    return predictions
