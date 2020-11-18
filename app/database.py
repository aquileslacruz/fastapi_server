import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import config

environment = os.getenv('ENVIRONMENT', 'dev')

configuration = config(environment)
connect_args = {} if environment != 'dev' else {'check_same_thread': False}

engine = create_engine(configuration.path, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()