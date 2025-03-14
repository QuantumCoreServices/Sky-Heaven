import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Container,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  Paper,
} from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [tradingData, setTradingData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/trading-data"); // API Endpoint
        setTradingData(response.data);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("⚠️ Failed to load trading data. Check API connection.");
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh data every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <Container maxWidth="lg" style={{ textAlign: "center", fontFamily: "Arial, sans-serif", marginTop: "20px" }}>
      <Typography variant="h3" gutterBottom>
        📊 AI-Powered Crypto Trading Dashboard
      </Typography>
      <Typography variant="h6" color="textSecondary" paragraph>
        Live market data & AI-driven trading insights powered by <strong>QuantumCore AI</strong>.
      </Typography>

      {error && <Typography color="error">{error}</Typography>}

      <Paper elevation={3} style={{ padding: "20px", marginBottom: "30px" }}>
        <Table>
          <TableHead>
            <TableRow style={{ backgroundColor: "#212121", color: "white" }}>
              <TableCell style={{ color: "white" }}>🔹 Coin</TableCell>
              <TableCell style={{ color: "white" }}>💰 Price (USD)</TableCell>
              <TableCell style={{ color: "white" }}>📈 RSI</TableCell>
              <TableCell style={{ color: "white" }}>🔀 MACD</TableCell>
              <TableCell style={{ color: "white" }}>📊 AI Prediction</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tradingData.length > 0 ? (
              tradingData.map((coin, index) => (
                <TableRow key={index} style={{ backgroundColor: index % 2 === 0 ? "#f5f5f5" : "#ffffff" }}>
                  <TableCell><strong>{coin.symbol}</strong></TableCell>
                  <TableCell>${coin.price.toFixed(2)}</TableCell>
                  <TableCell>{coin.rsi.toFixed(2)}</TableCell>
                  <TableCell>{coin.macd.toFixed(2)}</TableCell>
                  <TableCell style={{ color: coin.prediction > coin.price ? "green" : "red", fontWeight: "bold" }}>
                    {coin.prediction.toFixed(2)}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan="5">📡 Fetching live data...</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Paper>

      {/* AI Price Prediction Graph */}
      <Typography variant="h5" gutterBottom>
        🔮 AI-Powered Market Trend Forecasting
      </Typography>
      <ResponsiveContainer width="95%" height={400}>
        <LineChart data={tradingData.map(coin => ({ name: coin.symbol, price: coin.price, prediction: coin.prediction }))}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="price" stroke="#8884d8" name="Actual Price" />
          <Line type="monotone" dataKey="prediction" stroke="#ff7300" name="AI Predicted Price" />
        </LineChart>
      </ResponsiveContainer>

      <Typography variant="body1" style={{ marginTop: "20px", color: "#666" }}>
        Developed by <strong>QuantumCore AI</strong> | The Future of Algorithmic Trading 🚀
      </Typography>
    </Container>
  );
}

export default App;
