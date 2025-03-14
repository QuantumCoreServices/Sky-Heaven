const API_WS_URL = "ws://localhost:8000/ws/prices";  // WebSocket endpoint

export function connectWebSocket(setLiveData) {
    const socket = new WebSocket(API_WS_URL);

    socket.onopen = () => {
        console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            setLiveData(data);
        } catch (error) {
            console.error("Error parsing WebSocket message:", error);
        }
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
        console.log("WebSocket disconnected. Reconnecting...");
        setTimeout(() => connectWebSocket(setLiveData), 5000);
    };

    return socket;
}

