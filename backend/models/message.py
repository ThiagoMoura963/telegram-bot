import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.schemas.base import Base


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'schema': 'app'}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default='gen_random_uuid()',
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('app.users.id', ondelete='CASCADE'),
        nullable=False,
    )
    agent_id = Column(
        UUID(as_uuid=True),
        ForeignKey('app.agents.id', ondelete='CASCADE'),
        nullable=False,
    )
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    vector_message = Column(Vector(1536))
    created_at = Column(
        DateTime(timezone=True),
        server_default='now()',
        nullable=False,
    )

    agent = relationship('Agent', back_populates='messages')
    user = relationship('User', back_populates='messages')
