import json
from typing import Any, List, Optional 
import httpx

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form, Query
from sqlalchemy.orm import Session

from app.api.v1.schemas.file import File, FileCreate, FileUpdate, FileDetail
from app.core.security import get_current_active_user
from app.db.database import get_db
from app.db.models.user import User, UserRole
from app.services import file_service, project_service
from app.config import settings

router = APIRouter()

@router.post("/upload/", response_model=File)
async def upload_file(
    *,
    db: Session = Depends(get_db),
    project_id: int = Form(...),
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload de arquivo para um projeto
    
    Clientes pode dar upload de arquivos em seus projetos.
    Freelancers pode dar Upload de arquivos em projetos que eles são donos/estão trabalhando.
    """

    # Get the project
    project = project_service.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # Checar se o usuário tem autorização para dar upload de arquivos neste projeto
    if (current_user.role == UserRole.FREELANCER and project.owner_id != current_user.id) or \
       (current_user.role == UserRole.CLIENT and project.client_id != current_user.id):
        raise HTTPException(status_code=403, detail="Usuário não autorizado a dar upload de arquivos neste projeto")
    
    # Ler conteúdo do arquivo
    file_content = await file.read()

    # Preparar dados para o upload do arquivo
    file_data = {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(file_content),
        "project_id": project_id,
        "uploader_id": current_user.id,
    }

    # Enviar o arquivo para o serviço de armazenamento
    try:
        async with httpx.AsyncClient() as client:
            files = {"file": (file.filename, file_content, file.content_type)}
            data = {"metadata": json.dumps(file_data)}

            response = await client.post(
                f"{settings.FILE_PROCESSOR_URL}/api/files/upload",
                files=files,
                json=data,
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erro ao processar o arquivo: {response.text}",
                )

            # Obter a resposta do processador de arquivos
            file_data = response.json()

            # Criar arquivo e gravar no banco de dados
            file_in = FileCreate(
                filename=file_data["filename"],
                project_id=project_id,
            )

            file_obj = file_service.create(
                db=db, 
                obj_in=file_in, 
                uploader_id=current_user.id
            )

            return file_obj
    
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Erro na comunicação com o processador de arquivos: {str(exc)}",
        )
    
@router.get("/", response_model=List[File])
def read_files(
    db: Session = Depends(get_db),
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """ 
    Recuperação de arquivos

    Caso o id do projeto seja fornecido, obtenha os arquivos do projeto,
    Caso contrário, pegue todos os arquivos que o usuário tem acesso.
    """
    if project_id:
        project = project_service.get(db=db, id=project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
        # Checar se o usuário tem autorização para ver os arquivos deste projeto
        if (current_user.role == UserRole.FREELANCER and project.owner_id != current_user.id) or \
           (current_user.role == UserRole.CLIENT and project.client_id != current_user.id):
            raise HTTPException(status_code=403, detail="Usuário não autorizado a ver os arquivos deste projeto")
        
        # Recuperar arquivos do projeto
        files = file_service.get_multi_by_project(
            db=db, project_id=project_id, skip=skip, limit=limit
        )
    else:
        # Recuperar todos os arquivos que o usuário tem acesso
        if current_user.role == UserRole.FREELANCER:
            files = file_service.get_multi_by_owner_projects(
                db=db, uploader_id=current_user.id, skip=skip, limit=limit
            )
        else:
            # Recuperar todos os arquivos do cliente
            file = file_service.get_multi_by_owner_projects(
                db=db, uploader_id=current_user.id, skip=skip, limit=limit
            )
    
    return files

@router.get("/{file_id}", response_model=FileDetail)
def read_file(
    *,
    db: Session = Depends(get_db),
    file_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Recuperar um arquivo específico pelo ID.
 
    """
    file = file_service.get(db=db, id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    # Pegar o projeto associado ao arquivo
    project = project_service.get(db=db, id=file.project_id)

    # Checar se o usuário tem autorização para ver o arquivo
    if (current_user.role == UserRole.FREELANCER and project.owner_id != current_user.id) or \
       (current_user.role == UserRole.CLIENT and project.client_id != current_user.id):
        raise HTTPException(status_code=403, detail="Usuário não autorizado a ver este arquivo")
    
    return file

@router.delete("/{file_id}", response_model=File)
def delete_file(
    *,
    db: Session = Depends(get_db),
    file_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Deletar um arquivo
    
    Apenas o dono do projeto(Freelancer) ou quem está subindo o arquivo(Uploader) pode deletá-lo.
    """
    file = file_service.get(db=db, id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    # Pegar o projeto associado ao arquivo
    project = project_service.get(db=db, id=file.project_id)

    # Checar se o usuário tem autorização para deletar o arquivo
    if not (project.owner_id == current_user.id or file.uploader_id == current_user.id):
        raise HTTPException(status_code=403, detail="Usuário não autorizado a deletar este arquivo")
    
    # Deletar o arquivo no processador de arquivos
    try:
        httpx.delete(f"{settings.FILE_PROCESSOR_URL}/api/files/{file_id}")
    except httpx.RequestError:
        # Log do erro mas continue o processo de deleção
        pass

    # Deletar o arquivo do banco de dados
    file_service.delete(db=db, id=file_id)
    
    return file




