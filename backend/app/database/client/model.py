from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from typing import Optional, List
from datetime import datetime
from app.database.base.model import BaseModel, AuditMixin
from sqlalchemy import Column, String


class ClientBase(BaseModel):
    name: str
    contact_name: str
    contact_email: str
    db_name: str = Field(sa_column=Column(String, unique=True))


class Client(ClientBase, AuditMixin, table=True):
    users: List["User"] = Relationship(back_populates="client")