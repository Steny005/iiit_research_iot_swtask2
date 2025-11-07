# IoT Data Visualization Dashboard

A full-stack IoT data visualization platform built with **FastAPI** (backend) and **React.js + Vite** (frontend).  
It visualizes real or stored IoT data for multiple verticals — **Air Quality, Solar Light, and Water Flow** — using dynamic charts.

## Project Structure
TASK2_SOFTWAREPROJECT/
├── backend/
│ ├── iot_dataset.csv
│ ├── iot_dataset_mapping.csv
│ ├── loaddata.py
│ ├── main.py
│ └── pycache/
│
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── assets/
│ │ ├── components/chartview.jsx
│ │ ├── App.jsx
│ │ ├── config.js
│ │ └── main.jsx
│ ├── package.json
│ └── vite.config.js
│
└── readme.md


## Overview

The system connects a **PostgreSQL database** to a FastAPI backend and visualizes sensor data through a React (ECharts) frontend.  
Users can switch between dashboards for each vertical and analyze trends over time.

## Datasets and Parameters

**Air Quality (AQ)**  
- calibrated_pm25, calibrated_pm10, calibrated_temperature, calibrated_relative_humidity, calibrated_noise

**Solar Light (SL)**  
- active_power, voltage_rs, frequency, power_factor, pv1_power, pv2_power, pv3_power

**Water Flow (WF)**  
- flowrate, pressure, pressure_voltage, flow_volume, total_flow

## Steps Summary

1. Created PostgreSQL database `iot_db`.
2. Loaded and inserted data into **aq**, **sl**, and **wf** tables.
3. Built FastAPI backend with endpoints:  
   - `/api/aq`  
   - `/api/sl`  
   - `/api/wf`
4. Converted `NaN → None` for clean JSON responses.
5. Developed React frontend using Vite.
6. Used **ECharts** to plot time-series sensor data.

## Backend (FastAPI)

- Connects to PostgreSQL and retrieves vertical data.
- Cleans data and returns JSON responses.
- Example endpoints:  
  `/api/aq`, `/api/sl`, `/api/wf`

## Frontend (React + Vite)

- Fetches API data via **axios**.
- Displays charts using **ECharts**.
- Navigation switches between AQ, SL, and WF dashboards.

## Visualization

Each dashboard shows time-series line graphs with:  
- **X-axis:** Timestamp (`created_at`)  
- **Y-axis:** Sensor metric values  
- **Chart Type:** Line chart (multi-parameter view)

## Run Instructions

**Backend**

```bash
cd backend
uvicorn main:app --reload

cd frontend
npm install
npm run dev
Access the dashboard at: http://localhost:5173/

Conclusion
This project integrates PostgreSQL, FastAPI, and React (ECharts) to create a real-time IoT visualization dashboard.
It enables users to analyze and compare environmental, solar, and water flow data effectively.

Drive link: [VIDEO](https://drive.google.com/drive/folders/1qbRXy2FbGH1fNBuw61clthe7P3Wa6D0a?usp=sharing)