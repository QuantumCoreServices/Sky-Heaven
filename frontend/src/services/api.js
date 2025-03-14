const API_BASE_URL = "http://localhost:8000";  // Backend API URL

export async function fetchTradingData() {
    try {
        const response = await fetch(`${API_BASE_URL}/trading-data`);
        if (!response.ok) {
            throw new Error("Failed to fetch trading data");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching trading data:", error);
        return { error: "Unable to fetch trading data" };
    }
}
