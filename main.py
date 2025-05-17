from fastapi import FastAPI
import socketio
import sqlite3
import uvicorn
import os
import datetime
from pydantic import BaseModel

# Set up Socket.IO server (ASGI mode)
sio = socketio.AsyncServer(async_mode='asgi')
fastapi_app = FastAPI()
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

# Ensure the database path is correct
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db', 'NODEMCU.db')

# Connect to database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Creates a table if no exists
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS templogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            temperature REAL,
            created_at TEXT
        );
    """)
    conn.commit()
    conn.close()

# Root endpoint
@fastapi_app.get("/")
async def root():
    return {"message": "Backend is running"}

# Full log entry as stored in DB or returned to client
class TempLog(BaseModel):
    id: int
    name: str
    temperature: float
    created_at: str

# GET /templogs endpoint
@fastapi_app.get("/templogs")
async def get_templogs(limit: int = 15):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templogs ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")

# GET /templogs/week endpoint
@fastapi_app.get("/templogs/week")
async def get_templogs(limit: int = 15):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-7 days') ORDER BY created_at DESC", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")

# GET /templogs/day endpoint
@fastapi_app.get("/templogs/day")
async def get_templogs(limit: int = 15):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-1 day') ORDER BY created_at DESC", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")

# GET /templogs/hour endpoint
@fastapi_app.get("/templogs/hour")
async def get_templogs(limit: int = 15):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-1 hour') ORDER BY created_at DESC", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")

# Incoming POST request (client sends this)
class TempLogIn(BaseModel):
    name: str
    temperature: float

# POST /
@fastapi_app.post("/")
async def recive_data(data: TempLog):
    print("Data received:", data.dict())

    conn = get_db_connection()
    cursor = conn.cursor()

    created_at = datetime.utcnow().isoformat()

    try:
        cursor.execute(
            "INSERT INTO templogs (name, temperature, created_at) VALUES (?, ?, ?)",
            (data.name, data.temperature, created_at)
        )
        conn.commit()
        row_id = cursor.lastrowid
    except Exception as e:
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error inserting data into the database")
    finally:
        conn.close()

    # Emit to all connected clients via socket.io
    await sio.emit("logsupdate", {
        "id": row_id,
        "name": data.name,
        "temperature": data.temperature,
        "created_at": created_at
    })

    return {
        "message": "Data inserted successfully",
        "rowId": row_id
    }

# Socket.IO events
@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)

initialize_db()
# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)