
# Sistema de Votação - Frontend

Sistema completo de votação para associados desenvolvido em React.js com Redux, autenticação JWT e design responsivo.

## 🚀 Funcionalidades

- **Autenticação**: Login e registro com JWT
- **Dashboard**: Visualização de todas as pautas de votação
- **Votação**: Interface intuitiva para votar em pautas abertas
- **Resultados**: Visualização detalhada dos resultados das votações
- **Gerenciamento de Sessões**: Abertura de sessões de votação para usuários autenticados
- **Design Responsivo**: Interface adaptável para desktop e mobile

## 🛠️ Tecnologias

- **React.js** - Biblioteca para interface de usuário
- **Redux Toolkit** - Gerenciamento de estado global
- **React Router** - Navegação entre páginas
- **TailwindCSS** - Framework de CSS utilitário
- **shadcn/ui** - Componentes de interface elegantes
- **TypeScript** - Tipagem estática

## 📋 Pré-requisitos

- Node.js 18+
- npm ou yarn
- Backend API rodando na porta 8000

## 🚀 Instalação e Execução

### Método Docker

1. Construa e execute com Docker:
```bash
docker build -t vote-frontend .
docker run -p 3000:3000 -e REACT_APP_API_BASE_URL=http://localhost:8000 vote-frontend
```

## 📁 Estrutura do Projeto

```
src/
├── components/         # Componentes reutilizáveis
│   ├── ui/             # Componentes shadcn/ui
│   ├── Layout.tsx      # Layout principal
│   └── TopicCard.tsx   # Card de pauta
├── pages/              # Páginas da aplicação
│   ├── Dashboard.tsx   # Dashboard principal
│   ├── Login.tsx       # Página de login
│   ├── Register.tsx    # Página de registro
│   ├── Vote.tsx        # Página de votação
│   └── Results.tsx     # Página de resultados
├── services/           # Serviços de API
│   ├── api.ts         # Configuração base da API
│   ├── authService.ts # Serviços de autenticação
│   └── votingService.ts # Serviços de votação
├── store/             # Redux store
│   ├── index.ts       # Configuração do store
│   ├── authSlice.ts   # Estado de autenticação
│   └── votingSlice.ts # Estado de votação
└── hooks/             # Hooks customizados
```

## 🔗 Endpoints da API

O frontend se comunica com os seguintes endpoints:

### Autenticação
- `POST /register` - Registro de usuário
- `POST /login` - Login de usuário

### Pautas
- `GET /topics` - Listar todas as pautas
- `GET /topics/{id}` - Obter pauta específica
- `POST /topics/{id}/session` - Abrir sessão de votação
- `POST /topics/{id}/vote` - Registrar voto
- `GET /topics/{id}/result` - Obter resultado da votação

## 🎨 Design e UX

- **Design Moderno**: Interface limpa e profissional
- **Responsivo**: Adaptável para todos os dispositivos
- **Feedback Visual**: Indicadores de carregamento e mensagens de sucesso/erro
- **Acessibilidade**: Componentes acessíveis e navegação por teclado
- **Animações**: Transições suaves para melhor experiência

## 🔒 Segurança

- Token JWT armazenado no Redux e localStorage
- Proteção de rotas para usuários não autenticados
- Headers de autorização automáticos nas requisições
- Validação de formulários no frontend

## 📱 Funcionalidades por Página

### Dashboard
- Lista todas as pautas disponíveis
- Mostra status de cada pauta (Aguardando, Aberta, Encerrada)
- Botões contextuais baseados no status e autenticação

### Login/Registro
- Formulários com validação
- Formatação automática de CPF
- Feedback de erros e sucessos

### Votação
- Interface intuitiva com opções SIM/NÃO
- Informações da pauta e prazo de votação
- Confirmação visual da escolha

### Resultados
- Gráficos de barras com percentuais
- Estatísticas detalhadas
- Resultado final da votação

## 🐛 Problemas Conhecidos

- Certifique-se de que o backend esteja rodando na porta configurada
- Verifique as configurações de CORS no backend
- Em caso de erro de autenticação, limpe o localStorage
