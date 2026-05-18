from uuid import UUID

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.core.security import create_access_token, verify_hashed_value
from keyforge.tokens.repository import TokenRepository
from keyforge.users.models import User
from keyforge.users.repository import UserRepository


class AuthService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self._redis = redis
        self._db = db
        self._user_repository = UserRepository(db)
        self._token_repository = TokenRepository(redis)

    async def authenticate(self, email: str, password: str) -> User:
        if (user := await self._user_repository.get_by_email(email)) is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not verify_hashed_value(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Account is disabled")
        return user

    async def save(self, token: str, user_id: UUID) -> None:
        await self._token_repository.save(token, user_id)

    async def refresh(self, token: str) -> str:
        if (user_id := await self._token_repository.get(token)) is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        if (user := await self._user_repository.get_by_id(user_id)) is None:
            raise HTTPException(status_code=404, detail="User not found")
        access_token = create_access_token(user_id, user.role)
        return access_token

    async def logout(self, token: str) -> None:
        await self._token_repository.delete(token)
