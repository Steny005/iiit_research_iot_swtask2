import React, { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";
import axios from "axios";
import { API_BASE_URL } from "../config";

const ChartView = ({ vertical }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/${vertical}`)
      .then((res) => setData(res.data.data))
      .catch((err) => console.error(err));
  }, [vertical]);

  if (data.length === 0) return <p>Loading {vertical} data...</p>;

  const timestamps = data.map((d) => d.created_at);

  // Select metrics based on vertical
  let metrics = [];
  switch (vertical) {
    case "aq":
      metrics = [
        { key: "calibrated_pm25", name: "PM2.5 (µg/m³)" },
        { key: "calibrated_pm10", name: "PM10 (µg/m³)" },
        { key: "calibrated_temperature", name: "Temperature (°C)" },
        { key: "calibrated_relative_humidity", name: "Humidity (%)" },
        { key: "calibrated_noise", name: "Noise (dB)" },
      ];
      break;

    case "sl":
      metrics = [
        { key: "active_power", name: "Active Power (kW)" },
        { key: "voltage_rs", name: "Voltage (V)" },
        { key: "frequency", name: "Frequency (Hz)" },
        { key: "power_factor", name: "Power Factor" },
        { key: "pv1_power", name: "PV1 Power (kW)" },
        { key: "pv2_power", name: "PV2 Power (kW)" },
        { key: "pv3_power", name: "PV3 Power (kW)" },
      ];
      break;

    case "wf":
      metrics = [
        { key: "flowrate", name: "Flow Rate (L/s)" },
        { key: "pressure", name: "Pressure (Pa)" },
        { key: "pressure_voltage", name: "Pressure Voltage (V)" },
        { key: "flow_volume", name: "Flow Volume (m³)" },
        { key: "total_flow", name: "Total Flow (m³)" },
      ];
      break;

    default:
      metrics = [{ key: "", name: "Unknown Metric" }];
  }

  // Create ECharts series dynamically
  const series = metrics.map((m) => ({
    name: m.name,
    type: "line",
    smooth: true,
    data: data.map((d) => parseFloat(d[m.key] ?? 0)),
  }));

  const option = {
    title: { text: `${vertical.toUpperCase()} Dashboard – Sensor Trends` },
    tooltip: { trigger: "axis" },
    legend: { data: metrics.map((m) => m.name) },
    xAxis: { type: "category", data: timestamps, name: "Time" },
    yAxis: { type: "value", name: "Sensor Value" },
    series,
  };

  return (
    <div style={{ marginBottom: "2rem" }}>
      <ReactECharts option={option} style={{ height: "500px" }} />
    </div>
  );
};

export default ChartView;
