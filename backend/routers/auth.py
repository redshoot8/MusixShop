import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from backend.schemas import user as user_schema
from backend.utils import auth
from backend.database import database
from backend.database.crud import user as user_crud
from backend.config import settings

router = APIRouter(prefix='/api/auth')


@router.post('/register', response_model=user_schema.User)
async def register_user(user: user_schema.UserCreate, db: AsyncSession = Depends(database.get_db)):
    try:
        db_user = await user_crud.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail='Login already registered')

        hashed_password = auth.pwd_context.hash(user.password.get_secret_value())
        db_user = await user_crud.create_user(db, user.email, hashed_password)

        return db_user

    except HTTPException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post('/login')
async def login_for_access_token(
        response: JSONResponse,
        user: user_schema.UserCreate,
        db: AsyncSession = Depends(database.get_db)
):
    try:
        user = await auth.authenticate_user(db, user.email, user.password.get_secret_value())
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={'sub': user.email}, expires_delta=access_token_expires
        )

        refresh_token = auth.create_refresh_token(data={'sub': user.email})

        response.set_cookie(
            key='access_token',
            value=f'Bearer {access_token}',
            httponly=True,
            secure=True,
            samesite='strict'
        )

        response.set_cookie(
            key='refresh_token',
            value=f'Bearer {refresh_token}',
            httponly=True,
            secure=True,
            samesite='strict'
        )

        return {'access_token': access_token, 'refresh_token': refresh_token}

    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post('/refresh')
async def login_with_refresh_token(
        response: JSONResponse,
        refresh_token: str | None = Header(None),
        db: AsyncSession = Depends(database.get_db)
):
    try:
        refresh_token = refresh_token.replace('Bearer ', '')

        email = await auth.validate_refresh_token(refresh_token)
        if email is None:
            raise HTTPException(status_code=401, detail='Invalid refresh token')
        user = await user_crud.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail='User not found')

        access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
        response.set_cookie(key='access_token', value=f'Bearer {access_token}', httponly=True)

        return {'access_token': access_token, 'token_type': 'bearer'}

    except HTTPException as exc:
        print(f'Возникла ошибка HTTP: {str(exc)}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.get('/email')
async def get_email(db: AsyncSession = Depends(database.get_db), access_token: str | None = Header(None)):
    access_token = access_token.replace('Bearer ', '')
    user = await auth.get_user_from_token(access_token, db)
    return {'email': user.email}
