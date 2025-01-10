from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import Optional, List
from app.database.base.model import BaseModel, AuditMixin

class Dataset(BaseModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(default=None)
    name: str = Field()
    description: str
    datasource_id: int
    datasource_table: str
    datasource_columns: List = Field(sa_column=Column(JSON), default=[])
    datasource_primary_key: Optional[str] = None

    mappings: List["Mapping"] = Relationship(back_populates="dataset")