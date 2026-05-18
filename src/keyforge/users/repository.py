from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.users.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, email: str, password: str) -> User:
        user = User(email=email, hashed_password=password)
        self._db.add(user)
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self._db.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update(
        self, user_id: UUID, email: str | None, password: str | None
    ) -> User | None:
        if (user := await self.get_by_id(user_id)) is None:
            return None
        if email is not None:
            user.email = email
        if password is not None:
            user.hashed_password = password
        return user

    async def delete(self, user_id: UUID) -> None:
        if (user := await self.get_by_id(user_id)) is None:
            return None
        await self._db.delete(user)
