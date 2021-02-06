from fastapi import APIRouter, Depends
from requests import RoomCreateRequest

from controllers import insert_room, get_rooms, get_room, get_current_active_user
from mongodb import get_nosql_db, AsyncIOMotorClient
from config import MONGODB_DB_NAME
from models import User

router = APIRouter()


@router.put("/room", tags=["Rooms"])
async def create_room(
    request: RoomCreateRequest,
    client: AsyncIOMotorClient = Depends(get_nosql_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a room
    """
    db = client[MONGODB_DB_NAME]
    collection = db.rooms
    res = await insert_room(request.username, request.room_name, collection)
    return res


@router.get("/rooms", tags=["Rooms"])
async def get_all_rooms(
    client: AsyncIOMotorClient = Depends(get_nosql_db), current_user: User = Depends(get_current_active_user),
):
    """
    Fetch all available rooms
    """
    rooms = await get_rooms()
    return rooms


@router.get("/room/{room_name}", tags=["Rooms"])
async def get_single_room(
    room_name, current_user: User = Depends(get_current_active_user),
):
    """
    Get Room by room name
    """
    room = await get_room(room_name)
    return room
