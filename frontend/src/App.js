import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000"; // ✅ Change this if backend runs on another machine

function App() {
  const [prices, setPrices] = useState({});
  const [trades, setTrades] = useState([]);
  const [status, setStatus] = useState("Connecting...");

  // 🔹 Fetch Live Prices via WebSocket
  useEffect(() => {
    const ws = new WebSocket(`${API_URL.replace("http", "ws")}/ws/prices`);

    ws.onopen = () => setStatus("✅ Connected to WebSocket");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPrices(data);
    };
    ws.onerror = (error) => setStatus("❌ WebSocket Error: " + error.message);
    ws.onclose = () => setStatus("🔄 Reconnecting...");

    return () => ws.close();
  }, []);

  // 🔹 Fetch Trade History
  useEffect(() => {
    axios.get(`${API_URL}/trades`).then((response) => {
      setTrades(response.data.trades);
    }).catch((error) => {
      console.error("Error fetching trade history:", error);
    });
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>🚀 AI Crypto Trading Dashboard</h1>
      <h3>Status: {status}</h3>

      <h2>📊 Live Prices</h2>
      {Object.keys(prices).length > 0 ? (
        Object.keys(prices).map((symbol) => (
          <div key={symbol}>
            <strong>{symbol}</strong>: ${prices[symbol].current_price.toFixed(2)} 
            (AI Predicted: ${prices[symbol].predicted_price.toFixed(2)})
          </div>
        ))
      ) : (
        <p>🔄 Waiting for data...</p>
      )}

      <h2>📜 Trade History</h2>
      {trades.length > 0 ? (
        <ul>
          {trades.map((trade, index) => (
            <li key={index}>
              {trade.symbol} - {trade.side} at ${trade.price}
            </li>
          ))}
        </ul>
      ) : (
        <p>No trades yet...</p>
      )}
    </div>
  );
}

export default App;


