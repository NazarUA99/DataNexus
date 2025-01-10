import json
import subprocess
from fastapi import Depends
import uvicorn
import os

from app.config import Environment
from sqlmodel import SQLModel, text, inspect
from app.database.db import db_engine
from app.utils.logging import AppLogger
from app.config import get_settings

logger = AppLogger().get_logger()
settings = get_settings()

def create_all_db_objects():
    logger.info("Initializing database...")
    
    # Create connection and check if schema exists
    # with db_engine.connect() as conn:
    #     # Check if schema exists
    #     inspector = inspect(db_engine)
    #     if 'app' not in inspector.get_schema_names():
    #         logger.info("Creating 'app' schema...")
    #         conn.execute(text("CREATE SCHEMA IF NOT EXISTS app"))
    #         conn.commit()
        
    #     # Set search path
    #     conn.execute(text("SET search_path TO app"))
    #     conn.commit()
    
    # Import all models to ensure they're registered with SQLModel
    from app.database.client.model import Client
    from app.database.dataset.model import Dataset
    from app.database.datasource.model import Datasource
    from app.database.mapping.model import Mapping
    from app.database.user.model import User
    
    # Create all tables
    logger.info("Creating all database tables...")
    SQLModel.metadata.create_all(db_engine)
    logger.info("Database initialization completed")

def run_server():
    config = uvicorn.Config(
        "app.server:app",
        host="0.0.0.0",
        port=8009,
        log_config="./config.ini",
        reload=True,  # This is good
        reload_dirs=["app"],  # Add this to specify which directories to watch
        reload_includes=["*.py"],  # Add this to specify which files to watch
        workers=1  # Add this when using reload
    )
    logger.info(f"ENVIRONMENT: {settings.ENVIRONMENT}")
    if settings.ENVIRONMENT == Environment.LOCAL.value:
        config.log_config = "./config.local.ini"
    

    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    create_all_db_objects()
    run_server()
