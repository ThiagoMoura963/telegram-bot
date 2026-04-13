from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from backend.schemas.base import Base

class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    file_name = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    document_id = Column(UUID(as_uuid=True), ForeignKey("app.documents.id"), nullable=False)
    content = Column(String, nullable=False)
    

    content_vector = Column(Vector(1536), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="chunks")