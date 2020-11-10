from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.users import schemas as user_schemas


class DrinkBase(BaseModel):
    glasses: int


class DrinkCreate(DrinkBase):
    pass


class DrinkSimple(DrinkBase):
    datetime: datetime

    class Config:
        orm_mode = True


class Drink(DrinkSimple):
    id: int


class DrinkNotificationSimple(BaseModel):
    id: int
    user: str
    glasses: int
    datetime: datetime


class IdList(BaseModel):
    id_list: List[int]