from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT, SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from backend.models.crypto_ai import get_price_data, add_indicators, build_model
import numpy as np
import tensorflow as tf

# ✅ Binance API Credentials (Replace with actual keys)
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
client = Client(API_KEY, API_SECRET, tld='us')

# ✅ Fetch All Available Trading Pairs (USDT Pairs Only)
def get_all_coins():
    """Fetch all available USDT trading pairs from Binance."""
    exchange_info = client.get_exchange_info()
    return [s["symbol"] for s in exchange_info["symbols"] if s["quoteAsset"] == "USDT"]

# ✅ Ensure Model Exists or Train New Model
model = build_model()
try:
    model.load_weights("backend/models/ai_trading_model.weights.h5")
except:
    print("⚠️ No existing model found, training new model...")
    data = get_price_data("BTCUSDT")
    X = np.array([data["close"].values[-10:]])
    model.fit(X.reshape(-1, 10, 1), X[:, -1], epochs=1, batch_size=1)
    model.save_weights("backend/models/ai_trading_model.weights.h5")

# ✅ AI Price Prediction Function
def predict_price(symbol):
    """Predict future price using AI model."""
    data = get_price_data(symbol)
    last_10 = np.array([data["close"].values[-10:]])
    prediction = model.predict(last_10.reshape(1, 10, 1))
    print(f"🔮 AI Predicted Price for {symbol}: {prediction[0][0]}")
    return prediction[0][0]

# ✅ Buy Condition (AI + Technical Indicators)
def should_buy(symbol):
    """Decide whether to buy a cryptocurrency."""
    data = get_price_data(symbol)
    data = add_indicators(data)
    predicted_price = predict_price(symbol)
    
    if data["RSI"].iloc[-1] < 30 and predicted_price > data["close"].iloc[-1]:
        return True  # Buy if RSI is oversold & AI predicts price increase
    return False

# ✅ Sell Condition (AI + Technical Indicators)
def should_sell(symbol):
    """Decide whether to sell a cryptocurrency."""
    data = get_price_data(symbol)
    data = add_indicators(data)
    predicted_price = predict_price(symbol)
    
    if data["RSI"].iloc[-1] > 70 and predicted_price < data["close"].iloc[-1]:
        return True  # Sell if RSI is overbought & AI predicts price drop
    return False

# ✅ Execute Trade (Limit Orders)
def execute_trade(symbol, side, price):
    """Execute a limit order on Binance."""
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
        print(f"❌ Error placing order for {symbol}: {e}")

# ✅ Main Trading Function
def trade():
    """Run the trading strategy for all USDT trading pairs."""
    trading_pairs = get_all_coins()
    print(f"✅ Trading {len(trading_pairs)} pairs: {trading_pairs}")

    for symbol in trading_pairs:
        try:
            current_price = float(client.get_symbol_ticker(symbol=symbol)["price"])

            if should_buy(symbol):
                execute_trade(symbol, SIDE_BUY, current_price * 1.001)
            elif should_sell(symbol):
                execute_trade(symbol, SIDE_SELL, current_price * 0.999)
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")

# ✅ Run Trading Bot
if __name__ == "__main__":
    trade()
