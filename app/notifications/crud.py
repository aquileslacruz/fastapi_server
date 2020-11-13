from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.users import schemas as user_schemas
from app.drinking import schemas as drink_schemas
from . import models, schemas

NOTIFICATION_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail='The notification was not found')


def add_notification(db: Session, drink: drink_schemas.Drink,
                     user: user_schemas.User):
    notification = models.DrinkNotification(user_id=user.id, drink_id=drink.id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def remove_notification(db: Session, id: int, user: user_schemas.User):
    notification = db.query(models.DrinkNotification)\
        .filter(
            models.DrinkNotification.user_id == user.id,
            models.DrinkNotification.id == id
        )
    if not notification:
        raise NOTIFICATION_NOT_FOUND
    notification.delete()
    db.commit()
    return True


def get_notifications(db: Session, user: user_schemas.User):
    notifications = db.query(models.DrinkNotification)\
        .filter(
            models.DrinkNotification.user_id == user.id,
            models.DrinkNotification.received == False
        )\
        .order_by(models.DrinkNotification.datetime.desc())\
        .all()
    db.commit()
    return notifications