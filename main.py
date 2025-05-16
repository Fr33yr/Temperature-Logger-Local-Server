from fastapi import FastAPI
import socketio
import sqlite3
import uvicorn
import os

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

# GET /templogs endpoint
@fastapi_app.get("/templogs")
def get_templogs(limit: int = 15):
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
def get_templogs(limit: int = 15):
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
def get_templogs(limit: int = 15):
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
def get_templogs(limit: int = 15):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-1 hour') ORDER BY created_at DESC", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {e}")


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