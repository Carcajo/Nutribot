import aioredis
from config import Settings

settings = Settings()
redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")


async def set_state(user_id, state):
    await redis.set(f"state:{user_id}", state)


async def get_state(user_id):
    return await redis.get(f"state:{user_id}")

# import redis
# from config import Settings
#
# settings = Settings()
# redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
#
#
# async def set_state(user_id, state):
#     await redis_client.set(f"state:{user_id}", state)
#
#
# async def get_state(user_id):
#     return await redis_client.get(f"state:{user_id}")
