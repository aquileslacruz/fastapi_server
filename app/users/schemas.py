from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class SimpleUser(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class User(SimpleUser):
    following: List[UserBase] = []
