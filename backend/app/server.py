import time
import json
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
from contextlib import asynccontextmanager
from .config import get_settings
from .config import Environment
from .api.v1.client import router as clients_router
from .api.v1.dataset import router as datasets_router
from .api.v1.datasource import router as datasources_router
from .api.v1.mapping import router as mappings_router
from .api.v1.user import router as users_router
from .utils.logging import AppLogger

logger = AppLogger().get_logger()
settings = get_settings()

# Context manager that will run before the server starts and after the server stops
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the redis connection
    try:
        yield
    finally:
        pass
        # Close redis connection and release the resources

# Create the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients_router)
app.include_router(datasets_router)
app.include_router(datasources_router)
app.include_router(mappings_router)
app.include_router(users_router)

# Index route
@app.get("/")
async def index():
    return {"message": "Master Server API"}