from logging.config import fileConfig
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel
from alembic import context
from app.config import get_settings
import asyncio

from app.utils.logging import AppLogger
# Import all models explicitly
from app.database import *

logger = AppLogger().get_logger()

app_settings = get_settings()
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def include_name(name, type_, parent_names):
    """
    Include only the schemas and tables that are in the app schema.
    """
    if type_ == "schema":
        return name in ["app", "public"]
    return True

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=app_settings.PG_LOCAL_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        version_table_schema="app",
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        # Create schema if it doesn't exist
        context.execute(text("CREATE SCHEMA IF NOT EXISTS app"))
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_name=include_name,
        version_table_schema="app",
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in online mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = app_settings.PG_LOCAL_DATABASE_URL
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Create schema if it doesn't exist
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS app"))
        await connection.commit()

        # Run migrations using run_sync
        await connection.run_sync(do_run_migrations)

def run_sync_migrations():
    """Run migrations in 'online' mode."""
    try:
        asyncio.run(run_migrations_online())
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_sync_migrations()
