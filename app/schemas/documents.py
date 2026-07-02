from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str = Field(..., max_length=255)

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    workspace_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

