from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class ApplicationError(Exception):
    """
    Classe para 
    """
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Um erro inesperado ocorreu"
    headers: Optional[Dict[str, Any]] = None

    def __init__(
        self, 
        detail: Optional[str] = None,
        status_code: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code
        self.headers = headers
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        """
        Converte para FastAPI HTTPException.
        """
        return HTTPException(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )


class NotFoundError(ApplicationError):
    """
    Resource not found exception.
    """
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Recurso não encontrado"


class AuthenticationError(ApplicationError):
    """
    Erro de autenticação do Authentication
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "As credenciais não puderam ser ativadas"
    headers = {"WWW-Authenticate": "Bearer"}


class PermissionError(ApplicationError):
    """
    Permission error. User does not have required permissions.
    """
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not enough permissions"


class ValidationError(ApplicationError):
    """
    Data validation error.
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Validation error"


class DuplicateError(ApplicationError):
    """
    Resource already exists error.
    """
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists"


class ExternalServiceError(ApplicationError):
    """
    External service error (e.g. API call to file processor).
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Error in external service"