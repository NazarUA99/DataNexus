from enum import Enum
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from .dataset import DatasetResponse

class MappingDatasetColumn(SQLModel):
    label: str
    selected: bool = True

class MappingCustomColumnType(str, Enum):
    freeform = "freeform"
    static_list = "static_list"
    dynamic_list = "dynamic_list"

class MappingCustomColumn(SQLModel):
    label: str
    type: MappingCustomColumnType
    value: Optional[str] = None

class MappingCreate(SQLModel):
    id: Optional[int] = None
    client_id: int
    name: str
    description: Optional[str] = None
    dataset_id: Optional[int] = Field(default=None, foreign_key="app.dataset.id")
    dataset_columns: dict[str, MappingDatasetColumn] = Field(sa_column=Column(JSON), default={})
    custom_columns: List[MappingCustomColumn] = Field(sa_column=Column(JSON), default=[])

class MappingResponse(MappingCreate):
    id: int
    dataset: Optional[DatasetResponse] = None


class MappingUpdate(SQLModel):
    client_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    dataset_id: Optional[int] = None
    dataset_columns: Optional[dict[str, MappingDatasetColumn]] = None
    custom_columns: Optional[List[MappingCustomColumn]] = None




