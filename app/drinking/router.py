from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import get_db
from app.auth import get_current_user
from app.users import schemas as user_schemas
from . import schemas, crud

router = APIRouter()


# GET ALL MY DRINKING
@router.get('/', response_model=List[schemas.DrinkSimple])
def get_my_drinks(user: user_schemas.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    return user.drinks


# ADD A DRINK
@router.post('/', response_model=schemas.Drink)
def add_drink(drink: schemas.DrinkCreate,
              user: user_schemas.User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    return crud.add_drink(db, user, drink.glasses)


# GET TODAY'S DRINKS
@router.get('/today/', response_model=List[schemas.Drink])
def get_todays_drinks(user: user_schemas.User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    return crud.get_todays_drinks(db, user)