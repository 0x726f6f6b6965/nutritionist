from sqlalchemy import create_engine
from os import environ

__user = environ.get('POSTGRES_USER')
__password = environ.get('POSTGRES_PASSWORD')
__db = environ.get('POSTGRES_DB')
__port = environ.get('POSTGRES_PORT', 5432)
__host = environ.get('POSTGRES_HOST', 'localhost')

engine = create_engine(f'postgresql://{__user}:{__password}@{__host}:{__port}/{__db}', echo=True)
