class BaseConfig:
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Development(BaseConfig):
    DATABASE_URL = 'sqlite:///./sql_app.db'
    SECRET_KEY = '6eedb27444614bbd108e047cff0535c1aada58fdaf1d6258917a9803377fffda'


def config(env='dev'):
    if env == 'dev':
        return Development
    else:
        return Development