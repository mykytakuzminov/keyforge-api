from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("")
AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):  # type: ignore[misc]
    pass


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionFactory() as session:
        yield session
