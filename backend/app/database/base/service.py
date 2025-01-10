from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession


class BaseService:
    """
    Base service class for all services.

    Attributes:
        db_session (AsyncSession): database session
    """

    db_session: Optional[AsyncSession]

    def __init__(self, db_session: Optional[AsyncSession] = None, **kwargs):
        self.db_session = db_session