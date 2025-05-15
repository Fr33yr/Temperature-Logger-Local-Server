from fastapi import FastAPI
import socketio
import sqlite3
import uvicorn

# Set up Socket.IO server (ASGI mode)
sio = socketio.AsyncServer(async_mode='asgi')
fastapi_app = FastAPI()
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

@fastapi_app.get("/")
async def root():
    return {"message": "Backend is running"}

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
