from sqlmodel import select
from fastapi import HTTPException
from app.database.user.model import User
from app.utils.logging import AppLogger
from app.database.base.service import BaseService
from sqlalchemy.exc import IntegrityError, StatementError, SQLAlchemyError

logger = AppLogger().get_logger()

class UserService(BaseService):

    async def get_chili_users(self, offset: int, limit: int):
        query = select(User).offset(offset).limit(limit)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        return result.all()

    async def get_user_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        logger.info(f"query: {query}")
        result = await self.db_session.exec(query)
        user = result.first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user