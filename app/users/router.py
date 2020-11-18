from math import ceil
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import get_db
from app.auth import get_current_user, get_admin_user
from . import schemas, crud

router = APIRouter()

NOT_ALLOWED_EXCEPTION = HTTPException(status.HTTP_401_UNAUTHORIZED, 'You are not allowed')


# GET USERS
@router.get('/', response_model=schemas.PaginatedUser)
async def get_users(page: int = 1,
                    limit: int = 100,
                    user: schemas.User = Depends(get_admin_user),
                    db: Session = Depends(get_db)):
    total, users, max_page = crud.get_users(db, page, limit)
    data = {
        'page': page,
        'per_page': limit,
        'page_count': max_page,
        'total_count': total,
        'results': users
    }
    return schemas.PaginatedUser(**data)


# CREATE USER
@router.post('/', response_model=schemas.SimpleUser)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Username already registered")
    return crud.create_user(db=db, user=user)


# GET MY USER
@router.get('/me/', response_model=schemas.User)
async def get_my_user(user: schemas.User = Depends(get_current_user)):
    return user


# GET MY FOLLOWERS
@router.get('/followers/', response_model=List[schemas.User])
async def get_my_followers(user: schemas.User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    return crud.get_followers(db, user)


# GET THE USERS I FOLLOW
@router.get('/follow/', response_model=List[schemas.User])
async def get_my_follows(user: schemas.User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return user.following


# GET USERS BY USERNAME QUERY
@router.get('/search/', response_model=List[schemas.User])
async def search_users(user: schemas.User = Depends(get_current_user),
                       skip: int = 0,
                       limit: int = 10,
                       q: str = '',
                       db: Session = Depends(get_db)):
    return crud.search_users(db, user, q, skip, limit)


# GET USER BY ID
@router.get('/{user_id}/', response_model=schemas.User)
async def get_user(user_id: int,
                   user: schemas.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, id=user_id)


# EDIT USER
@router.put('/{user_id}/', response_model=schemas.User)
async def modify_user(user_id: int,
                      data: dict,
                      user: schemas.User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if not user.is_admin and user_id != user.id:
        raise NOT_ALLOWED_EXCEPTION 
    return crud.modify_user_by_id(db, id=user_id, data=data)


# DELETE USER
@router.delete('/{user_id}/', response_model=str)
async def delete_user(user_id: int,
                      user: schemas.User = Depends(get_admin_user),
                      db: Session = Depends(get_db)):
    crud.delete_user_by_id(db, id=user_id)
    return 'Deleted User'


# FOLLOW USER
@router.post('/{user_id}/follow/', response_model=str)
async def follow_user(user_id: int,
                      user: schemas.User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    crud.follow_user(db, user, user_id)
    return 'Added Follow'


# UNFOLLOW USER
@router.post('/{user_id}/unfollow/', response_model=str)
async def unfollow_user(user_id: int,
                        user: schemas.User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    crud.unfollow_user(db, user, user_id)
    return 'Removed Follow'