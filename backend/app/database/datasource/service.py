from sqlmodel import select
from fastapi import HTTPException
from app.database.datasource.model import Datasource
from app.schemas.datasource import DatasourceUpdate
from app.database.base.service import BaseService
from sqlalchemy.exc import IntegrityError
from app.utils.logging import AppLogger
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError

logger = AppLogger().get_logger()

class DatasourceService(BaseService):
    async def get_all_datasources(self, offset: int, limit: int):
        query = select(Datasource).offset(offset).limit(limit)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        return result.all()

    async def get_datasource_by_id(self, datasource_id: int):
        query = select(Datasource).where(Datasource.id == datasource_id)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        datasource = result.first()
        if not datasource:
            raise HTTPException(status_code=404, detail="Datasource not found")
        return datasource
