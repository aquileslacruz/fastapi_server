from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relation, relationship

from app.database import Base

following = Table(
    'following', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('follow_id', Integer, ForeignKey('users.id'), index=True),
    UniqueConstraint('user_id', 'follow_id', name='unique_following'))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, default='')
    last_name = Column(String, default='')
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    following = relation('User',
                         secondary=following,
                         primaryjoin=following.c.user_id == id,
                         secondaryjoin=following.c.follow_id == id)

    def get_name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.username