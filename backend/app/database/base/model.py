from datetime import datetime, timezone
from typing import Any, Optional
from sqlmodel import SQLModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, StatementError
from fastapi import HTTPException
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    __name__: str

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "__tablename__"):
            cls.__tablename__ = cls.__name__.lower()
        # Set schema for all tables
        if not hasattr(cls, "__table_args__"):
            cls.__table_args__ = dict(schema="app")

    async def save(self, db_session: AsyncSession):
        try:
            self.model_validate(self.model_dump())
            await db_session.add(self)
            await db_session.commit()
            await db_session.refresh(self)
            return self
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"IntegrityError: {e}"
            )
        except StatementError as e:
            # Handle JSON serialization errors and other statement errors
            logger.error(f"StatementError: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data format: {str(e)}"
            )
        except SQLAlchemyError as e:
            # Handle any other database-related errors
            logger.error(f"Database error: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            # Handle any unexpected errors
            logger.error(f"Unexpected error: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

    async def delete(self, db_session: AsyncSession):
        try:
            db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )

    async def update(self, db_session: AsyncSession, **kwargs):
        try:
            if not kwargs:
                return self

            updated_instance = self.model_copy(update=kwargs)
            updated_instance.model_validate(updated_instance.model_dump())

            for key, value in kwargs.items():
                setattr(self, key, value)

            await db_session.commit()
            await db_session.refresh(self)
            return self
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
        except StatementError as e:
            # Handle JSON serialization errors and other statement errors
            logger.error(f"StatementError: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data format: {str(e)}"
            )
        except Exception as e:
            # Handle any unexpected errors
            logger.error(f"Unexpected error: {e}")
            await db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )


class AuditMixin(SQLModel):
    """Mixin for tracking creation and updates"""
    created: datetime = Field(default_factory=datetime.now)
    created_by: int = Field(default=0)  # Default system user
    updated: datetime = Field(default_factory=lambda: datetime.now)
    updated_by: int = Field(default=0)  # Default system user


# Register the event listener for automatic update timestamp
@event.listens_for(AuditMixin, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated = datetime.now()
