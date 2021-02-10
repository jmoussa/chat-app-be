from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from mongodb import close_mongo_connection, connect_to_mongo, get_nosql_db
from starlette.middleware.cors import CORSMiddleware
from config import MONGODB_DB_NAME
from api import router as api_router
from notifier import Notifier
import pymongo
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',  # can alter with time
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
        await notifier.generator.asend(None)
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


notifier = Notifier()


@app.websocket("/ws/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name, user_name):
    await notifier.connect(websocket, room_name)
    try:
        while True:
            data = await websocket.receive_text()
            logger.warning(f"Recieved: {data}")
            await notifier.push(f"{data}", room_name)
    except WebSocketDisconnect:
        await notifier.remove(websocket, room_name)


app.include_router(api_router, prefix="/api")
