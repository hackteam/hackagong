import sqlalchemy
from sqlalchemy import Column, ForeignKey, Sequence, \
    Integer, String, Boolean, DateTime, Unicode
from sqlalchemy.orm import relationship, backref

from common import Base, db_session
import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, Sequence('tasks_id_seq', optional=True), primary_key=True)
    date_created = Column(DateTime)
    date_completed = Column(DateTime,default=None)
    date_cancelled = Column(DateTime, default=None)
    name = Column(String(50))
    description = Column(String(500))
    todo_list_id = Column(Integer, ForeignKey('todo_list.id'))
    user_created_id = Column(Integer, ForeignKey('accounts.id'))
    user_reviewer_id = Column(Integer, ForeignKey('accounts.id'))
    # reward_id = relationship("Reward")

    def __init__(self, name, creator, reviewer, reward, description=None):
        self.date_created = datetime.utcnow()
        self.name = name
        self.description = description
        self.user_created_id = creator
        self.user_reviewer_id = reviewer
        self.reward_id = reward
        return self.id

    def complete_task(self):
        self.date_completed = datetime.utcnow()
        return self.id

    def modify_task(self, name,description):
        self.name = name
        self.description = description
        return self.id

    def cancel_task(self):
        self.date_cancelled = datetime.utcnow()
        return self.id

