from src.config import REDIS_SERVER, REDIS_PORT
from redis.asyncio import Redis


redis_client = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=0)
