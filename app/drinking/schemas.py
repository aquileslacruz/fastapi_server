from typing import List
from pydantic import BaseModel
from datetime import datetime


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