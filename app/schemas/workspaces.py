from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)  # optional


class WorkspaceResponse(WorkspaceBase):
    id: int
    pinecone_namespace: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


