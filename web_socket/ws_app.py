import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Can handle incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# HTTP endpoint to send data to all connected WebSocket clients
@app.get("/send")
async def send_message(message: str):
    await manager.broadcast(message)
    return {"message": "Message sent to WebSocket clients"}


if __name__ == "__main__":
    # Don't use reload=True here
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/send?message=Hello
