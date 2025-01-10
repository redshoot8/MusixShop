from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from backend.database.models import Product
from backend.schemas.product import ProductCreate, ProductUpdate


async def create_product(session: AsyncSession, product: ProductCreate) -> Product:
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    result = await session.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()

async def get_all_products(session: AsyncSession) -> Sequence[Product]:
    result = await session.execute(select(Product))
    return result.scalars().all()


async def update_product(session: AsyncSession, product_id: int, product_data: ProductUpdate):
    updated_fields = product_data.model_dump(exclude_unset=True)
    query = update(Product).where(Product.id == product_id).values(**updated_fields)
    await session.execute(query)
    await session.commit()


async def delete_product(session: AsyncSession, product_id: int):
    await session.execute(delete(Product).where(Product.id == product_id))
    await session.commit()

