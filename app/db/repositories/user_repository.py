from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.user import User, UserRole
from app.db.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    Repositório para o modelo de usuario
    """

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Obtém um usuário pelo email
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_role(
            self, db: Session, *, role: UserRole, skip: int = 0, limit: int = 0 
    ) -> List[User]:
        """ 
        Obtem usuário pela função(role)
        """
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def get_clients(self, db: Session, *, skip: int = 0, limit: int = 0) -> List[User]:
        """
        Obtem clientes
        """
        return self.get_by_role(db, role=UserRole.CLIENT, skip=skip, limit=limit)
    
    def get_freelancers(self, db: Session, *, skip: int = 0, limit: int = 0) -> List[User]:
        """
        Obtem freelancers
        """
        return self.get_by_role(db, role=UserRole.FREELANCER, skip=skip, limit=limit)
    
    def get_admins(self, db: Session, *, skip: int = 0, limit: int = 0) -> List[User]:
        """
        Obtem administradores
        """
        return self.get_by_role(db, role=UserRole.ADMIN, skip=skip, limit=limit)
    
user_repository = UserRepository(User)