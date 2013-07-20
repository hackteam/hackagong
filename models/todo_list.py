# -*- coding: utf-8 -*-

from common import Base

from sqlalchemy import Column, Sequence, Unicode, UnicodeText, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Todo(Base):
    ''' Todo list '''

    __tablename__ = 'todo_list'

    id = Column(Integer, Sequence('todo_list_seq', optional=True), primary_key=True)
    
    name = Column(Unicode(100), nullable=False)    
    owner_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime)

    #Relationships
    owner = relationship('User', backref='todo_list')
    tasks = relationship('Task', cascade='all, delete-orphan')



    def __init__(self, created=None, owner_id=None,name=None):
        self.created = created if created else datetime.utcnow()
        self.owner_id = owner_id
        self.name=name
        return id


