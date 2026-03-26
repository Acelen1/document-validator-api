from enum import Enum
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, JSON, TIMESTAMP
from database import Base
import uuid

# SQLAlchemy model
class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    worker_name = Column(String(100), nullable=False)
    training_completed = Column(Boolean, nullable=False)
    medical_certificate = Column(Boolean, nullable=False)
    status = Column(String(10), nullable=False)
    errors = Column(JSON, nullable=True)
    middle_name = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

# Enum status
class DocumentStatus(str, Enum):
    valid = "valid"
    invalid = "invalid"

# Pydantic models
class DocumentCreate(BaseModel):
    worker_name: str
    training_completed: bool
    medical_certificate: bool
    middle_name: Optional[str] = None

class DocumentUpdateRequest(BaseModel):
    worker_name: Optional[str] = None
    training_completed: Optional[bool] = None
    medical_certificate: Optional[bool] = None
    middle_name: Optional[str] = None