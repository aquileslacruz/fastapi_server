from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Drink(Base):
    __tablename__ = 'drinks'

    id = Column(Integer, primary_key=True, index=True)
    glasses = Column(Integer)
    datetime = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    user = relationship('User')