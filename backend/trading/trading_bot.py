from binance.enums import ORDER_TYPE_LIMIT, SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT, SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from models.crypto_ai import get_price_data, add_indicators, build_model
import numpy as np
import tensorflow as tf

# 🔹 Connect to Binance API (Replace with your credentials)
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
client = Client(API_KEY, API_SECRET)

# 🔹 Load or Train AI Model
model = build_model()
try:
    model.load_weights("backend/models/ai_trading_model.h5")  # Load saved model
except:
    print("⚠️ No existing model found, training new model.")
    data = get_price_data("BTCUSDT")
    X = np.array([data["close"].values[-10:]])
    model.fit(X.reshape(-1, 10, 1), X[:, -1], epochs=1, batch_size=16)
    model.save_weights("backend/models/ai_trading_model.h5")

# 🔹 Predict Price Movement
def predict_price(symbol):
    data = get_price_data(symbol)
    last_10 = np.array([data["close"].values[-10:]])
    prediction = model.predict(last_10.reshape(1, 10, 1))
    return prediction[0][0]  # Return predicted price

# 🔹 Buy/Sell Logic Based on AI + Indicators
def should_buy(symbol):
    data = get_price_data(symbol)
    data = add_indicators(data)
    predicted_price = predict_price(symbol)
    
    if data["rsi"].iloc[-1] < 30 and predicted_price > data["close"].iloc[-1] * 1.02:
        return True  # Buy if RSI is oversold & AI predicts increase
    return False

def should_sell(symbol):
    data = get_price_data(symbol)
    data = add_indicators(data)
    predicted_price = predict_price(symbol)
    
    if data["rsi"].iloc[-1] > 70 and predicted_price < data["close"].iloc[-1] * 0.98:
        return True  # Sell if RSI is overbought & AI predicts drop
    return False

# 🔹 Execute Trade with Limit Orders
def execute_trade(symbol, side, price):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=0.01,  # Adjust quantity as needed
            price=str(price)
        )
        print(f"✅ {side} LIMIT order placed for {symbol} at {price}")
    except Exception as e:
        print(f"❌ Error placing order: {e}")

# 🔹 Run Trading Strategy
def trade():
    symbols = ["BTCUSDT", "ETHUSDT"]
    for symbol in symbols:
        current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])
        if should_buy(symbol):
            execute_trade(symbol, SIDE_BUY, current_price * 0.99)  # Buy slightly below market price
        elif should_sell(symbol):
            execute_trade(symbol, SIDE_SELL, current_price * 1.01)  # Sell slightly above market price

if __name__ == "__main__":
    trade()

def should_buy(symbol):
    data = get_price_data(symbol)
    data = add_indicators(data)
    if data["rsi"].iloc[-1] < 30 and data["macd"].iloc[-1] > data["signal"].iloc[-1]:
        return True  # Only buy if RSI is below 30 and MACD is bullish
    return False

def should_sell(symbol):
    data = get_price_data(symbol)
    data = add_indicators(data)
    if data["rsi"].iloc[-1] > 70 and data["macd"].iloc[-1] < data["signal"].iloc[-1]:
        return True  # Only sell if RSI is above 70 and MACD is bearish
    return False


def execute_trade(symbol, side, price):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=0.01,  # Adjust based on capital
            price=str(price)  # Limit price
        )
        print(f"✅ {side} LIMIT order executed for {symbol} at {price}")
    except Exception as e:
        print(f"❌ Error trading {symbol}: {e}")
