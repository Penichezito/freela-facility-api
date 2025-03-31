from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.db.models.user import User

# Shared properties
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

# Properties to receive via API on creation
class ProjectCreate(ProjectBase):
    client_id: int

# Properties to receive via API on update
class ProjectUpdate(ProjectBase):
    pass

# Properties to return via API
class Project(ProjectBase):
    id: int
    owner_id: int
    client_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return via API with owner and client details
class ProjectDetail(Project):
    owner: "User"
    client: "User"
    file_count: int

    class Config:
        orm_mode = True
