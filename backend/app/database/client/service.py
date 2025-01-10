from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.database.client.model import Client
from app.utils.logging import AppLogger
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError
from app.database.base.service import BaseService
logger = AppLogger().get_logger()

class ClientService(BaseService):
    async def get_chili_clients(self, offset: int, limit: int):
        query = select(Client).offset(offset).limit(limit)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        return result.all()

    async def get_client_by_id(self, client_id: int):
        client = await self.db_session.get(Client, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client