import React, { useEffect, useState } from "react";
import { fetchTradingData } from "./services/api";
import { API_BASE_URL, REFRESH_INTERVAL } from "./services/config";
import { connectWebSocket } from "./services/websocket";
import {
  Container,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  Paper,
  CircularProgress
} from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

export default function App() {
    const [tradingData, setTradingData] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            const data = await fetchTradingData();
            if (data.error) {
                setError(data.error);
            } else {
                setTradingData(data);
            }
            setLoading(false);
        };

        fetchData();
        const interval = setInterval(fetchData, REFRESH_INTERVAL);

        // Enable WebSocket for live data updates
        const socket = connectWebSocket(setTradingData);

        return () => {
            clearInterval(interval);
            socket.close();
        };
    }, []);

    return (
        <Container maxWidth="lg" style={{ textAlign: "center", fontFamily: "Arial, sans-serif", marginTop: "20px" }}>
            <Typography variant="h3" gutterBottom>
                📊 AI-Powered Crypto Trading Dashboard
            </Typography>
            <Typography variant="h6" color="textSecondary" paragraph>
                Real-time market data & AI-driven trading insights powered by QuantumCore AI.
            </Typography>

            {loading ? (
                <CircularProgress style={{ color: "#007AFF", margin: "20px" }} />
            ) : error ? (
                <Typography color="error">{error}</Typography>
            ) : (
                <>
                    {/* Data Table */}
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
                                            <TableCell>${coin.price ? coin.price.toFixed(2) : "N/A"}</TableCell>
                                            <TableCell>{coin.rsi ? coin.rsi.toFixed(2) : "N/A"}</TableCell>
                                            <TableCell>{coin.macd ? coin.macd.toFixed(2) : "N/A"}</TableCell>
                                            <TableCell style={{ color: coin.prediction > coin.price ? "green" : "red", fontWeight: "bold" }}>
                                                {coin.prediction ? coin.prediction.toFixed(2) : "N/A"}
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
                        <LineChart
                            data={tradingData.map(coin => ({ name: coin.symbol, price: coin.price || 0, prediction: coin.prediction || 0 }))}
                        >
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
                </>
            )}
        </Container>
    );
}
