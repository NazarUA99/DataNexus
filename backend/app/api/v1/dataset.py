from typing import List
from fastapi import APIRouter, Depends, Query

from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.dataset import DatasetResponse, DatasetCreate, DatasetUpdate
from app.database.dataset.model import Dataset
from app.database.db import get_session
from app.utils.logging import AppLogger
from app.database.dataset.service import DatasetService

logger = AppLogger().get_logger()

router = APIRouter(
    prefix="/client/datasets",
    tags=["datasets"]
)

@router.get("", response_model=List[DatasetResponse])
async def get_all_datasets(
    *,
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    logger.info("getting datasets")
    service = DatasetService(db)
    datasets = await service.get_all_datasets(offset, limit)
    logger.info(f"datasets: {datasets}")
    return datasets

@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset_by_id(
    *,
    db: AsyncSession = Depends(get_session),
    dataset_id: int
):
    service = DatasetService(db)
    dataset = await service.get_dataset_by_id(dataset_id)
    logger.info(f"dataset: {dataset}")
    return dataset

@router.post("", response_model=DatasetResponse)
async def create_dataset(
    *,
    db: AsyncSession = Depends(get_session),
    dataset: DatasetCreate
):
    new_dataset = Dataset(**dataset.model_dump())
    return await new_dataset.save(db)

@router.patch("/{dataset_id}", response_model=DatasetResponse)
async def update_hero(
    *,
    db: AsyncSession = Depends(get_session),
    dataset_id: int,
    dataset: DatasetUpdate
):
    service = DatasetService(db)
    current_dataset = await service.get_dataset_by_id(dataset_id)
    return await current_dataset.update(db, **dataset.model_dump(exclude_none=True))
