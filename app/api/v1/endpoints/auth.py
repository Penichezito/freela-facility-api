from datetime import timedelta
from typing import Any 

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.schemas.token import Token
from app.api.v1.schemas.user import User, UserCreate
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
) 

from app.config import settings
from app.db.database import get_db
from app.db.models.user import User as UserModel
from app.services import user_service

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth Token de Login Compatível, get para acesso do token para futuras requisições
    """

    # Autenticação usuário
    user = user_service.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    
    # Gerando Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=User)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """ Registrar novo usuário"""
    # Verificando se o email já está cadastrado
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Um usuário com este email já existe no sistema")
    
    # Criando novo usuário
    user = user_service.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=User)
def read_users_me(
    current_user: UserModel = Depends(get_current_user),
) -> Any:
    """Receber usuário atual"""
    return current_user