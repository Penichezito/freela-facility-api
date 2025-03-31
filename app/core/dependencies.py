from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User, UserRole
from app.core.security import get_current_active_user

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Valida que o usuário atual é um administrador.
    Se não for, levanta uma exceção HTTP 403 (Forbidden).
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissão de admin",
        )
    return current_user

def get_current_freelancer_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Valida que o usuário atual é um freelancer.
    Se não for, levanta uma exceção HTTP 403 (Forbidden).
    """
    if current_user.role != UserRole.FREELANCER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissão de freelancer",
        )
    return current_user

def get_current_client_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Valida que o usuário atual é um cliente.
    Se não for, levanta uma exceção HTTP 403 (Forbidden).
    """
    if current_user.role != UserRole.CLIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissão de cliente",
        )
    return current_user

def get_current_admin_or_freelancer_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Valida que o usuário atual é um administrador ou freelancer.
    Se não for, levanta uma exceção HTTP 403 (Forbidden).
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.FREELANCER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui nenhuma permissão",
        )
    return current_user