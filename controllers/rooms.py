from config import MONGODB_DB_NAME
from controllers.users import get_user
from mongodb import get_nosql_db
from models import RoomInDB
import logging

logger = logging.getLogger(__name__)


async def insert_room(username, room_name, collection):
    room = {}
    room["room_name"] = room_name
    user = await get_user(username)
    room["members"] = [user] if user is not None else []
    # room = Room(**room)
    dbroom = RoomInDB(**room)
    response = await collection.insert_one(dbroom.dict())
    return {"id_inserted": str(response.inserted_id)}


async def get_rooms():
    client = await get_nosql_db()
    db = client[MONGODB_DB_NAME]
    collection = db.rooms
    rows = collection.find()
    row_list = []
    async for row in rows:
        row_list.append(RoomInDB(**row))
    return row_list


async def get_room(room_name) -> RoomInDB:
    client = await get_nosql_db()
    db_client = client[MONGODB_DB_NAME]
    db = db_client.rooms
    row = await db.find_one({"room_name": room_name})
    if row is not None:
        return RoomInDB(**row)
    else:
        return None


async def set_room_activity(room_name, activity_bool):
    client = await get_nosql_db()
    db_client = client[MONGODB_DB_NAME]
    db = db_client.rooms
    room = await get_room(room_name)
    _id = room["_id"]
    try:
        result = await db.replace_one({"_id": _id}, {"activity": activity_bool})
        if result.modified_count < 1:
            raise Exception("Room activity could not be updated")
    except Exception as e:
        logger.error(f"ERROR SETTING ACTIVITY: {e}")
    new_doc = await get_room(room_name)
    return new_doc
