# -*- coding: utf-8 -*-

from common import Base
from sqlalchemy import Column, Sequence, Unicode, UnicodeText, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
import datetime

class Reward(Base):
    ''' Reward '''

    __tablename__ = 'reward'

    id = Column(Integer, Sequence('rewards_seq', optional=True), primary_key=True)
    name = Column(String(50));

    text = Column(String(400));
    media_url = Column(String(400));
    media_length = Column(Integer);

    TYPE_VIDEO, TYPE_MUSIC, TYPE_TEXT = range(3)
    reward_type = Column(Integer, nullable=False, default=TYPE_TEXT)  # class discriminator
    __mapper_args__ = {'polymorphic_on': reward_type}
    created_time = Column(DateTime)



    #Relationships
#    creator = relationship('Account')
#    owner_id = Column(Integer, ForeignKey('accounts.id'))
#    task = relationship('Task')
    creator = relationship('User')
    owner_id = Column(Integer, ForeignKey('users.id'))



    def __init__(self, name, owner_id=None):
        self.created_time = datetime.utcnow()
        self.owner_id = owner_id
        self.name=name
        return id

    def set_reward_values(self, text=None,media_url=None,media_length=None):
        if (text==None and media_url==None and media_length==None):
            return False
        if (text != None):
            self.text = text
        if (media_url != None):
            self.media_url = media_url
        if (media_length != None):
            self.media_length = media_length
        return self.id

class Video_Reward(Reward):

    def __init__(self,name,)
    pass

class Music_Reward(Reward):
    pass

class TextReward(Reward):
    pass


