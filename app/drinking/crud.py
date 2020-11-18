from sqlalchemy.orm import Session
from sqlalchemy import Date, cast, func
from datetime import date
from typing import List
import os

from app.users import schemas as user_schemas
from app.users import crud as users_crud
from app.users import models as user_models
from app.notifications import crud as notifications_crud
from . import models, schemas


def add_drink(db: Session, user: user_schemas.User, glasses: int):
    # Create Drink
    drink = models.Drink(user_id=user.id, glasses=glasses)
    db.add(drink)
    db.commit()
    db.refresh(drink)

    # Notify Followers
    followers = users_crud.get_followers(db, user)
    _ = [
        notifications_crud.add_notification(db, drink, follower)
        for follower in followers
    ]

    return drink


def get_todays_drinks(db: Session, user: user_schemas.User):
    if os.getenv('ENVIRONMENT') != 'dev':
        date_filter = cast(models.Drink.datetime, Date)
    else:
        date_filter = func.DATE(models.Drink.datetime)
    
    return db.query(models.Drink).filter(
        models.Drink.user_id == user.id,
        date_filter == date.today()
        ).order_by(
            models.Drink.datetime.desc()).all()
