from datetime import datetime, timedelta
from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import settings, get_db
from . import config, authenticate_user, create_access_token, schemas, get_current_user
from app.users import schemas as user_schemas


router = APIRouter()

LOGIN_EXCEPTION = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect username or password',
    headers={"WWW-Authenticate": "Bearer"}
)


@router.get('/', response_model=schemas.Token)
async def reload(user: user_schemas.User = Depends(get_current_user)):
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.post('/', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise LOGIN_EXCEPTION
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }