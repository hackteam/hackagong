from config import BASE_URL_PATH, DB_NAME

from sqlalchemy import create_engine, types, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.types import TypeDecorator, VARCHAR

engine = create_engine(BASE_URL_PATH+DB_NAME,echo=True)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

def db_init():
    Base.metadata.create_all(engine)


def db_session(close=False):
    dbs = Session()
    # deal with "ghost" object issues caused by updates in other threads
    if close:
        dbs.close()
    return dbs

