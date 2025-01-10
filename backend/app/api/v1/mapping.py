from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.mapping import MappingResponse, MappingCreate, MappingUpdate
from app.database.db import get_session
from app.utils.logging import AppLogger
from app.database.mapping.service import MappingService
from app.database.mapping.model import Mapping
logger = AppLogger().get_logger()

router = APIRouter(
    prefix="/client/configs",
    tags=["mappings"]
)


@router.get("", response_model=List[MappingResponse])
async def get_all_mappings(
    *,
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    logger.info("getting mappings")
    service = MappingService(db)
    mappings = await service.get_all_mappings(offset, limit)
    logger.info(f"mappings: {mappings}")
    return mappings


@router.get("/{mapping_id}", response_model=MappingResponse)
async def get_mapping(
    *,
    db: AsyncSession = Depends(get_session),
    mapping_id: int
):
    service = MappingService(db)
    mapping = await service.get_mapping_by_id(mapping_id)
    logger.info(f"mapping: {mapping}")
    return mapping
    

@router.post("", response_model=MappingResponse)
async def create_mapping(
    *,
    db: AsyncSession = Depends(get_session),
    mapping: MappingCreate
):
    # Convert the mapping object to dict and handle serialization
    mapping_data = mapping.model_dump()
    
    # Create new Mapping instance with serialized data
    db_mapping = Mapping(**mapping_data)
    return await db_mapping.save(db)


@router.patch("/{mapping_id}", response_model=MappingResponse)
async def update_mapping(
    *,
    db: AsyncSession = Depends(get_session),
    mapping_id: int,
    mapping: MappingUpdate
):
    service = MappingService(db)
    db_mapping = await service.get_mapping_by_id(mapping_id)
    return await db_mapping.update(db, **mapping.model_dump(exclude_none=True))
