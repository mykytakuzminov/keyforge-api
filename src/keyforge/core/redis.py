from redis.asyncio import Redis

redis_client: Redis | None = None


def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis not initialized")
    return redis_client
