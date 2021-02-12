from config import MONGODB_DB_NAME
from controllers.users import get_user
from mongodb import get_nosql_db
from models import RoomInDB, User
import logging
from bson import ObjectId

logger = logging.getLogger(__name__)


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


async def get_rooms():
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    collection = db.rooms
    rows = collection.find()
    row_list = []
    for row in rows:
        row["_id"] = str(row["_id"])
        row_list.append(row)
    return row_list


async def get_room(room_name) -> RoomInDB:
    client = await get_nosql_db()
    db_client = client[MONGODB_DB_NAME]
    db = db_client.rooms
    row = db.find_one({"room_name": room_name})
    if row is not None:
        row["_id"] = str(row["_id"])
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
        if user not in room["members"]:
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
        if user in room["members"]:
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
