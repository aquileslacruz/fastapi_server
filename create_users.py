import random

from app.database import SessionLocal, engine, Base
from app.users import schemas, crud

FIRST_NAMES = ['John', 'Steve', 'Michael', 'Dyrus', 'Jeremy']
LAST_NAMES = ['Michaels', 'Stevens', 'Andrews', 'Jones', 'Johnson']

# Create the DB
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if there are already users
total, _, _ = crud.get_users(db)
if total > 0:
    exit()

# Create and admin
data = {
    "username": "admin",
    "password": "admin1234"
}
crud.create_admin_user(db, schemas.UserCreate(**data))

# Create 100 users
users = []
for i in range(1, 100):
    data = {
        'first_name': random.choice(FIRST_NAMES),
        'last_name': random.choice(LAST_NAMES),
        'username': 'user{:>03}'.format(i),
        'password': '12345678'
    }
    user = crud.create_user(db, schemas.UserCreate(**data))
    users.append(user)
    print('User {} created'.format(user.username))

# Add 10-15 follows to each user
for user in users:
    size = random.choice([i for i in range(10, 15)])
    sample = random.sample(users, size)
    for person in sample:
        crud.follow_user(db, user, person.id)
