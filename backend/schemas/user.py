from pydantic import BaseModel, SecretStr
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(UserBase):
    username: str | None = None
    password: SecretStr | None = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Для работы с ORM-моделями
        arbitrary_types_allowed = True
