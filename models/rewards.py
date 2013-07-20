# -*- coding: utf-8 -*-

from common import Base
from sqlalchemy import Column, Sequence, Unicode, UnicodeText, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Reward(Base):
    ''' Reward '''

    __tablename__ = 'reward'

    id = Column(Integer, Sequence('rewards_seq', optional=True), primary_key=True)
    TYPE_VIDEO, TYPE_TEXT = range(2)
    reward_type = Column(Integer, nullable=False, default=TYPE_VIDEO)  # class discriminator
    __mapper_args__ = {'polymorphic_on': reward_type}


    created = Column(DateTime)

    #Relationships
    creator = relationship('Account')
    owner_id = Column(Integer, ForeignKey('accounts.id'))

    task = relationship('Task', backref='reward')



    def __init__(self, created=None, owner_id=None):
        self.created = created if created else datetime.utcnow()
        self.owner_id = owner_id
        self.name=name
        return id

class MMReward(Reward):
    pass

class TextReward(Reward):
    pass


