# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware
import os

# --- Database Config ---
DB_URL = os.getenv("DB_URL", "postgresql://postgres:chiNNu2005@localhost:5432/iot_db")
engine = create_engine(DB_URL)

# --- FastAPI App ---
app = FastAPI(title="IoT Sensor Data API", version="1.0")

# Allow React frontend to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "IoT API is running"}

@app.get("/api/{vertical}")
def get_vertical_data(vertical: str):
    """
    Fetch all data from a given vertical table.
    Example: /api/aq , /api/wf , /api/sl
    """
    table = f"{vertical.lower()}_data"
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table} LIMIT 1000"))
            rows = [dict(row._mapping) for row in result]
            return {"vertical": vertical, "count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
