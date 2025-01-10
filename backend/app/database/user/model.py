from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from typing import Optional
from datetime import datetime
from pydantic import EmailStr
from app.database.base.model import BaseModel, AuditMixin

class User(BaseModel, AuditMixin, table=True):
    client_id: int = Field(default=None, foreign_key="app.client.id", index=True)
    client: Optional["Client"] = Relationship(back_populates="users")
    name: str = Field(sa_column=Column(String))
    username: str = Field(sa_column=Column(String, unique=True, index=True))
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    password: str
    created: datetime
    created_by: int
    updated: datetime
    updated_by: int
    last_login: Optional[datetime] = None