from sqlalchemy.orm import Session

from app.users import schemas as user_schemas
from app.users import crud as users_crud
from app.users import models as user_models
from . import models, schemas

def add_drink(db: Session, user: user_schemas.User, glasses: int):
    # Create Drink
    drink = models.Drink(user_id=user.id, glasses=glasses)
    db.add(drink)
    db.commit()
    db.refresh(drink)

    # Notify Followers
    followers = users_crud.get_followers(db, user)
    notifications = [add_notification(db, drink, follower) for follower in followers]
    return drink


def add_notification(db: Session, drink: schemas.Drink, user: user_schemas.User):
    notification = models.DrinkNotification(user_id=user.id, drink_id=drink.id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_notifications(db: Session, user: user_schemas.User):
    # Remove old ones
    db.query(models.DrinkNotification)\
        .filter(
            models.DrinkNotification.user_id == user.id, 
            models.DrinkNotification.received == True
        )\
        .delete()

    # Get the new ones
    notifications = db.query(models.DrinkNotification)\
        .filter(
            models.DrinkNotification.user_id == user.id, 
            models.DrinkNotification.received == False
        )\
        .all()
    for notification in notifications:
        notification.received = True
    
    db.commit()
    return notifications