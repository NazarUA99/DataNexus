from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Form
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.users import UserResponse, UserCreate, UserUpdate
from app.database.user.service import UserService
from app.services.user import UserManagementService
from app.utils.logging import AppLogger
from app.database.db import get_session

logger = AppLogger().get_logger()

router = APIRouter(
    prefix="/client/users",
    tags=["users"]
)

@router.get("", response_model=List[UserResponse])
async def get_chili_users(
    *,
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    rq: Request,
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = UserService(db)
    users = await service.get_chili_users(offset, limit)
    logger.info(f"users: {users}")
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    *,
    db: AsyncSession = Depends(get_session),
    user_id: int,
    rq: Request
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    logger.info(f"user ID: {user.id}")
    return user


@router.post("", response_model=UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(get_session),
    user: UserCreate,
    rq: Request
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = UserManagementService(db)
    return await service.create_user(user)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    db: AsyncSession = Depends(get_session),
    user_id: int,user: UserUpdate, rq: Request
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = UserManagementService(db)
    return await service.update_current_user(user_id, user)

@router.post("/login", response_model=UserResponse)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    rq: Request,
    db: AsyncSession = Depends(get_session)
):
    logger.info(f"request {rq.method}:{router.prefix}{rq.path_params}")
    service = UserManagementService(db)
    return await service.login(username, password)
    
