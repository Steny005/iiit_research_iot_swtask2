import React, { useState } from "react";
import ChartView from "./components/chartview";

function App() {
  const [vertical, setVertical] = useState("aq");

  return (
    <div style={{ textAlign: "center" }}>
      <h1>IoT Sensor values Dashboard </h1>
      <div>
        <button onClick={() => setVertical("aq")}>Air Quality</button>
        <button onClick={() => setVertical("wf")}>Water Flow</button>
        <button onClick={() => setVertical("sl")}>Solar Light</button>
      </div>
      <ChartView vertical={vertical} />
    </div>
  );
}

export default App;
