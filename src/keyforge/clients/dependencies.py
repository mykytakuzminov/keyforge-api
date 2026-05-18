from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from keyforge.clients.service import ClientService
from keyforge.core.database import get_db


def get_client_service(db: AsyncSession = Depends(get_db)) -> ClientService:
    return ClientService(db)
