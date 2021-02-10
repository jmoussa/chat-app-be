from collections import defaultdict
from fastapi import WebSocket
from controllers import set_room_activity
import logging

logger = logging.getLogger(__name__)


class Notifier:
    def __init__(self):
        self.connections: dict = defaultdict(dict)
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            print(f"MESSAGE : {message}")
            msg = message["message"]
            room_name = message["room_name"]
            await self._notify(msg, room_name)

    async def push(self, msg: str, room_name: str = None):
        message_body = {"content": msg, "room_name": room_name}
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        logger.warning(room_name)
        await set_room_activity(room_name, True)
        if self.connections[room_name] == {} or len(self.connections[room_name]) == 0:
            self.connections[room_name] = []
        self.connections[room_name].append(websocket)
        print(f"CONNECTIONS : {self.connections[room_name]}")

    async def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)
        if len(self.connections[room_name]) == 0:
            await set_room_activity(room_name, False)

    async def _notify(self, message: str, room_name: str):
        living_connections = []
        while len(self.connections[room_name]) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections[room_name].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections[room_name] = living_connections
