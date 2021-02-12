from fastapi import APIRouter, Depends
from requests import RoomCreateRequest
import logging
from controllers import insert_room, get_rooms, get_room, get_current_active_user, add_user_to_room
from mongodb import get_nosql_db, MongoClient
from config import MONGODB_DB_NAME
from models import User

router = APIRouter()
logger = logging.getLogger(__name__)


def format_ids(nested_dictionary):
    """
    Loops through nested dictionary (with arrays 1 layer deep) to
    properly format the MongoDB '_id' field to a string instead of an ObjectId
    """
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            nested_dictionary[key] = format_ids(value)
        elif type(value) is list:
            new_arr = []
            for item in value:
                if type(item) is dict:
                    new_arr.append(format_ids(item))
            nested_dictionary[key] = new_arr
        else:
            if key == "_id":
                nested_dictionary[key] = str(value)
    return nested_dictionary


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
    # ObjectId shenanagains
    formatted_rooms = [format_ids(room) for room in rooms]
    return formatted_rooms


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
