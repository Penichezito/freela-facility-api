from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.file import File
from app.db.models.project import Project
from app.db.repositories.base import BaseRepository


class FileRepository(BaseRepository[File]):
    """
    Repository for File model.
    """

    def get_multi_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[File]:
        """
        Get files by project ID.
        """
        return (
            db.query(File)
            .filter(File.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_uploader(
        self, db: Session, *, uploader_id: int, skip: int = 0, limit: int = 100
    ) -> List[File]:
        """
        Get files by uploader ID.
        """
        return (
            db.query(File)
            .filter(File.uploader_id == uploader_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_owner_projects(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[File]:
        """
        Get files from projects owned by a user.
        """
        return (
            db.query(File)
            .join(Project, File.project_id == Project.id)
            .filter(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_client_projects(
        self, db: Session, *, client_id: int, skip: int = 0, limit: int = 100
    ) -> List[File]:
        """
        Get files from projects where a user is a client.
        """
        return (
            db.query(File)
            .join(Project, File.project_id == Project.id)
            .filter(Project.client_id == client_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


file_repository = FileRepository(File)