from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.api.v1.schemas.project import ProjectCreate, ProjectUpdate

def get(db: Session, id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def get_multi_by_owner(
    db: Session, *, owner_id: int, skip: int = 0, limit: int = 100    
) -> List[Project]:
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_multi_by_client(
        db: Session, *, client_id: int, skip: int = 0, limit: int = 100
) -> List[Project]:
    return (
        db.query(Project)
        .filter(Project.client_id == client_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create(db: Session, *, obj_in: ProjectCreate) -> Project:
    db_obj = Project(
        name=obj_in.name,
        description=obj_in.description,
        client_id=obj_in.client_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj

def create_with_owner(
        db: Session, *, obj_in: ProjectCreate, owner_id: int
) -> Project:
    db_obj = Project(
        name=obj_in.name,
        description=obj_in.description,
        owner_id=owner_id,
        client_id=obj_in.client_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj

def update(
        db: Session,
        *,
        db_obj: Project,
        obj_in: Union[ProjectUpdate, Dict[str, Any]]
) -> Project:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else: 
        update_data = obj_in.dict(exclude_unset=True)

    for field in update_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj

def remove(db: Session, *, id: int) -> Project:
    obj = db.query(Project).get(id)
    db.delete(obj)
    db.commit()

    return obj

