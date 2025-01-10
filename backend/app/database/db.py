
from collections.abc import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.utils.aws_client import AWSClient
from app.config import get_settings

settings = get_settings()

def get_database_engine():
    """
    Factory function to create appropriate database engine based on environment
    """
    if settings.ENVIRONMENT == "production":
        aws_client = AWSClient(settings.AWS_SECRET_ARN)
        return aws_client.get_engine()
    else:
        # Local PostgreSQL connection string
        return create_async_engine(settings.PG_LOCAL_DATABASE_URL, echo=True)

# Initialize engine once at module level
db_engine = get_database_engine()

async def get_engine() -> AsyncGenerator:
    async with async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False) as db_engine:
        yield db_engine

async def get_session() -> AsyncGenerator:
    async_session = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
