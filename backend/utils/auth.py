import datetime
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import database
from backend.database.crud import user as user_crud
from backend.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)  # 7 days to die :)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await user_crud.get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user


async def validate_refresh_token(token: str):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    login: str = payload.get('sub')
    return login


async def get_user_from_token(token: str, db):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception

    user = await user_crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user
