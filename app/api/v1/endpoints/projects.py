from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from app.api.v1.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectDetail
from app.core.security import get_current_active_user
from app.db.database import get_db 
from app.db.models.user import User, UserRole
from app.services import project_service

router = APIRouter()

@router.post("/", response_model=Project)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any: 
    """
    Endpoint para criar um novo Projeto.
    Apenas Freelancers podem criar projetos.
    """
    if current_user.role != UserRole.FREELANCER:
        raise HTTPException(
            status_code=403,
            detail="Apenas Freelancers podem criar projetos"
        )
    
    # Criando projeto
    project = project_service.create_with_owner(
        db=db, 
        obj_in=project_in, 
        owner_id=current_user.id
    )
    return project

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """ 
    Endpoint para Recuperar projetos 
    Freelancers podem ver todos os seus próprios projetos.
    Clientes pode ver todos os projetos em que eles fazem parte.
    """
    if current_user.role == UserRole.FREELANCER:
        projects = project_service.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    else:
        projects = project_service.get_multi_by_client(
            db=db, client_id=current_user, skip=skip, limit=limit
        )
    
    return projects
@router.get("/{project_id}", response_model=ProjectDetail)
def read_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Endpoint para Recuperar um projeto específico pelo ID.
    Freelancers podem ver todos os seus próprios projetos.
    """
    project = project_service.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Check if user has permission to view the project
    if (current_user.role == UserRole.FREELANCER and project.owner_id != current_user.id) or \
       (current_user.role == UserRole.CLIENT and project.client_id != current_user.id):
        raise HTTPException(status_code=403, detail="Você não tem permissão para visualizar este projeto")
    
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """ 
    Endpoint para Atualizar Projeto.
    Apenas o proprietário do projeto (Freelancer) pode atualizá-lo.
    """
    project = project_service.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Checando se o usuário tem permissão para atualizar o projeto
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Você não tem permissão para atualizar este projeto")
    
    project = project_service.update(db=db, db_obj=project, obj_in=project_in)
    
    return project

@router.delete("/{project_id}", response_model=Project)
def delete_project (
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """ 
    Endpoint para Deletar um projeto 
    Apenas o proprietário do projeto (Freelancer) pode deletar um projeto
    """
    project = project_service.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Checando se o usuário tem permissão para deletar o projeto
    if project_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar este projeto")
    
    project = project_service.remove(db=db, id=project_id)

    return project
