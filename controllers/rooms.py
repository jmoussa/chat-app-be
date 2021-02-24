from config import MONGODB_DB_NAME
from controllers.users import get_user
from utils import format_ids
from mongodb import get_nosql_db
from models import RoomInDB, User
import logging
import json
from bson import ObjectId

logger = logging.getLogger(__name__)


async def upload_message_to_room(data):
    message_data = json.loads(data)
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    try:
        room = await get_room(message_data["room_name"])
        user = await get_user(message_data["user"]["username"])
        message_data["user"] = user
        message_data.pop("room_name", None)
        collection = db.rooms
        collection.update_one({"_id": ObjectId(room["_id"])}, {"$push": {"messages": message_data}})
        return True
    except Exception as e:
        logger.error(f"Error adding message to DB: {type(e)} {e}")
        return False


async def insert_room(username, room_name, collection):
    room = {}
    room["room_name"] = room_name
    user = await get_user(username)
    room["members"] = [user] if user is not None else []
    dbroom = RoomInDB(**room)
    response = collection.insert_one(dbroom.dict())
    res = collection.find_one({"_id": response.inserted_id})
    res["_id"] = str(res["_id"])
    return res


async def get_rooms(filter_list: list = None):
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    collection = db.rooms
    if filter_list is None:
        rows = collection.find()
    else:
        rows = collection.find({"room_name": {"$in": filter_list}})

    row_list = []
    for row in rows:
        f_row = format_ids(row)
        row_list.append(f_row)
    return row_list


async def get_room(room_name) -> RoomInDB:
    client = await get_nosql_db()
    db_client = client[MONGODB_DB_NAME]
    db = db_client.rooms
    row = db.find_one({"room_name": room_name})
    if row is not None:
        row = format_ids(row)
        return row
    else:
        return None


async def add_user_to_room(username: str, room_name: str):
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    try:
        room = await get_room(room_name)
        user = await get_user(username)

        collection = db.rooms
        username_list = [m["username"] for m in room["members"]]
        if user["username"] not in username_list:
            logger.info(f"Adding {user['username']} to members")
            collection.update_one({"_id": ObjectId(room["_id"])}, {"$push": {"members": user}})
            return True
        else:
            logger.info(f"{user['username']} is already a member")
            return True
    except Exception as e:
        logger.error(f"Error updating members: {e}")
        return None


async def remove_user_from_room(user: User, room_name: str, username=None):
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    try:
        room = await get_room(room_name)
        if username is not None and user is None:
            user = await get_user(username)

        collection = db.rooms
        username_list = [m["username"] for m in room["members"]]
        if user["username"] in username_list:
            logger.info(f"Removing {user['username']} from {room_name} members")
            collection.update_one(
                {"_id": ObjectId(room["_id"])}, {"$pull": {"members": {"username": user["username"]}}}
            )
            return True
        else:
            logger.info(f"{user['username']} is already out of the room")
            return True
    except Exception as e:
        logger.error(f"Error updating members: {e}")
        return False


async def set_room_activity(room_name, activity_bool):
    client = await get_nosql_db()
    db_client = client[MONGODB_DB_NAME]
    db = db_client.rooms
    room = await get_room(room_name)
    if room is not None:
        _id = room["_id"]
        try:
            result = db.update_one({"_id": ObjectId(_id)}, {"$set": {"active": activity_bool}})
            logger.info(f"Updated room activity {result}")
        except Exception as e:
            logger.error(f"ERROR SETTING ACTIVITY: {e}")
        new_doc = await get_room(room_name)
        return new_doc
    else:
        return None


async def get_user_favorites(user_name):
    user = await get_user(user_name)
    favs = user["favorites"]
    favorite_rooms = await get_rooms(favs)
    return favorite_rooms
