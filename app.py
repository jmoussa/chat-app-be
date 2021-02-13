from fastapi import FastAPI, WebSocket
from websockets.exceptions import ConnectionClosedError
from starlette.websockets import WebSocketDisconnect
from controllers import get_room, remove_user_from_room, upload_message_to_room
from mongodb import close_mongo_connection, connect_to_mongo, get_nosql_db
from starlette.middleware.cors import CORSMiddleware
from config import MONGODB_DB_NAME
from api import router as api_router
from notifier import ConnectionManager
import pymongo
import logging
import json

app = FastAPI()
logger = logging.getLogger(__name__)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    try:
        db.create_collection("users")
    except pymongo.errors.CollectionInvalid as e:
        logging.warning(e)
        pass
    try:
        db.create_collection("rooms")
    except pymongo.errors.CollectionInvalid as e:
        logging.warning(e)
        pass
    try:
        db.create_collection("messages")
    except pymongo.errors.CollectionInvalid as e:
        logging.warning(e)
        pass
    try:
        user_collection = db.users
        room_collection = db.rooms
        user_collection.create_index("username", name="username", unique=True)
        room_collection.create_index("room_name", name="room_name", unique=True)
    except pymongo.errors.CollectionInvalid as e:
        logging.warning(e)
        pass


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


manager = ConnectionManager()


@app.websocket("/ws/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name, user_name):
    # add user
    await manager.connect(websocket, room_name)
    room = await get_room(room_name)
    data = {
        "content": f"{user_name} has entered the chat",
        "user": {"username": user_name},
        "room_name": room_name,
        "type": "entrance",
        "new_room_obj": room,
    }
    await manager.broadcast(f"{json.dumps(data, default=str)}")
    try:
        # wait for messages
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"{data}", websocket)
            await upload_message_to_room(data)
            await manager.broadcast(f"{data}")
    except (WebSocketDisconnect, ConnectionClosedError):
        # remove user
        logger.warning("Disconnecting Websocket")
        await manager.disconnect(websocket, room_name)
        await remove_user_from_room(None, room_name, username=user_name)
        room = await get_room(room_name)
        data = {
            "content": f"{user_name} has left the chat",
            "user": {"username": user_name},
            "room_name": room_name,
            "type": "dismissal",
            "new_room_obj": room,
        }
        await manager.broadcast(f"{json.dumps(data, default=str)}")


app.include_router(api_router, prefix="/api")
