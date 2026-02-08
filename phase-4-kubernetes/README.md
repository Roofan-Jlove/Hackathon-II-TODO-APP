# Todo Manager - Phase III: AI-Powered Chatbot

> A full-stack todo management web application with an AI-powered chatbot for natural language task management.

[![Next.js](https://img.shields.io/badge/Next.js-16%2B-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python_3.13%2B-009688)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon_Serverless-316192)](https://neon.tech/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9%2B-blue)](https://www.typescriptlang.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991)](https://openai.com/)
[![MCP](https://img.shields.io/badge/MCP-Tools-orange)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-Educational-orange)](./LICENSE)

---

## Overview

**Phase IV** containerizes the Phase III AI-powered chatbot application and deploys it to a local Kubernetes cluster using Minikube. The application runs in Docker containers orchestrated by Kubernetes with proper health checks, resource limits, and service discovery.

### What's New in Phase IV

- **Docker Containerization** - Multi-stage builds for optimized images
- **Kubernetes Deployment** - 2 replicas each for frontend and backend
- **Helm Charts** - Parameterized deployments with values files
- **Service Discovery** - Frontend communicates with backend via Kubernetes DNS
- **Health Probes** - Liveness and readiness checks for automatic recovery
- **Resource Management** - CPU and memory limits for pod scheduling
- **Minikube Local Cluster** - Full Kubernetes deployment running locally

### Phase III Features (Retained)

- **AI Chatbot Interface** - Conversational task management
- **Natural Language Processing** - Create tasks by simply describing them
- **5 MCP Tools** - add_task, list_tasks, update_task, complete_task, delete_task
- **Stateless Architecture** - All conversation state persisted to database
- **Multi-turn Conversations** - Context-aware AI responses

---

## Architecture

### Kubernetes Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Minikube Cluster                            │
│                                                                  │
│  ┌─────────────────────┐       ┌─────────────────────┐         │
│  │   todo-frontend     │       │   todo-backend      │         │
│  │   (Deployment)      │       │   (Deployment)      │         │
│  │   Replicas: 2       │       │   Replicas: 2       │         │
│  │                     │       │                     │         │
│  │  ┌─────────────┐   │       │  ┌─────────────┐   │         │
│  │  │  Pod (Next) │   │  HTTP │  │ Pod (FastAPI)│   │         │
│  │  │  Port 3000  │───┼──────►│  │  Port 8000  │   │         │
│  │  └─────────────┘   │       │  └─────────────┘   │         │
│  │  ┌─────────────┐   │       │  ┌─────────────┐   │         │
│  │  │  Pod (Next) │   │       │  │ Pod (FastAPI)│   │         │
│  │  │  Port 3000  │   │       │  │  Port 8000  │   │         │
│  │  └─────────────┘   │       │  └─────────────┘   │         │
│  └─────────────────────┘       └─────────────────────┘         │
│           │                             │                       │
│           │ NodePort                    │ ClusterIP             │
│           ▼                             ▼                       │
│  ┌─────────────────────┐       ┌─────────────────────┐         │
│  │  frontend-service   │       │  backend-service    │         │
│  │  (NodePort)         │       │  (ClusterIP)        │         │
│  │  Port: 30789        │       │  Port: 8000         │         │
│  └─────────────────────┘       └─────────────────────┘         │
│           │                             │                       │
└───────────┼─────────────────────────────┼───────────────────────┘
            │                             │
            │ minikube service            │
            │ (tunnel)                    │
            ▼                             ▼
    Browser Access              ┌───────────────────────┐
    http://127.0.0.1:51399      │   Neon PostgreSQL     │
                                │   (External Cloud)    │
                                │                       │
                                │   ┌───────────────┐   │
                                │   │  OpenAI API   │   │
                                │   │  (GPT-4o)     │   │
                                │   └───────────────┘   │
                                └───────────────────────┘
```

### Container Images

| Component | Image | Base | Size | User |
|-----------|-------|------|------|------|
| Frontend | `todo-frontend:latest` | node:20-alpine | ~200MB | nextjs |
| Backend | `todo-backend:latest` | python:3.13-slim | ~500MB | appuser |

### System Overview (Traditional)

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  Next.js        │ ←──────→│  FastAPI        │ ←──────→│  PostgreSQL     │
│  Frontend       │  HTTPS  │  Backend        │   SQL   │  Database       │
│  + ChatKit      │         │  + OpenAI       │         │  (Neon Cloud)   │
│  (Port 3000)    │         │  (Port 8000)    │         │                 │
│                 │         │                 │         │                 │
└─────────────────┘         └────────┬────────┘         └─────────────────┘
                                     │
                                     │ API Calls
                                     ↓
                            ┌─────────────────┐
                            │                 │
                            │  OpenAI API     │
                            │  (GPT-4o)       │
                            │                 │
                            └─────────────────┘
```

### Stateless Chat Flow

```
1. User types message in chat UI
   ↓
2. POST /api/chat/message (with JWT cookie)
   ↓
3. Backend authenticates user (JWT → user_id)
   ↓
4. Get/create conversation (from database)
   ↓
5. Fetch last 20 messages (from database)
   ↓
6. Store user message (to database)
   ↓
7. Build message array for OpenAI
   ↓
8. Run OpenAI Agent with MCP tools
   ├── Agent analyzes message
   ├── Agent calls MCP tools (e.g., add_task)
   │   └── Tool executes (filtered by user_id)
   └── Agent generates response
   ↓
9. Store assistant response (to database)
   ↓
10. Return response to client
   ↓
11. Chat UI displays response
```

---

## Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16+ | React framework with App Router |
| TypeScript | 5.9+ | Type-safe JavaScript |
| Tailwind CSS | 3.4+ | Utility-first CSS |
| React | 19+ | UI library |
| OpenAI ChatKit | Latest | Pre-built chat UI components |
| React Query | 5+ | Server state management |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.109+ | High-performance async API |
| Python | 3.13+ | Backend language |
| SQLModel | 0.0.14+ | ORM (SQLAlchemy + Pydantic) |
| PostgreSQL | 15+ | Database (Neon Serverless) |
| OpenAI SDK | Latest | AI model integration |
| MCP SDK | Latest | Tool protocol implementation |
| PyJWT | 2.8+ | JWT authentication |

### AI & ML
| Technology | Purpose |
|------------|---------|
| OpenAI GPT-4o | Language model for chat |
| MCP (Model Context Protocol) | Standardized tool calling |
| Function Calling | AI-to-tool communication |

---

## Quick Start

### Prerequisites

**Phase IV (Kubernetes):**
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **Minikube** ([Install](https://minikube.sigs.k8s.io/docs/start/))
- **kubectl** ([Install](https://kubernetes.io/docs/tasks/tools/))
- **Helm** ([Install](https://helm.sh/docs/intro/install/))
- **Neon PostgreSQL** (cloud database)
- **OpenAI API Key** ([Get one](https://platform.openai.com/))

**Local Development:**
- **Node.js** 18.x or higher
- **Python** 3.13 or higher
- **UV** Package Manager ([Install](https://docs.astral.sh/uv/))

### Installation

#### Option 1: Kubernetes Deployment (Phase IV - Recommended)

```bash
# 1. Clone repository
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP/phase-4-kubernetes

# 2. Start Minikube
minikube start

# 3. Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# 4. Build Docker images
docker build -t todo-backend:latest -f docker/backend/Dockerfile ./backend
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile ./frontend

# 5. Create Kubernetes secrets
kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --from-literal=BETTER_AUTH_SECRET="your-secret"

# 6. Deploy with Helm
helm install todo-backend ./helm-charts/backend
helm install todo-frontend ./helm-charts/frontend

# 7. Check deployment status
kubectl get pods

# 8. Access the application
minikube service todo-frontend
# Opens browser automatically!
```

**Verify Deployment:**
```bash
# Check all pods are running
kubectl get pods

# Expected output:
# NAME                             READY   STATUS    RESTARTS
# todo-backend-xxx-xxx             1/1     Running   0
# todo-backend-xxx-xxx             1/1     Running   0
# todo-frontend-xxx-xxx            1/1     Running   0
# todo-frontend-xxx-xxx            1/1     Running   0
```

#### Option 2: Local Development (Traditional)

```bash
# 1. Clone repository
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP/phase-4-kubernetes

# 2. Set Up Backend
cd backend
uv sync
cp .env.example .env
# Edit .env with your credentials
uv run uvicorn app.main:app --reload

# 3. Set Up Frontend (separate terminal)
cd ../frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
npm run dev

# 4. Access Application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Features

### AI Chat Commands

The AI assistant understands natural language. Here are some example commands:

#### Creating Tasks
```
"Create a task to buy groceries"
"Add a high priority task for the client meeting tomorrow"
"I need to remember to call mom this weekend"
"Make a task: Review Q4 reports, priority high, tags: work, urgent"
```

#### Listing Tasks
```
"Show me my tasks"
"List all high priority tasks"
"What tasks do I have due this week?"
"Show completed tasks"
```

#### Updating Tasks
```
"Change the priority of task 5 to high"
"Update the client meeting task to include agenda prep"
"Mark task 3 as in progress"
```

#### Completing Tasks
```
"Mark task 3 as done"
"Complete the groceries task"
"I finished the code review"
```

#### Deleting Tasks
```
"Delete task 7"
"Remove the groceries task"
"Cancel the old meeting task"
```

### MCP Tools

The AI uses these 5 tools to manage tasks:

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_task` | Create a new task | title, description, priority, tags, due_date |
| `list_tasks` | Retrieve tasks with filters | status, priority, tags, limit |
| `update_task` | Update an existing task | task_id, title, description, status, priority |
| `complete_task` | Mark a task as completed | task_id |
| `delete_task` | Delete a task permanently | task_id |

**Security Note:** All tools automatically receive the `user_id` from JWT authentication and filter database queries accordingly.

---

## Kubernetes Features (Phase IV)

### Containerization

**Backend Image:**
- Base: `python:3.13-slim`
- Multi-stage build for optimization
- Non-root user: `appuser`
- Size: ~500MB
- Health endpoint: `/health`

**Frontend Image:**
- Base: `node:20-alpine`
- Next.js standalone output
- Non-root user: `nextjs`
- Size: ~200MB
- Production optimized

### High Availability

**Deployment Strategy:**
- 2 replicas for frontend (load balanced)
- 2 replicas for backend (load balanced)
- Rolling updates (zero downtime)
- Automatic pod restarts on failure

**Resource Management:**
```yaml
# Frontend pods
requests:
  memory: "128Mi"
  cpu: "100m"
limits:
  memory: "256Mi"
  cpu: "200m"

# Backend pods
requests:
  memory: "256Mi"
  cpu: "250m"
limits:
  memory: "512Mi"
  cpu: "500m"
```

### Health Monitoring

**Liveness Probes:**
- Checks if pods are running
- Restarts pod if probe fails
- HTTP GET to health endpoint

**Readiness Probes:**
- Checks if pods are ready for traffic
- Removes from service if not ready
- Database connectivity check

### Service Discovery

**Internal Communication:**
- Frontend → Backend: `http://todo-backend:8000`
- Kubernetes DNS resolves service names
- Automatic load balancing across pods

**External Access:**
- Frontend: NodePort service (via Minikube tunnel)
- Backend: ClusterIP (internal only)
- Managed by `minikube service todo-frontend`

### Configuration Management

**ConfigMaps (Non-sensitive):**
- `NEXT_PUBLIC_API_URL=http://todo-backend:8000`
- `CORS_ORIGINS=http://todo-frontend`

**Secrets (Sensitive):**
- `DATABASE_URL` (Neon PostgreSQL)
- `OPENAI_API_KEY` (OpenAI API)
- `BETTER_AUTH_SECRET` (JWT authentication)

### Helm Charts

**Parameterized Deployments:**
- `values.yaml` for environment-specific configs
- Templated manifests for reusability
- Easy upgrades: `helm upgrade todo-backend ./helm-charts/backend`

**Chart Structure:**
```
helm-charts/
├── backend/
│   ├── Chart.yaml          # Chart metadata
│   ├── values.yaml         # Default values
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── configmap.yaml
└── frontend/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
```

---

## Project Structure

```
phase-3-ai-chatbot/
├── frontend/                        # Next.js Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/               # AI Chat page
│   │   │   │   └── page.tsx        # Chat interface
│   │   │   ├── tasks/              # Task management pages
│   │   │   └── ...
│   │   ├── components/
│   │   │   ├── features/
│   │   │   │   ├── chat/           # Chat components
│   │   │   │   └── tasks/          # Task components
│   │   │   └── ...
│   │   └── lib/
│   │       ├── api.ts              # API client (includes chat methods)
│   │       └── types.ts            # TypeScript types
│   ├── package.json
│   └── README.md
│
├── backend/                         # FastAPI Backend
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── routers/
│   │   │   ├── chat.py             # Chat endpoints
│   │   │   ├── tasks.py            # Task CRUD endpoints
│   │   │   └── auth.py             # Auth endpoints
│   │   ├── mcp/
│   │   │   └── server.py           # 5 MCP tools
│   │   ├── ai/
│   │   │   ├── agent.py            # OpenAI Agent
│   │   │   └── prompts.py          # System prompts
│   │   ├── models.py               # SQLModel models
│   │   └── ...
│   ├── pyproject.toml
│   └── README.md
│
├── specs/                           # Specifications
│   ├── features/
│   │   └── chatbot-features.md     # Chatbot feature specs
│   ├── api/
│   │   └── chat-endpoints.md       # Chat API specs
│   └── mcp/
│       └── mcp-tools-overview.md   # MCP tools specs
│
├── CLAUDE.md                        # Claude Code navigation guide
└── README.md                        # This file
```

---

## API Endpoints

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat/message` | Send a message to AI assistant |
| `GET` | `/api/chat/conversations` | List user's conversations |
| `GET` | `/api/chat/conversations/{id}` | Get conversation with messages |
| `DELETE` | `/api/chat/conversations/{id}` | Delete a conversation |

### Example: Send Chat Message

**Request:**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -H "Cookie: auth-token=<jwt-token>" \
  -d '{
    "message": "Create a task to buy groceries",
    "conversation_id": 123
  }'
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "✅ I've created a task titled 'Buy groceries'. Would you like to set a due date or priority?",
  "tool_calls": [
    {
      "tool": "add_task",
      "result": {
        "success": true,
        "data": {
          "id": "task-uuid",
          "title": "Buy groceries",
          "priority": "medium"
        }
      }
    }
  ]
}
```

---

## Environment Variables

### Backend (.env)

```bash
# Database - Neon Serverless PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname

# Authentication
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters

# CORS
CORS_ORIGINS=http://localhost:3000

# OpenAI (Phase III)
OPENAI_API_KEY=sk-your-openai-api-key

# Optional
DEBUG=false
```

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters
BETTER_AUTH_URL=http://localhost:3000
```

---

## Security

### User Isolation

**All MCP tools filter by user_id:**
- `user_id` is extracted from JWT token
- Every database query includes `WHERE user_id = ?`
- Users can only access their own tasks and conversations

### Authentication Flow

1. User logs in → receives JWT token in httpOnly cookie
2. Chat requests include cookie automatically
3. Backend verifies JWT, extracts user_id
4. MCP tools receive user_id for filtering

### Data Privacy

- Conversations stored only in your database
- Messages sent to OpenAI for processing
- No conversation data shared between users

---

## Development

### Running Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
uv run uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Testing

**Backend Tests:**
```bash
cd backend
uv run pytest -v
uv run pytest tests/test_mcp_tools.py -v
uv run pytest tests/test_chat_endpoints.py -v
```

**Frontend Tests:**
```bash
cd frontend
npm test
npm run test:run
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Add conversations and messages tables"
alembic upgrade head
```

---

## Troubleshooting

### Common Issues

**1. OpenAI API Key Error:**
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Ensure key is in backend/.env
OPENAI_API_KEY=sk-your-key-here
```

**2. Chat Not Working:**
- Check backend logs for errors
- Verify JWT cookie is being sent
- Ensure CORS_ORIGINS includes frontend URL

**3. Database Connection:**
```bash
# Verify DATABASE_URL format
postgresql+asyncpg://user:password@host:5432/dbname
```

**4. MCP Tool Errors:**
- Check that user_id is being passed correctly
- Verify database tables exist (run migrations)

---

## Documentation

- **Main Guide:** [CLAUDE.md](./CLAUDE.md) - Navigation for Claude Code
- **Backend Docs:** [backend/README.md](./backend/README.md) - Backend guide
- **Frontend Docs:** [frontend/README.md](./frontend/README.md) - Frontend guide
- **Specifications:** [specs/](./specs/) - Feature and API specifications
- **API Docs:** http://localhost:8000/docs (when backend is running)

---

## Contributing

This is an educational hackathon project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Read the relevant specifications
4. Write tests for your feature
5. Implement according to specs
6. Submit a Pull Request

---

## Acknowledgments

- **Claude Code** - AI-powered development assistant
- **OpenAI** - GPT-4o language model
- **SpecKit Plus** - Specification-driven development framework
- **Anthropic MCP** - Model Context Protocol

---

## License

Educational project for learning purposes.

---

<div align="center">

**Built with Next.js, FastAPI, OpenAI, and Claude Code**

**Phase IV - Local Kubernetes Deployment**

**Status:** Deployment Complete ✅

**Last Updated:** February 9, 2026

[⬆ Back to Top](#todo-manager---phase-iii-ai-powered-chatbot)

</div>
