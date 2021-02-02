from fastapi import APIRouter, Depends
from requests import RoomCreateRequest

from controllers import insert_room, get_rooms, get_room
from mongodb import get_nosql_db, AsyncIOMotorClient
from config import MONGODB_DB_NAME

router = APIRouter()


@router.put("/create_room")
async def create_room(request: RoomCreateRequest, client: AsyncIOMotorClient = Depends(get_nosql_db)):
    db = client[MONGODB_DB_NAME]
    collection = db.rooms
    res = await insert_room(request.username, request.room_name, collection)
    return res


@router.get("/rooms")
async def get_all_rooms(client: AsyncIOMotorClient = Depends(get_nosql_db)):
    rooms = await get_rooms()
    return rooms


@router.get("/room/{room_name}")
async def get_single_room(room_name):
    room = await get_room(room_name)
    return room
