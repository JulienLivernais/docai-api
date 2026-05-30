from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class QABase(BaseModel):
    question: str = Field(...)

class QACreate(QABase):
    workspace_id: int

class QAResponse(QABase):
    id: int
    answer: str
    workspace_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

