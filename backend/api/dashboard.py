from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.models.crypto_ai import predict_price
from binance.client import Client
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Add CORS support to allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Binance API Credentials (Replace with actual keys)
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
client = Client(API_KEY, API_SECRET, tld="us")

# ✅ Store last executed trades
trade_log = []

# ✅ Home Route
@app.get("/")
async def home():
    return {"message": "AI Crypto Trading Dashboard API"}

# ✅ Fetch All Coins Trading Data from Binance
@app.get("/trading-data")
async def get_trading_data():
    try:
        tickers = client.get_all_tickers()  # Fetch all available trading pairs
        data = []

        for ticker in tickers:
            symbol = ticker["symbol"]
            price = float(ticker["price"])

            try:
                predicted_price = predict_price(symbol)  # AI price prediction
            except Exception:
                predicted_price = None  # If prediction fails, set to None

            data.append({
                "symbol": symbol,
                "current_price": price,
                "predicted_price": predicted_price
            })

        return data

    except Exception as e:
        return {"error": f"Failed to fetch trading data: {str(e)}"}

# ✅ WebSocket for Live Price Streaming (ALL Coins)
@app.websocket("/ws/prices")
async def stream_prices(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            prices = {}
            tickers = client.get_all_tickers()  # Fetch all coins

            for ticker in tickers:
                symbol = ticker["symbol"]
                price = float(ticker["price"])

                try:
                    predicted_price = predict_price(symbol)
                except Exception:
                    predicted_price = None  # Handle AI prediction failures

                prices[symbol] = {
                    "current_price": price,
                    "predicted_price": predicted_price
                }

            await websocket.send_text(json.dumps(prices))
            await asyncio.sleep(5)  # Update every 5 seconds

    except WebSocketDisconnect:
        print("WebSocket client disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

# ✅ API to Get Trade History
@app.get("/trades")
async def get_trades():
    return {"trades": trade_log}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# ✅ Store Executed Trades
def log_trade(symbol, side, price):
    trade_log.append({
        "symbol": symbol,
        "side": side,
        "price": price
    })
