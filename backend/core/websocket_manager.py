from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.client_data: Dict = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.client_data[client_id] = {"websocket": websocket, "subscriptions": set()}

    def disconnect(self, client_id: str):
        if client_id in self.client_data:
            try:
                self.active_connections.remove(self.client_data[client_id]["websocket"])
            except ValueError:
                pass
            del self.client_data[client_id]

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        for conn in disconnected:
            try:
                self.active_connections.remove(conn)
            except ValueError:
                pass

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.client_data:
            try:
                await self.client_data[client_id]["websocket"].send_json(message)
            except Exception:
                self.disconnect(client_id)
