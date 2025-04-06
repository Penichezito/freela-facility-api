import json 
from typing import List, Optional, Dict, Any, Union 

from sqlalchemy.orm import Session
from app.db.models.file import File 
from app.api.v1.schemas.file import FileCreate, FileUpdate

def get(db: Session, id: int) -> Optional[File]:
    return db.query(File).filter(File.id == id).first()

def get_multi(
        db: Session, *, skip: int = 0, limit: int = 100
) -> List[File]:
    return db.query(File).offset(skip).limit(limit).all()

def get_multi_by_project(
        db: Session, *, project_id: int, skip: int = 0, limit: int = 100
) -> List[File]:
    return(
        db.query(File)
        .filter(File.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_multi_by_uploader(
    db: Session, *, uploader_id: int, skip: int = 0, limit: int = 100
) -> List[File]:
    return(
        db.query(File)
        .filter(File.uploader_id == uploader_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_multi_by_owner_projects(
    db: Session, *, obj_in: FileCreate, file_data: Dict[str, Any], uploader_id: int
) -> File:
    db_obj = File(
        filename=file_data.get("filename"),
        original_filename=file_data.get("original_filename", file_data.get("filename")),
        file_path=file_data.get("file_path"),
        file_type=file_data.get("file_type"),
        file_size=file_data.get("file_size"),
        content_type=file_data.get("content_type"),
        metadata=json.dumps(file_data.get("metadata", {})),
        uploader_id=uploader_id,
        project_id=obj_in.project_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj

def update(
        db: Session, 
        *,
        db_obj: File,
        obj_in: Union[FileUpdate, Dict[str, Any]]
) -> File:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    
    # Handle metadata as JSON
    if "metadata" in update_data and update_data["metadata"]:
        update_data["metadata"] = json.dumps(update_data["metadata"])

    for field in update_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj

def remove(db: Session, *, id: int) -> File:
    obj = db.query(File).get(id)
    db.delete(obj)
    db.commit()
    
    return obj
        