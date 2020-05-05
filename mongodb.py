from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT


# MongoDB
class MongoDB:
    client: AsyncIOMotorClient = None


db = MongoDB()


async def get_nosql_db() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(
        str(MONGODB_URL), maxPoolSize=MAX_CONNECTIONS_COUNT, minPoolSize=MIN_CONNECTIONS_COUNT,
    )
    logging.info("connected to mongodb")


async def close_mongo_connection():
    db.client.close()
    logging.info("closed mongo connection")
