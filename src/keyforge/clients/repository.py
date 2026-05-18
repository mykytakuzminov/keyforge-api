from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.clients.models import Client


class ClientRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, name: str, client_secret: str) -> Client:
        client = Client(name=name, client_secret=client_secret)
        self._db.add(client)
        return client

    async def get_by_id(self, client_id: UUID) -> Client | None:
        return await self._db.get(Client, client_id)

    async def get_all(self) -> list[Client]:
        result = await self._db.execute(select(Client))
        return list(result.scalars().all())

    async def update(self, client_id: UUID, name: str) -> Client | None:
        if (client := await self.get_by_id(client_id)) is None:
            return None
        client.name = name
        return client

    async def delete(self, client_id: UUID) -> None:
        if (client := await self.get_by_id(client_id)) is None:
            return None
        await self._db.delete(client)
