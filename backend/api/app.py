import uvicorn
from fastapi import FastAPI
from mangum import Mangum  # Add this line
from fastapi.middleware.cors import CORSMiddleware
from trading.trading_bot import predict_price  # Import AI function

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# 🔹 AI Prediction Endpoint
@app.get("/predict/{symbol}")
def get_prediction(symbol: str):
    predicted_price = predict_price(symbol)
    return {"symbol": symbol, "predicted_price": predicted_price}

# This makes the app work with AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
