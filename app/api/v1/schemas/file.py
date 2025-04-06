from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Shared Properties
class FileBase(BaseModel):
    filename: str
    project_id: int

# Properties to receive via API on creation
class FileCreate(FileBase):
    pass

# Properties to receive via API on update
class FileUpdate(BaseModel):
    filename: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# Properties to return via API
class File(FileBase):
    id: int
    original_filename: str
    file_type: str
    file_size: int
    content_type: str
    metadata: Optional[Dict[str, Any]] 