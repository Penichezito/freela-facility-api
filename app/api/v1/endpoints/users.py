from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.v1.schemas.user import User, UserCreate, UserUpdate
from app.core.security import get_current_active_user, get_password_hash
from app.db.database import get_db
from app.db.models.user import User as UserModel, UserRole
from app.services import user_service

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """ 
    Recuperar usuário
    """
    # Se o usuário não for admin, ele só pode ver seu próprio usuário
    if current_user.role != UserRole.ADMIN:
        users =  [current_user]
    else:
        users = user_service.get_multi(db=db, skip=skip, limit=limit)
    
    return users

@router.get("/clients", response_model=List[User])
def read_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """ 
    Recuperar clientes. Apenas para Freelancers e administradores.
    """
    if current_user.role not in [UserRole.FREELANCER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBBIDDEN,
            detail="Permissão negada. Apenas Freelancers e administradores podem ver clientes."
        )
    
    # Obter todos os usuários com o papel de cliente
    clients = user_service.get_multi_by_role(
        db=db, role=UserRole.CLIENT, skip=skip, limit=limit
    )

    return clients

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Cria um novo usuário. Apenas admins podem criar outros usuarios com papel de admin.
    """
    # Checa se o usuário existe
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Um usuário com esse email já existe no sistema.",
        )
    
    # Checa as permissões do usuário atual
    if user_in.role == UserRole.ADMIN and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para criar novos usuários com papel de admin.",
        )
    
    # Cria um novo usuário
    user = user_service.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=User)
def read_user_me(
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """ 
    Recuperar usuário atual.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    full_name: str = Body(None),
    password: str = Body(None),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """ 
    Atualizar usuário atual.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)

    if full_name is not None:
        user_in.full_name = full_name
    if password is not None:
        user_in.password = password

    user = user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Obtem um usuario específico pelo ID
    """
    user = user_service.get(db, id=user_id)
    if user == current_user:
        return user
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nenhuma permissão para ver esse usuário",
        )
    return user

@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Atualiza o usuário. Apenas administradores podem atualizar outros usuários.
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="O usuário com esse username não existe no sistema",
        )
    
    # Check permissions
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nenhuma permissão para atualizar esse usuário",
        )
    
    # Admin can't change their own role
    if (
        current_user.id == user_id and 
        user_in.role is not None and 
        user_in.role != current_user.role
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode mudar seu próprio papel",
        )
    
    user = user_service.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Deleta um usuário. Apenas administradores podem deletar outros usuários.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nenhuma permissão para deletar esse usuário",
        )
    
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="O usuário com esse id e username não existe no sistema",
        )
    
    # Admin can't delete themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode deletar a si mesmo",
        )
    
    user = user_service.remove(db, id=user_id)
    return user