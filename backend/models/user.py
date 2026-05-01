from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.schemas.base import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'app'}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    agents = relationship('Agent', back_populates='owner')
    messages = relationship('Message', back_populates='user')


class Agent(Base):
    __tablename__ = 'agents'
    __table_args__ = {'schema': 'app'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    instruction = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('app.users.id'))

    messages = relationship('Message', back_populates='agent')
    owner = relationship('User', back_populates='agents')
