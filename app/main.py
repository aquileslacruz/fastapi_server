from fastapi import FastAPI

from .database import engine, Base
from .auth.router import router as auth_router
from .users.router import router as users_router
from .drinking.router import router as drinking_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Auth Routes
app.include_router(
    auth_router,
    prefix='/token',
    tags=['auth'],
    responses={404: {'description': 'Not Found'}}
)

# User Routes
app.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not Found'}}
)

# Drink Routes
app.include_router(
    drinking_router,
    prefix='/drinks',
    tags=['drinks'],
    responses={404: {'description': 'Not Found'}}
)