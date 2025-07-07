
# Backend - Sistema de Votação

Backend Django REST Framework para o sistema de votação online para cooperativas.

## Tecnologias

- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Docker

## API Endpoints

### Autenticação
- `POST /register` - Cadastro de usuário
- `POST /login` - Login e obtenção de token JWT

### Pautas e Votação
- `GET /topics` - Lista todas as pautas (público)
- `POST /topics` - Criar nova pauta (requer autenticação)
- `POST /topics/{id}/session` - Abrir sessão de votação (requer autenticação)
- `POST /topics/{id}/vote` - Registrar voto (requer autenticação)
- `GET /topics/{id}/result` - Ver resultado da votação (público)

## Como executar localmente

### Pré-requisitos
- Python 3.11+
- PostgreSQL
- pip

### Instalação
```bash
cd backend
pip install -r requirements.txt
```

### Configurar banco de dados
1. Criar banco PostgreSQL
2. Copiar `.env.example` para `.env` e configurar variáveis
3. Executar migrações:
```bash
python manage.py migrate
```

### Executar servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

## Como executar com Docker

### Executar sistema completo
Na raiz do projeto:
```bash
docker-compose up --build
```

O backend estará disponível em `http://localhost:8000`

## Estrutura do projeto

```
backend/
├── voting_system/     # Configurações do Django
├── users/            # App de usuários e autenticação
├── topics/           # App de pautas e votação
├── votes/            # App de votos
├── requirements.txt  # Dependências Python
├── Dockerfile       # Container Docker
└── entrypoint.sh    # Script de inicialização
```

## Funcionalidades

- ✅ Autenticação JWT
- ✅ CRUD de pautas
- ✅ Sistema de votação
- ✅ Controle de sessões
- ✅ Resultados de votação
- ✅ CORS configurado
- ✅ Banco PostgreSQL
