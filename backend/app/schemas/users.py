from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, String
from pydantic import EmailStr
from datetime import datetime

class UserBase(SQLModel):
    id: Optional[int] = None
    client_id: int
    name: str
    username: str = Field(sa_column=Column(String, unique=True, index=True))
    email: EmailStr

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created: datetime
    created_by: int
    updated: datetime
    updated_by: int
    last_login: Optional[datetime] = None


class UserUpdate(SQLModel):
    client_id: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    last_login: Optional[datetime] = None


class UserUpdatePassword(SQLModel):
    password: Optional[str] = None