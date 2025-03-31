from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_current_active_user
from app.core.dependencies import (
    get_current_admin_user,
    get_current_freelancer_user,
    get_current_client_user,
    get_current_admin_or_freelancer_user,
)
from app.db.database import get_db
from app.db.models.user import User

# Re-export dependencies for use in API endpoints
__all__ = [
    "get_db",
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "get_current_freelancer_user",
    "get_current_client_user",
    "get_current_admin_or_freelancer_user",
]