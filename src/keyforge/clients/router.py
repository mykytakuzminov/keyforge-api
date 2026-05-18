from uuid import UUID

from fastapi import APIRouter, Depends

from keyforge.auth.dependencies import get_current_admin
from keyforge.auth.schemas import TokenPayload
from keyforge.clients.dependencies import get_client_service
from keyforge.clients.models import Client
from keyforge.clients.schemas import (
    ClientCreate,
    ClientCreateResponse,
    ClientResponse,
    ClientUpdate,
)
from keyforge.clients.service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=list[ClientResponse])
async def get_all_clients(
    service: ClientService = Depends(get_client_service),
    _: TokenPayload = Depends(get_current_admin),
) -> list[Client]:
    return await service.get_all()


@router.post("/", response_model=ClientCreateResponse)
async def create_client(
    client_in: ClientCreate,
    service: ClientService = Depends(get_client_service),
    _: TokenPayload = Depends(get_current_admin),
) -> ClientCreateResponse:
    client, secret = await service.create(client_in.name)
    response = ClientCreateResponse.model_validate(client)
    response.client_secret = secret
    return response


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client_by_id(
    client_id: UUID,
    service: ClientService = Depends(get_client_service),
    _: TokenPayload = Depends(get_current_admin),
) -> Client:
    return await service.get_by_id(client_id)


@router.delete("/{client_id}", status_code=204)
async def delete_client(
    client_id: UUID,
    service: ClientService = Depends(get_client_service),
    _: TokenPayload = Depends(get_current_admin),
) -> None:
    await service.delete(client_id)


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: UUID,
    client_in: ClientUpdate,
    service: ClientService = Depends(get_client_service),
    _: TokenPayload = Depends(get_current_admin),
) -> Client:
    return await service.update(client_id, client_in.name)
