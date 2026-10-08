import enum
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TranslationStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TranslationRequest(Base):
    __tablename__ = "translation_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, nullable=False)
    source_text = Column(Text, nullable=False)
    file_path = Column(String, nullable=True)
    target_lang = Column(String, nullable=False)
    translated_text = Column(Text, nullable=True)
    status = Column(Enum(TranslationStatus), nullable=False, default=TranslationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error_log = Column(Text, nullable=True)
