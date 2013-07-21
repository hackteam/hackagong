import sqlalchemy, random
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
    name = Column(String(100), default=None)
    email = Column(String(100), default=None)
    picture = Column(String(20), default=None)

    created = Column(DateTime)
    last_login = Column(DateTime)

    def __init__(self, username=None,
                  password=None,
                 created=None, last_login=None):
        self.username = username
        self.password = password
        self.created = datetime.utcnow()
        self.last_login = last_login
        self.picture = "profile_picture_%s.png" %(random.randint(1,4))

    def set_details(self,username=None,password=None,name=None,email=None):
        if (username):
            self.username = username
        if (password):
            self.password = password
        if (name):
            self.name = name
        if (email):
            self.email = email

