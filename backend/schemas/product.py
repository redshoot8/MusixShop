from pydantic import BaseModel, Field
from datetime import datetime
from backend.database.models import ProductType


class ProductBase(BaseModel):
    title: str = Field(max_length=100)
    product_type: ProductType
    price: int = Field(ge=0)
    description: str | None = None
    image_url : str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    title: str | None = Field(default=None, max_length=100)
    product_type: ProductType | None = None
    price: int | None = Field(default=None, ge=0)
    description: str | None = None
    image_url: str | None = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
