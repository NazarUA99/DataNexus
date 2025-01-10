from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.client.model import Client
from app.schemas.client import ClientUpdate, ClientCreate
from app.database.client.service import ClientService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from app.utils.logging import AppLogger
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError

logger = AppLogger().get_logger()

class ClientManagementService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client_service = ClientService(db)

    async def create_client(self, client: ClientCreate) -> Client:

        api_client = ClientCreate.model_validate(client)
        logger.info(f"api_client: {api_client}")
        # Create client
        db_client = Client(**api_client.model_dump())
        logger.info(f"db_client: {db_client}")
        # date_now = datetime.now(timezone.utc)
        current_user_id = 0
        # db_client.created = date_now
        db_client.created_by = current_user_id
        # db_client.updated = date_now
        db_client.updated_by = current_user_id
        
        # Save client
        return await db_client.save(self.db)
        
    async def update_current_client(self, client_id: int, client: ClientUpdate):
        db_client = await self.client_service.get_client_by_id(client_id)
        logger.info(f"db_client before ID: {db_client.id}")

        if not db_client:
            logger.error(f"Client not found with id: {client_id}")
            raise HTTPException(status_code=404, detail="Client not found")
        
        new_client = ClientUpdate.model_validate(client)
        update_data = new_client.model_dump(exclude_none=True)
        update_data["updated"] = datetime.now()
        update_data["updated_by"] = 0

        return await db_client.update(self.db, **update_data)