from pydantic import BaseModel, SecretStr, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: SecretStr = Field(min_length=8, max_length=24)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=120)
    password: SecretStr | None = Field(default=None, min_length=8, max_length=24)


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Для работы с ORM-моделями
        arbitrary_types_allowed = True
