from sqlmodel import SQLModel, Field, Column, JSON, Relationship
from typing import Optional, List
from pydantic import field_validator
from enum import Enum
from app.database.base.model import BaseModel, AuditMixin

class MappingDatasetColumn(SQLModel):
    label: str
    selected: bool = True
    def json(self):
        return {
            "label": self.label,
            "selected": self.selected
        }

class MappingCustomColumnType(str, Enum):
    freeform = "freeform"
    static_list = "static_list"
    dynamic_list = "dynamic_list"

class MappingCustomColumn(SQLModel):
    label: str
    type: MappingCustomColumnType
    value: Optional[str] = None

class Mapping(BaseModel, table=True):
    client_id: int
    name: str
    description: Optional[str] = None
    dataset_id: Optional[int] = Field(default=None, foreign_key="app.dataset.id")
    dataset_columns: dict[str, MappingDatasetColumn] = Field(sa_column=Column(JSON), default={})
    custom_columns: List[MappingCustomColumn] = Field(sa_column=Column(JSON), default=[])

    dataset: Optional["Dataset"] = Relationship(back_populates="mappings")

    @field_validator("dataset_columns", mode="before")
    def serialize_dataset_columns(cls, v):
        if isinstance(v, dict):
            return {
                key: value.model_dump() if isinstance(value, MappingDatasetColumn) else value 
                for key, value in v.items()
            }
        return v

    @field_validator("custom_columns", mode="before")
    def serialize_custom_columns(cls, v):
        if isinstance(v, list):
            return [
                item.model_dump() if isinstance(item, MappingCustomColumn) else item 
                for item in v
            ]
        return v
