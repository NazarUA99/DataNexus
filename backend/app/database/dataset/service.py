from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.database.dataset.model import Dataset
from app.schemas.dataset import DatasetUpdate
from datetime import datetime, timezone
from app.utils.logging import AppLogger
from app.database.base.service import BaseService
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError

logger = AppLogger().get_logger()


class DatasetService(BaseService):
    async def get_all_datasets(self, offset: int, limit: int):
        query = select(Dataset).offset(offset).limit(limit)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        logger.info(f"result len: {len(result)}")
        return result.all()

    async def get_dataset_by_id(self, dataset_id: int):
        query = select(Dataset).where(Dataset.id == dataset_id)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        logger.info(f"result len: {len(result)}")
        dataset = result.first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        return dataset