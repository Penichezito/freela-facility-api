from sqlalchemy import Boolean, Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

import enum

class UserRole(str, enum.Enum):
    FREELANCER = "freelancer"
    CLIENT = "client"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    projects_owned = relationship("Project", back_populates="owner", foreign_keys="Projects.owner_id")
    projects_client = relationship("Project", back_populates="client", foreing_keys="Project.client_id")
    files = relationship("File", back_populates="uploader")
    
