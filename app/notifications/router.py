from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import get_db
from app.auth import get_current_user
from app.users import schemas as user_schemas
from . import schemas, crud

router = APIRouter()


# GET ALL MY NOTIFICATIONS
@router.get('/', response_model=List[schemas.DrinkNotification])
async def get_notifications(
        user: user_schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db, user)
    return [{
        'id': notification.id,
        'user': notification.drink.user.get_name(),
        'glasses': notification.drink.glasses,
        'datetime': notification.drink.datetime
    } for notification in notifications]


# REMOVE NOTIFICATION BY ID
@router.delete('/{notification_id}/')
async def remove_notification(
    notification_id: int,
    user: user_schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    crud.remove_notification(db=db, id=notification_id, user=user)
    return 'Notification Removed'