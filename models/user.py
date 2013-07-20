import sqlalchemy
from sqlalchemy import Column, ForeignKey, Sequence, \
    Integer, String, Boolean, DateTime, Unicode
from sqlalchemy.orm import relationship, backref

from common import Base, db_session
from datetime import datetime
class User(Base):
    ''' Account '''

    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq', optional=True), primary_key=True)

    username = Column(Unicode(30), unique=True, nullable=False)

    password = Column(Unicode(40),nullable=False)



    created = Column(DateTime)
    last_login = Column(DateTime)

    def __init__(self, username=None,
                  password=None,
                 created=None, last_login=None):
        self.username = username
        self.password = password
        self.created = datetime.utcnow()
        self.last_login = last_login


