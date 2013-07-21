# -*- coding: utf-8 -*-

from common import Base
from sqlalchemy import Column, Sequence, Unicode, UnicodeText, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime


class Reward(Base):
    ''' Reward '''

    __tablename__ = 'reward'

    id = Column(Integer, Sequence('rewards_seq', optional=True), primary_key=True)
    name = Column(String(50));

    text = Column(String(400));
    media_url = Column(String(400));
    media_length = Column(Integer);

    TYPE_VIDEO, TYPE_IMAGE, TYPE_MUSIC, TYPE_TEXT = range(4)
    reward_type = Column(Integer, nullable=False, default=TYPE_TEXT)  # class discriminator
    __mapper_args__ = {'polymorphic_on': reward_type}
    created_time = Column(DateTime)



    #Relationships
#    creator = relationship('Account')
#    owner_id = Column(Integer, ForeignKey('accounts.id'))
#    task = relationship('Task')
    creator = relationship('User',backref='reward')
    owner_id = Column(Integer, ForeignKey('users.id'))



    def __init__(self, name, owner_id=None):
        self.created_time = datetime.utcnow()
        self.owner_id = owner_id
        self.name=name

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


class VideoReward(Reward):
    __tablename__ = 'video_rewards'
    __mapper_args__ = {'polymorphic_identity': Reward.TYPE_VIDEO}
    id = Column(Integer, ForeignKey('reward.id'), primary_key=True)



class MusicReward(Reward):
    __tablename__ = 'music_rewards'
    __mapper_args__ = {'polymorphic_identity': Reward.TYPE_MUSIC}
    id = Column(Integer, ForeignKey('reward.id'), primary_key=True)


class TextReward(Reward):
    __tablename__ = 'text_rewards'
    __mapper_args__ = {'polymorphic_identity': Reward.TYPE_TEXT}
    id = Column(Integer, ForeignKey('reward.id'), primary_key=True)



class ImageReward(Reward):
    __tablename__ = 'image_rewards'
    __mapper_args__ = {'polymorphic_identity': Reward.TYPE_IMAGE}
    id = Column(Integer, ForeignKey('reward.id'), primary_key=True)

