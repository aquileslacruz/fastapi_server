from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import get_db
from app.auth import get_current_user
from . import schemas, crud

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get('/me', response_model=schemas.User)
async def get_my_user(user: schemas.User = Depends(get_current_user)):
    return user