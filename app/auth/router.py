from datetime import datetime, timedelta
from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app import settings, get_db
from . import config, authenticate_user, create_access_token, schemas, get_current_user
from app.users import schemas as user_schemas

router = APIRouter()
security = HTTPBasic()

LOGIN_EXCEPTION = HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail='Incorrect username or password',
                                headers={"WWW-Authenticate": "Bearer"})


# USE TOKEN TO GET A NEW ONE
@router.get('/', response_model=schemas.Token)
async def reload(user: user_schemas.User = Depends(get_current_user)):
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username},
                                       expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


# GET A NEW TOKEN USING USERNAME AND PASSWORD
@router.post('/', response_model=schemas.Token)
async def login(credentials: HTTPBasicCredentials = Depends(security),
                db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise LOGIN_EXCEPTION
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username},
                                       expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
