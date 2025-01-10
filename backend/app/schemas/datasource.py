from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class DatasourceType(str, Enum):
    MSSQL = "mssql"
    Postgres = "postgres"
    API = "api"


class DatasourceBase(SQLModel):
    id: Optional[int] = None
    client_id: int
    name: str
    description: str
    type: DatasourceType
    server: str
    serverport: int
    database: str
    username: str
    directconnect: bool


class DatasourceCreate(DatasourceBase):
    password: str

class DatasourceResponse(DatasourceBase):
    id: int

class DatasourceUpdate(SQLModel):
    client_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[DatasourceType] = None
    server: Optional[str] = None
    serverport: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    directconnect: Optional[bool] = None
    password: Optional[str] = None

