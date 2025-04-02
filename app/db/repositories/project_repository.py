from typing import List, Optional 

from sqlalchemy.orm import Session

from app.db.models.project import Project 
from app.db.repositories.base import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    """
    Repositório para o modelo de Projeto
    """

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Obtém uma lista de projetos por proprietário
        """
        return (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_client(
            self, db: Session, *, client_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Obtém uma lista de projetos por cliente ID
        """
        return (
            db.query(Project)
            .filter(Project.client_id == client_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_project_with_files(self, db: Session, *, project_id: int) -> Optional[Project]:
        """
        Obtém um projeto com arquivos associados
        """
        return (db.query(Project).filter(Project.id == project_id).first())

project_repository = ProjectRepository(Project)