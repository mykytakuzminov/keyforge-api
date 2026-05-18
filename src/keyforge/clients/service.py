from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.clients.models import Client
from keyforge.clients.repository import ClientRepository
from keyforge.core.security import generate_secure_token, hash_value


class ClientService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._client_repository = ClientRepository(db)

    async def create(self, name: str) -> tuple[Client, str]:
        client_secret = generate_secure_token()
        hashed_client_secret = hash_value(client_secret)
        client = await self._client_repository.create(name, hashed_client_secret)
        await self._db.commit()
        await self._db.refresh(client)
        return client, client_secret

    async def get_by_id(self, client_id: UUID) -> Client:
        if (client := await self._client_repository.get_by_id(client_id)) is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    async def get_all(self) -> list[Client]:
        return await self._client_repository.get_all()

    async def delete(self, client_id: UUID) -> None:
        await self._client_repository.delete(client_id)
        await self._db.commit()

    async def update(self, client_id: UUID, name: str) -> Client:
        if (client := await self._client_repository.update(client_id, name)) is None:
            raise HTTPException(status_code=404, detail="Client not found")
        await self._db.commit()
        await self._db.refresh(client)
        return client
