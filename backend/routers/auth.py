from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import user as user_schema
from backend.database.crud import user as user_crud
from backend.database.database import get_db
from backend.utils.security import hash_password, verify_password
from backend.utils.auth import security
from backend.config import settings

router = APIRouter(prefix='/api/auth', tags=['auth'])


@router.post('/register', response_model=user_schema.User)
async def register(user: user_schema.UserCreate, session: AsyncSession = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password.get_secret_value())
        new_user = await user_crud.create_user(session, user.username, hashed_password)
        return new_user
    except ValueError:
        raise HTTPException(status_code=400, detail='Username already exists')


@router.post('/login', response_model=user_schema.User)
async def login(credentials: user_schema.UserCreate, response: Response, session: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_username(session, credentials.username)

    if not user:
        raise HTTPException(status_code=400, detail='Invalid username or password')

    if not verify_password(credentials.password.get_secret_value(), user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid username or password')

    access_token = security.create_access_token(uid=str(user.id))
    refresh_token = security.create_refresh_token(uid=str(user.id))

    response.set_cookie(settings.JWT_ACCESS_TOKEN_NAME, access_token)
    response.set_cookie(settings.JWT_REFRESH_TOKEN_NAME, refresh_token)

    return user