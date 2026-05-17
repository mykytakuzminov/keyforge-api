from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.core.security import hash_password
from keyforge.users.models import User
from keyforge.users.repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._user_repository = UserRepository(db)

    async def get_by_id(self, user_id: UUID) -> User:
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_by_email(self, email: str) -> User:
        user = await self._user_repository.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create(self, email: str, password: str) -> User:
        hashed_password = hash_password(password)
        user = await self._user_repository.create(email, hashed_password)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def update(
        self, user_id: UUID, email: str | None, password: str | None
    ) -> User:
        hashed_password = hash_password(password) if password is not None else None
        user = await self._user_repository.update(user_id, email, hashed_password)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        await self._user_repository.delete(user_id)
        await self._db.commit()
        return
