from fastapi import FastAPI, Depends, HTTPException
from fastapi.midllware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
import uvicorn

from app.appi.v1.router import api_router
from app.core.security import get_current_active_user
from app.db.databae import get_db, init_db
from app.config import settings

app = FastAPI(
    title="Freela Facility API",
    description="API Principal para gerenciamento de freelancers, clientes, projetos e arquivos",
    version="1.0.0",
)

# Configuração de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    f"http://{settings.FRONTEND_HOST}",
    f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão da rota da API
app.include_router(api_router, prefix="/api/v1")

# Inicialização do banco de dados
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/heath", tags=["Health"])
def heath_check():
    """
    Endpoint para verificação de saúde da API
    """
    return {"status": "healthy"}

# Personalização de documentação OpenAPI (Swagger)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Freela Facility API",
        version="1.0.0",
        description="API para gerenciamento de freelancers, clientes, projetos e arquivos",
        routes=app.routes,
    )
    
    # Personalização adicional (caso necessário)
    openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Configuração do FastAPI para ouvir requisições na porta 8000
if __name__ =="__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)