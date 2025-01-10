from typing import List
from fastapi import APIRouter, Depends, Query, Request

from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.client import ClientResponse, ClientUpdate, ClientCreate
from app.services.client import ClientManagementService
from app.database.client.service import ClientService
from app.database.db import get_session
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter(
    prefix="/client/clients",
    tags=["clients"]
)

@router.get("", response_model=List[ClientResponse])
async def get_chili_clients(
    *,
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    rq: Request,
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = ClientService(db)
    return await service.get_chili_clients(offset, limit)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    *,
    db: AsyncSession = Depends(get_session),
    client_id: int,
    rq: Request
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = ClientService(db)
    client = await service.get_client_by_id(client_id)
    return client


@router.post("", response_model=ClientResponse)
async def create_client(
    *,
    db: AsyncSession = Depends(get_session),
    client: ClientCreate,
    rq: Request
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = ClientManagementService(db)
    return await service.create_client(client)


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    *,
    db: AsyncSession = Depends(get_session),
    client_id: int,
    client: ClientUpdate,
    rq: Request
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = ClientManagementService(db)
    return await service.update_current_client(client_id, client)
