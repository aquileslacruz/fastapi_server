from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import get_db
from app.auth import get_current_user, get_admin_user
from . import schemas, crud

router = APIRouter()


@router.get('/', response_model=List[schemas.SimpleUser])
async def get_users(user: schemas.User = Depends(get_admin_user), skip: int = 0, 
                    limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@router.post('/', response_model=schemas.SimpleUser)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get('/search', response_model=List[schemas.SimpleUser])
async def search_users(user: schemas.User = Depends(get_current_user), skip: int = 0,
                       limit: int = 10, q: str = '', db: Session = Depends(get_db)):
    return crud.search_users(db, user, q, skip, limit)


@router.get('/me', response_model=schemas.User)
async def get_my_user(user: schemas.User = Depends(get_current_user)):
    return user


@router.get('/follow', response_model=List[schemas.SimpleUser])
async def get_my_follows(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user.following


@router.post('/follow', response_model=schemas.User)
async def create_follow(followee: schemas.UserBase, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.add_follow(db, user, followee.username)


@router.get('/{user_id}', response_model=schemas.SimpleUser)
async def get_user(user_id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, id=user_id)


@router.post('/{user_id}/follow', response_model=str)
async def follow_user(user_id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.follow_user(db, user, user_id)
    return 'Added Follow'


@router.post('/{user_id}/unfollow', response_model=str)
async def unfollow_user(user_id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.unfollow_user(db, user, user_id)
    return 'Removed Follow'