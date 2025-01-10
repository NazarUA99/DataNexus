from sqlmodel import select
from fastapi import HTTPException
from app.database.mapping.model import Mapping
from app.schemas.mapping import MappingResponse, MappingUpdate
from app.database.base.service import BaseService
from app.utils.logging import AppLogger
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError

logger = AppLogger().get_logger()

class MappingService(BaseService):
    async def get_all_mappings(self, offset: int, limit: int):
        query = select(Mapping).offset(offset).limit(limit)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        return result.all()

    async def get_mapping_by_id(self, mapping_id: int):
        if mapping_id == 0:
            return MappingResponse(id=0, client_id=0, name="Default Mapping", description="Default Mapping", dataset_id=0,
                             dataset_columns={}, custom_columns=[])
        query = select(Mapping).where(Mapping.id == mapping_id)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        mapping = result.first()
        if not mapping:
            raise HTTPException(status_code=404, detail="Mapping not found")
        return mapping