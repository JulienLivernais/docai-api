from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=30)
    email: EmailStr

    @field_validator('username')
    @classmethod
    def strip_username(cls, v) -> str:
        return v.strip()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=30)


class UserUpdate(UserBase):
    username: str | None = Field(None, min_length=5, max_length=30)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=30) # Field(None, ...) means Optional


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)





