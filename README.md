# Freela Facility - Sistema de Gerenciamento de Arquivos para Freelancers

O Freela Facility é uma solução completa para freelancers gerenciarem arquivos enviados por clientes, organizando-os automaticamente com tags e categorias para facilitar o acesso e melhorar a produtividade.

## Arquitetura do Sistema

Este projeto segue uma arquitetura de microserviços, composta por três componentes principais:

1. **Frontend (Next.js)**: Interface de usuário responsiva e intuitiva para freelancers e clientes.
2. **API Principal (FastAPI)**: Gerencia autenticação, usuários, projetos e metadados de arquivos.
3. **API de Processamento de Arquivos (Flask)**: Especializada no processamento, categorização e armazenamento de arquivos.
4. **Serviço Externo**: Google Cloud Vision API para análise e categorização automática de imagens.

![Arquitetura do Sistema](https://github.com/Penichezito/freela-facility-api/blob/main/assets/Diagrama%20FreelaFacility-2025-04-13-113424.png)

## Requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local do frontend)
- Python 3.11+ (para desenvolvimento local das APIs)
- PostgreSQL (gerenciado pelo Docker)

## Configuração e Instalação

### Usando Docker (Recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/freela-facility.git
   cd freela-facility
   ```

2. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

3. Inicie os serviços com Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Acesse a aplicação:
   - Frontend: http://localhost:3000
   - API Principal: http://localhost:8000
   - API de Processamento: http://localhost:5000

## Repositórios de Componentes

- [API Principal](https://github.com/seu-usuario/freela-facility-api)
- [API de Processamento de Arquivos](https://github.com/seu-usuario/freela-facility-file-processor)
- [Frontend](https://github.com/seu-usuario/freela-facility-frontend)

## Configuração e Execução

1. Clone este repositório principal:
   \`\`\`bash
   git clone https://github.com/seu-usuario/freela-facility.git
   cd freela-facility
   \`\`\`

2. Clone os repositórios dos componentes:
   \`\`\`bash
   git clone https://github.com/seu-usuario/freela-facility-api.git
   git clone https://github.com/seu-usuario/freela-facility-file-processor.git
   git clone https://github.com/seu-usuario/freela-facility-frontend.git
   \`\`\`

3. Configure o arquivo .env (opcional):
   \`\`\`bash
   cp .env.example .env
   # Edite o arquivo .env conforme necessário
   \`\`\`

4. Inicie os serviços com Docker Compose:
   \`\`\`bash
   docker-compose up -d
   \`\`\`

5. Acesse o sistema:
   - Frontend: http://localhost:3000
   - API Principal: http://localhost:8000/docs
   - API de Processamento: http://localhost:5000/health
  
### Comandos para reinicialização e reconstrução do Docker Compose:
```bash
docker-compose down
docker-compose build api
docker-compose up -d

```

### Desenvolvimento Local (Sem Docker)

Consulte os READMEs específicos em cada diretório de componente para instruções detalhadas de desenvolvimento local:

- [Frontend (Next.js)](./freela-facility-frontend/README.md)
- [API Principal (FastAPI)](./freela-facility-api/README.md)
- [API de Processamento (Flask)](./freela-facility-file-processor/README.md)

## Funcionalidades Principais

- **Autenticação e Gerenciamento de Usuários**
  - Registro de freelancers e clientes
  - Autenticação JWT
  - Perfis e configurações de usuário

- **Gerenciamento de Projetos**
  - Criação e edição de projetos
  - Atribuição de clientes a projetos
  - Dashboard com métricas de projetos

- **Upload e Gerenciamento de Arquivos**
  - Upload de múltiplos arquivos
  - Suporte a vários formatos (imagens, documentos, código, etc.)
  - Categorização automática por tipo de arquivo

- **Organização Automática com Tags**
  - Geração automática de tags baseada em conteúdo
  - Análise de imagens com Google Cloud Vision API
  - Tags personalizáveis e pesquisáveis

- **Visualização e Recuperação de Arquivos**
  - Visualização de arquivos por projeto ou tag
  - Pesquisa avançada de arquivos
  - Pré-visualização integrada para arquivos compatíveis

## Integração com Google Cloud Vision API

Este projeto utiliza a Google Cloud Vision API para análise automática de imagens e geração de tags relevantes. A API é usada para:

- Detecção de objetos e cenas em imagens
- Reconhecimento de texto em imagens
- Identificação de cores predominantes
- Classificação de conteúdo

Para configurar a integração:

1. Crie uma conta de serviço no Google Cloud Platform
2. Ative a Vision API para seu projeto
3. Faça download das credenciais JSON
4. Adicione o caminho para o arquivo de credenciais na variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS`

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

# Freela Facility API Principal

API principal do sistema Freela Facility, responsável por gerenciamento de usuários, autenticação, projetos e coordenação com a API de processamento de arquivos.

## Tecnologias Utilizadas

- **FastAPI**: Framework web rápido para construção de APIs com Python
- **SQLAlchemy**: ORM para interação com banco de dados
- **PostgreSQL**: Banco de dados relacional
- **JWT**: Autenticação via tokens JWT
- **Alembic**: Migrações de banco de dados
- **Docker**: Containerização da aplicação

## Estrutura do Projeto

```
freela-facility-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── config.py            # Configurações da aplicação
│   ├── core/                # Núcleo (segurança, dependências)
│   ├── db/                  # Modelos e conexão com banco de dados
│   │   ├── database.py
│   │   ├── models/          # Modelos SQLAlchemy
│   │   └── repositories/    # Repositórios para acesso a dados
│   ├── api/                 # Rotas da API
│   │   ├── v1/              # API versão 1
│   │   │   ├── endpoints/   # Endpoints por recurso
│   │   │   └── schemas/     # Esquemas Pydantic
│   │   └── deps.py          # Dependências da API
│   ├── services/            # Lógica de negócios
│   └── utils/               # Utilitários
├── tests/                   # Testes
├── alembic/                 # Migrações do banco de dados
├── Dockerfile               # Configuração do Docker
└── requirements.txt         # Dependências do projeto
```

## Endpoints da API

A API principal oferece os seguintes endpoints:

### Autenticação

- `POST /api/v1/auth/login` - Login de usuário
- `POST /api/v1/auth/register` - Registro de novo usuário
- `GET /api/v1/auth/me` - Informações do usuário atual

### Usuários

- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{user_id}` - Obter usuário específico
- `PUT /api/v1/users/{user_id}` - Atualizar usuário
- `DELETE /api/v1/users/{user_id}` - Excluir usuário

### Projetos

- `GET /api/v1/projects/` - Listar projetos
- `POST /api/v1/projects/` - Criar novo projeto
- `GET /api/v1/projects/{project_id}` - Obter projeto específico
- `PUT /api/v1/projects/{project_id}` - Atualizar projeto
- `DELETE /api/v1/projects/{project_id}` - Excluir projeto

### Arquivos

- `POST /api/v1/files/upload/` - Upload de arquivo
- `GET /api/v1/files/` - Listar arquivos
- `GET /api/v1/files/{file_id}` - Obter arquivo específico
- `DELETE /api/v1/files/{file_id}` - Excluir arquivo

## Instalação e Execução

### Com Docker

```bash
# Construir a imagem
docker build -t freela-facility-api .

# Executar o container
docker run -p 8000:8000 --env-file .env freela-facility-api
```

### Desenvolvimento Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/freela-facility-api.git
   cd freela-facility-api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. Execute as migrações:
   ```bash
   alembic upgrade head
   ```

6. Execute a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```

## Documentação da API

A documentação interativa da API está disponível em:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testes

Para executar os testes:

```bash
pytest
```

## Integração com Outros Serviços

### API de Processamento de Arquivos

A API principal se comunica com a API de processamento de arquivos para:

- Upload e processamento de arquivos
- Análise e categorização automática
- Gerenciamento de tags

A comunicação é feita via HTTP utilizando o cliente HTTPX.

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | URL de conexão com o banco de dados | `postgresql://postgres:postgres@localhost:5432/freela_facility` |
| `FILE_PROCESSOR_URL` | URL da API de processamento de arquivos | `http://localhost:5000/api` |
| `SECRET_KEY` | Chave secreta para JWT | Gerada automaticamente |
| `ALGORITHM` | Algoritmo para JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token | `30` |
