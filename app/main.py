from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .auth.router import router as auth_router
from .users.router import router as users_router
from .drinking.router import router as drinking_router
from .notifications.router import router as notifications_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Routes
app.include_router(auth_router,
                   prefix='/token',
                   tags=['auth'],
                   responses={404: {
                       'description': 'Not Found'
                   }})

# User Routes
app.include_router(users_router,
                   prefix='/users',
                   tags=['users'],
                   responses={404: {
                       'description': 'Not Found'
                   }})

# Drink Routes
app.include_router(drinking_router,
                   prefix='/drinks',
                   tags=['drinks'],
                   responses={404: {
                       'description': 'Not Found'
                   }})

# Notification Routes
app.include_router(notifications_router,
                   prefix='/notifications',
                   tags=['notifications'],
                   responses={404: {
                       'description': 'Not Found'
                   }})
