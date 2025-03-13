import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState("Fetching...");

  useEffect(() => {
    axios.get("https://6t3txwn699.execute-api.us-west-2.amazonaws.com/prod/")
      .then((response) => {
        console.log("✅ API Response:", response.data);  // Debugging
        setData(response.data.message || "No data received");
      })
      .catch((error) => {
        console.error("❌ API Error:", error);  // Log error
        setData("Error fetching data");
      });
  }, []);

  return (
    <div>
      <h1>FastAPI + React Integration</h1>
      <p>Response from FastAPI: {data}</p>
    </div>
  );
}

export default App;

