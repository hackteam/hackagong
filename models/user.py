import sqlalchemy
from sqlalchemy import Column, ForeignKey, Sequence, \
    Integer, String, Boolean, DateTime, Unicode
from sqlalchemy.orm import relationship, backref

from common import Base, db_session
import datetime

class Account(Base):
    ''' Account '''

    __tablename__ = 'accounts'

    id = Column(Integer, Sequence('users_id_seq', optional=True), primary_key=True)

    USER, ADMIN = range(2)
    ROLES = (USER,ADMIN)
    ROLE_NAMES = (u'User', u'Admin')

    role = Column(Integer, nullable=False, default=USER)  # class discriminator
    __mapper_args__ = {'polymorphic_on': role}

    username = Column(Unicode(30), unique=True, nullable=False)

    given_name = Column(Unicode(40), nullable=False)
    family_name = Column(Unicode(40), nullable=False)

    full_name = property(
        lambda self: unicode(self.given_name) + u' '
        + unicode(self.family_name),
        None)

    password_hash = Column(String(60), nullable=False)

    def set_password(self, password):
        self.password_hash = hash_password(password) if password else None

    password = property(None, set_password)

    created = Column(DateTime)
    last_login = Column(DateTime)

    def __init__(self, username=None,
                 given_name=None, family_name=None,
                 password_hash=None, password=None,
                 role=USER,
                 created=None, last_login=None):
        self.username = username
        self.given_name = given_name
        self.family_name = family_name
        self.password_hash = password_hash
        if password:
            self.password = password
        self.role = role
        self.created = created if created else datetime.utcnow()
        self.last_login = last_login

    def __unicode__(self):
        return u'<%s: %s "%s"%s>' % (self.__class__.__name__,
            self.username, self.full_name)

    def __str__(self):
        return unicode(self).encode('utf-8')

class User(Account):
    ''' Normal User '''

    __tablename__ = 'users'
    __mapper_args__ = {'polymorphic_identity': Account.USER}

    id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)

    email = Column(Unicode(100))
    phone = Column(Unicode(100))

    # relationships

    def __init__(self, username=None,
                 given_name=None, family_name=None,
                 password_hash=None, password=None,
                 created=None, last_login=None,
                 email=None, phone=None):
        super(Account, self).__init__(username=username,
             given_name=given_name, family_name=family_name,
             password_hash=password_hash, password=password,
             role=Account.USER,
             created=created, last_login=last_login)
        self.email = email
        self.phone = phone

