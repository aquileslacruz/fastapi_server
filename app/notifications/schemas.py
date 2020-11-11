from typing import List
from pydantic import BaseModel
from datetime import datetime


class DrinkNotificationSimple(BaseModel):
    id: int

    class Config:
        orm_mode = True


class DrinkNotification(DrinkNotificationSimple):
    id: int
    user: str
    glasses: int
    datetime: datetime