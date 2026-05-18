from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


ClientUpdate = ClientCreate


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    is_active: bool
    created_at: datetime


class ClientCreateResponse(ClientResponse):
    client_secret: str
