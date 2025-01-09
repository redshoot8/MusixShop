from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from backend.config import settings

engine = create_async_engine(settings.database_url_asyncpg)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
