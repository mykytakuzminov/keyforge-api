from uuid import UUID

from redis.asyncio import Redis


class TokenRepository:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def save(self, token: str, user_id: UUID) -> None:
        await self._redis.set(token, str(user_id), ex=604800)

    async def get(self, token: str) -> UUID | None:
        if (response := await self._redis.get(token)) is None:
            return None
        return UUID(response.decode())

    async def delete(self, token: str) -> None:
        await self._redis.delete(token)
