from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''


class SimpleUser(UserBase):
    id: int
    is_active: bool
    is_admin: bool


class UserSimple(UserBase):
    first_name: str
    last_name: str


class UserId(BaseModel):
    id: int

    class Config:
        orm_mode = True


class User(SimpleUser):
    first_name: str
    last_name: str
    following: List[UserId] = []
