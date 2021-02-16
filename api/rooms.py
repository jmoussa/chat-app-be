from fastapi import APIRouter, Depends
from requests import RoomCreateRequest
import logging
from controllers import insert_room, get_rooms, get_room, get_current_active_user, add_user_to_room
from mongodb import get_nosql_db, MongoClient
from config import MONGODB_DB_NAME
from models import User
from utils import format_ids

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/room", tags=["Rooms"])
async def create_room(
    request: RoomCreateRequest,
    client: MongoClient = Depends(get_nosql_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a room
    """
    db = client[MONGODB_DB_NAME]
    collection = db.rooms
    res = await insert_room(request.username, request.room_name, collection)
    return res


@router.put("/room/{room_name}", tags=["Rooms"])
async def add_user_to_room_members(
    room_name: str, client: MongoClient = Depends(get_nosql_db), current_user: User = Depends(get_current_active_user),
):
    """
    Add a user to the room's members
    """
    row = await add_user_to_room(current_user.username, room_name)
    return row


@router.get("/rooms", tags=["Rooms"])
async def get_all_rooms(
    client: MongoClient = Depends(get_nosql_db), current_user: User = Depends(get_current_active_user)
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
    formatted_room = format_ids(room)
    return formatted_room
