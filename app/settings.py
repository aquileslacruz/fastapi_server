import os


class BaseConfig:
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Development(BaseConfig):
    DATABASE_URL = 'sqlite:///./sql_app.db'
    SECRET_KEY = '6eedb27444614bbd108e047cff0535c1aada58fdaf1d6258917a9803377fffda'

    @property
    def path(self):
        return self.DATABASE_URL


class Production(BaseConfig):
    DB_PORT = os.getenv('POSTGRES_PORT')
    DB_NAME = os.getenv('POSTGRES_DB')
    DB_HOST = os.getenv('POSTGRES_HOST')
    DB_LOGIN = os.getenv('POSTGRES_USER')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')

    @property
    def path(self):
        return f'postgres://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


def config(env='dev'):
    if env == 'dev':
        return Development()
    elif env == 'prod':
        return Production()
    else:
        return Development()