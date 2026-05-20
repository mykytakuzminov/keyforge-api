from fastapi import Request
from redis.asyncio import Redis


async def get_redis(request: Request) -> Redis:
    client: Redis = request.app.state.redis_client
    return client
