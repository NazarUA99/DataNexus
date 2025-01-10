from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse
from app.database.datasource.service import DatasourceService
from app.database.db import get_session
from app.schemas.datasource import DatasourceResponse, DatasourceCreate, DatasourceUpdate
from app.utils.logging import AppLogger
from app.database.datasource.model import Datasource

logger = AppLogger().get_logger()
router = APIRouter(
    prefix="/client/datasources",
    tags=["datasources"]
)

@router.get("", response_model=list[DatasourceResponse])
async def get_all_datasources(
    *,
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    logger.info("getting all datasources full path")
    service = DatasourceService(db)
    datasources = await service.get_all_datasources(offset, limit)
    logger.info(f"datasources: {datasources}")
    return datasources

@router.get("/{datasource_id}", response_model=DatasourceResponse)
async def get_datasource(
    *,
    db: AsyncSession = Depends(get_session),
    datasource_id: int
):
    service = DatasourceService(db)
    datasource = await service.get_datasource_by_id(datasource_id)
    logger.info(f"datasource: {datasource}")
    return datasource

@router.post("", response_model=DatasourceResponse)
async def create_datasource(
    *,
    db: AsyncSession = Depends(get_session),
    datasource: DatasourceCreate
):
    datasource = Datasource.model_validate(datasource)
    return await datasource.save(db)

@router.patch("/{datasource_id}", response_model=DatasourceResponse)
async def update_datasource(
    *,
    db: AsyncSession = Depends(get_session),
    datasource_id: int,
    datasource: DatasourceUpdate
):
    service = DatasourceService(db)
    db_datasource = await service.get_datasource_by_id(datasource_id)
    return await db_datasource.update(db, **datasource.model_dump(exclude_none=True))

@router.post("/verify")
async def verify_datasource(
    *,
    datasource: DatasourceCreate
):
    datasource = Datasource.model_validate(datasource)
    return JSONResponse(content={"status": "success", "message": "Datasource verified successfully"})

