from sqlalchemy.orm import Session
from typing import List

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
    _ = [notifications_crud.add_notification(db, drink, follower) for follower in followers]
    
    return drink