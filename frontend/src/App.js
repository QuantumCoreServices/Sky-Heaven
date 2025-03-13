import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState("");

  useEffect(() => {
    axios
      .get("https://6t3txwn699.execute-api.us-west-2.amazonaws.com/prod/")
      .then((response) => {
        setData(response.data.message);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
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

