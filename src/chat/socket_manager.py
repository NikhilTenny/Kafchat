from fastapi import WebSocket
from typing import List
import json


class SocketManager:
    def __init__(self):
        self.active_connections: dict[int,WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, id: int):
        await websocket.accept()
        self.active_connections[id] = websocket
        
    def disconnect(self, id: int):
        del self.active_connections[id]
        
    async def personal_msg(self, message: dict, id: int):
        if id in self.active_connections:
            await self.active_connections[id].send_text(
                json.dumps(message)
            )
        else:
            print(f'userid {id} websocket not connected')
            
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))
            

sock_manager = SocketManager()
