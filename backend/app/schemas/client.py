from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class ClientCreate(SQLModel):
    id: Optional[int] = None
    name: str
    contact_name: str
    contact_email: str
    db_name: str

class ClientResponse(ClientCreate):
    id: int
    created: datetime
    created_by: int
    updated: datetime
    updated_by: int


class ClientUpdate(SQLModel):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    db_name: Optional[str] = None
