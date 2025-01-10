from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON

class DatasetCreate(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(default=None)
    name: str = Field()
    description: str
    datasource_id: int
    datasource_table: str
    datasource_columns: List = Field(sa_column=Column(JSON), default=[])
    datasource_primary_key: Optional[str] = None

class DatasetResponse(DatasetCreate):
    id: int

class DatasetUpdate(DatasetResponse):
    client_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    datasource_id: Optional[int] = None
    datasource_table: Optional[str] = None
    datasource_columns: Optional[List] = None
    datasource_primary_key: Optional[str] = None