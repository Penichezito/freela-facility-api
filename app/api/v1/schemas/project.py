from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

# Properties to receive via API on creation
class ProjectsCreate(ProjectBase):
    cliente_id: int

# Properties to receive via API on update
class ProjectsUpdate(ProjectBase):
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

# Properties to return via API with owener and client details
class ProjectDetail(Project):
    owner: "User"
    client: "User"
    file_count: int

    class Config:
        orm_mode = True