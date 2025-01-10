from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete, update
from backend.database.models import User
from backend.schemas.user import UserUpdate


async def create_user(session: AsyncSession, email, hashed_password) -> User:
    new_user = User(email=email, hashed_password=hashed_password)
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise ValueError('Username already exists')


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def update_user(session: AsyncSession, user_id: int, user_data: UserUpdate):
    query = update(User).where(User.id == user_id).values(**user_data.model_dump(exclude_unset=True))
    await session.execute(query)
    await session.commit()


async def delete_user(session: AsyncSession, user_id: int):
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
