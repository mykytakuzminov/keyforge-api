from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.users.models import User
from keyforge.users.repository import UserRepository
from keyforge.users.schemas import UserCreate, UserUpdate


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

    async def create(self, user_in: UserCreate) -> User:
        user = await self._user_repository.create(user_in.email, user_in.password)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def update(self, user_id: UUID, user_in: UserUpdate) -> User:
        user = await self._user_repository.update(
            user_id, user_in.email, user_in.password
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        await self._user_repository.delete(user_id)
        await self._db.commit()
        return
