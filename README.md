# Sistema de Votação para Cooperativas

Esse projeto foi desenvolvido a fim de solucionar um desafio técnico para `WK_JobHub`. A descrição esta em `Gerenciamento sessões de votação.pdf`

Este projeto é uma solução completa para gestão de sessões de votação, composta por um backend Django REST Framework e um frontend React.js com Redux. Todo o sistema é containerizado com Docker, facilitando a execução e o deploy.

## 🏛️ Arquitetura do Projeto

- **Backend:** Django 4.2 + Django REST Framework, JWT, PostgreSQL
- **Frontend:** React.js, Redux Toolkit, TypeScript, TailwindCSS, shadcn/ui
- **Infraestrutura:** Docker, Docker Compose

## 🚀 Funcionalidades Principais

- Cadastro e autenticação de usuários (JWT)
- Criação e listagem de pautas de votação
- Abertura e controle de sessões de votação
- Registro de votos (SIM/NÃO)
- Visualização de resultados em tempo real
- Interface responsiva e intuitiva
- Proteção de rotas e validação de formulários
- Integração com API externa para validação de CPF
- (Bônus) Suporte a MQTT para atualização em tempo real dos resultados

## 📦 Estrutura de Diretórios

```
├── backend/    # Backend Django REST Framework
│   ├── users/      # Usuários e autenticação
│   ├── topics/     # Pautas e sessões
│   ├── votes/      # Votos
│   └── ...
├── frontend/   # Frontend React.js + Redux
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
├── docker-compose.yml
└── README.md
```

## 🔗 Endpoints Principais

### Autenticação
- `POST /register` — Cadastro de usuário
- `POST /login` — Login e obtenção de token JWT

### Pautas e Votação
- `GET /topics` — Listar pautas
- `POST /topics` — Criar pauta (autenticado)
- `POST /topics/{id}/session` — Abrir sessão de votação (autenticado)
- `POST /topics/{id}/vote` — Registrar voto (autenticado)
- `GET /topics/{id}/result` — Ver resultado da votação

## ▶️ Como Executar o Projeto

### Com Docker Compose (recomendado)

1. Certifique-se de ter Docker e Docker Compose instalados.
2. Na raiz do projeto, execute:

```bash
docker-compose up -d --build
```

- O backend estará disponível em `http://localhost:8000`
- O frontend estará disponível em `http://localhost:3000`

### Execução Manual

Veja os READMEs em `/backend` e `/frontend` para instruções detalhadas de execução manual.

## 🔒 Segurança
- Autenticação JWT
- Proteção de rotas no frontend
- Validação de formulários e CPF
- CORS configurado no backend

## 🌐 Integrações e Bônus
- Integração com API externa para validação de CPF: `https://user-info.herokuapp.com/users/{cpf}`
- (Opcional) Suporte a MQTT para atualização em tempo real dos resultados
