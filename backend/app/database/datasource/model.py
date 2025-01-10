from enum import Enum
from app.database.base.model import BaseModel

class Datasource(BaseModel, table=True):
    client_id: int
    name: str
    description: str
    type: str
    server: str
    serverport: int
    database: str
    username: str
    directconnect: bool
    password: str