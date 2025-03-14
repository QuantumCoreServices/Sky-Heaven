from fastapi import FastAPI, WebSocket
from backend.models.crypto_ai import get_price_data, predict_price
from binance.client import Client
import json
import asyncio

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Binance API Credentials (Replace with actual keys)
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
client = Client(API_KEY, API_SECRET, tld='us')

# ✅ Store last executed trades
trade_log = []

@app.get("/")
async def home():
    return {"message": "AI Crypto Trading Dashboard API"}

# ✅ WebSocket for Live Prices
@app.websocket("/ws/prices")
async def stream_prices(websocket: WebSocket):
    await websocket.accept()
    trading_pairs = ["BTCUSDT", "ETHUSDT"]

    try:
        while True:
            prices = {}
            for symbol in trading_pairs:
                ticker = client.get_symbol_ticker(symbol=symbol)
                predicted_price = predict_price(symbol)
                prices[symbol] = {
                    "current_price": float(ticker["price"]),
                    "predicted_price": float(predicted_price)
                }
            
            await websocket.send_text(json.dumps(prices))
            await asyncio.sleep(5)  # Update every 5 seconds

    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

# ✅ API to Get Trade History
@app.get("/trades")
async def get_trades():
    return {"trades": trade_log}

# ✅ Store Executed Trades
def log_trade(symbol, side, price):
    trade_log.append({
        "symbol": symbol,
        "side": side,
        "price": price
    })
