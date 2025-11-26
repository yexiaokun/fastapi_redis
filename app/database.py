from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import redis.asyncio as aioredis

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
REDIS_URL = os.getenv("REDIS_URL")

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client[DB_NAME]

redis_client = aioredis.from_url(REDIS_URL)