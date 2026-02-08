# Hackathon II - TODO App (Mono Repo)

A comprehensive 5-phase hackathon project demonstrating full-stack development, AI integration, and cloud deployment of a TODO application.

[![Phase 1](https://img.shields.io/badge/Phase_1-Complete-brightgreen)](./phase-1-console-app)
[![Phase 2](https://img.shields.io/badge/Phase_2-Complete-brightgreen)](./phase-2-web-app)
[![Phase 3](https://img.shields.io/badge/Phase_3-Complete-brightgreen)](./phase-3-ai-chatbot)
[![Phase 4](https://img.shields.io/badge/Phase_4-Complete-brightgreen)](./phase-4-kubernetes)
[![Phase 5](https://img.shields.io/badge/Phase_5-Planned-lightgrey)](./phase-5-cloud-deployment)

## Project Overview

This mono repository contains all 5 phases of the Hackathon II TODO App project. Each phase builds upon the previous one, showcasing different technologies and deployment strategies.

## Repository Structure

```
HackathonII-TODO-APP/
├── phase-1-console-app/          # ✅ Phase 1: CLI Application (COMPLETE)
├── phase-2-web-app/              # ✅ Phase 2: Web Application (COMPLETE)
├── phase-3-ai-chatbot/           # ✅ Phase 3: AI-Powered Chatbot (COMPLETE)
├── phase-4-kubernetes/           # ✅ Phase 4: Kubernetes Deployment (COMPLETE)
├── phase-5-cloud-deployment/     # 📋 Phase 5: Cloud Deployment (PLANNED)
└── README.md                     # This file
```

## Phases

### Phase 1: Console Application ✅ COMPLETE

**Technology:** Python 3.13+, UV, Colorama, Functional Programming

A feature-rich command-line TODO manager with:
- CRUD operations (Create, Read, Update, Delete)
- Task priorities (High, Medium, Low)
- Tags and categories
- Search and filter capabilities
- Sorting options
- Recurring tasks (Daily, Weekly, Monthly)
- 100% test coverage (56 unit tests)

**Location:** `phase-1-console-app/`
**Documentation:** See `phase-1-console-app/README.md`

**Quick Start:**
```bash
cd phase-1-console-app
uv sync
uv run python src/main.py
```

---

### Phase 2: Web Application ✅ COMPLETE

**Technology:** FastAPI (Python 3.13+), Next.js 16+, TypeScript, PostgreSQL, Tailwind CSS

Production-ready full-stack web application with:
- **RESTful API Backend:** FastAPI with SQLModel ORM
- **Modern Frontend:** Next.js 16+ with App Router and TypeScript
- **Authentication:** Better Auth with secure JWT tokens in httpOnly cookies
- **Database:** Neon Serverless PostgreSQL with cloud persistence
- **Kanban Board:** Drag-and-drop interface with 4 status columns (Ready, In Progress, Review, Done)
- **Advanced Search & Filter:** Real-time search, filter by priority/tags/status
- **Task Sorting:** By date, priority, title, or completion status
- **Task Features:** Priorities (High/Medium/Low), tags, recurring tasks (Daily/Weekly/Monthly), due dates
- **UI/UX:** Responsive design with Tailwind CSS and Lucide React icons
- **Testing:** 100% test coverage - 42/42 tests passing (28 backend + 14 frontend)
- **Security:** User isolation, password hashing (bcrypt), XSS/CSRF protection, input validation

**Location:** `phase-2-web-app/`
**Documentation:** See `phase-2-web-app/README.md`

**Test Coverage:**
- Backend: 28/28 tests (Authentication, CRUD, Authorization, Validation)
- Frontend: 14/14 tests (Vitest + React Testing Library)
- Status: Production Ready ✅

**Quick Start:**
```bash
# Backend (Terminal 1)
cd phase-2-web-app/backend
uv sync
cp .env.example .env  # Configure database and secrets
uv run uvicorn app.main:app --reload
# API Docs: http://localhost:8000/docs

# Frontend (Terminal 2)
cd phase-2-web-app/frontend
npm install
cp .env.example .env.local  # Configure backend URL
npm run dev
# App: http://localhost:3000
```

---

### Phase 3: AI-Powered Chatbot ✅ COMPLETE

**Technology:** Next.js 16+, FastAPI, OpenAI GPT-4o, MCP Tools, PostgreSQL

AI-powered conversational interface for TODO management:
- **Natural Language Processing** - Create and manage tasks through conversation
- **5 MCP Tools** - add_task, list_tasks, update_task, complete_task, delete_task
- **Stateless Architecture** - All conversation state persisted to database
- **Multi-turn Conversations** - Context-aware AI responses with tool calling
- **OpenAI ChatKit** - Pre-built chat UI components
- **User Isolation** - Secure per-user data access
- **Built on Phase 2** - Extends web app with AI capabilities

**Location:** `phase-3-ai-chatbot/`
**Documentation:** See `phase-3-ai-chatbot/README.md`
**Status:** ✅ Complete - AI Chatbot fully functional

**Features:**
- Chat with AI to manage tasks ("Create a task to buy groceries")
- List tasks with filters ("Show me high priority tasks")
- Update and complete tasks through conversation
- Persistent conversation history
- Secure JWT authentication

**Quick Start:**
```bash
# Backend (Terminal 1)
cd phase-3-ai-chatbot/backend
uv sync
cp .env.example .env  # Add DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY
uv run uvicorn app.main:app --reload
# API Docs: http://localhost:8000/docs

# Frontend (Terminal 2)
cd phase-3-ai-chatbot/frontend
npm install
cp .env.example .env.local  # Configure backend URL
npm run dev
# App: http://localhost:3000
```

---

### Phase 4: Kubernetes Deployment ✅ COMPLETE

**Technology:** Kubernetes, Minikube, Helm, Docker, Next.js 16+, FastAPI, OpenAI GPT-4o

Container orchestration and local Kubernetes deployment of Phase 3 AI Chatbot application:
- **Docker Containerization** - Multi-stage builds for optimized images
  - Backend: Python 3.13-slim (~500MB)
  - Frontend: Node 20-alpine (~200MB)
- **Kubernetes Deployments** - 2 replicas each for HA
- **Service Discovery** - Frontend → Backend via Kubernetes DNS
- **Health Probes** - Liveness and readiness checks
- **Resource Management** - CPU and memory limits
- **Helm Charts** - Parameterized deployments
- **Minikube Local Cluster** - Full K8s deployment locally
- **Non-root Containers** - Security best practices
- **ConfigMaps & Secrets** - Environment configuration

**Location:** `phase-4-kubernetes/`
**Documentation:** See `phase-4-kubernetes/README.md`
**Status:** ✅ Complete - Running on Minikube

**Quick Start (Kubernetes):**
```bash
# Start Minikube
minikube start

# Configure Docker for Minikube
eval $(minikube docker-env)

# Build images
docker build -t todo-backend:latest -f docker/backend/Dockerfile ./backend
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile ./frontend

# Create secrets
kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL=$DATABASE_URL \
  --from-literal=OPENAI_API_KEY=$OPENAI_API_KEY \
  --from-literal=BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET

# Deploy with Helm
helm install todo-backend ./helm-charts/backend
helm install todo-frontend ./helm-charts/frontend

# Access application
minikube service todo-frontend
```

**Quick Start (Local Development):**
```bash
# Backend
cd phase-4-kubernetes/backend && uv run uvicorn app.main:app --reload

# Frontend
cd phase-4-kubernetes/frontend && npm run dev
```

---

### Phase 5: Cloud Deployment 📋 PLANNED

**Technology:** TBD (AWS/Azure/GCP, Terraform/Pulumi)

Production cloud deployment:
- Infrastructure as Code (IaC)
- CI/CD pipelines
- Monitoring and logging
- Load balancing
- Security hardening

**Location:** `phase-5-cloud-deployment/`
**Status:** Folder structure created

---

## Development Principles

Each phase follows these core principles:

1. **Specification-Driven Development (SDD)**: Using Spec-Kit Plus framework
2. **Test-Driven Development (TDD)**: Write tests first, then implementation
3. **Documentation First**: Comprehensive docs for each phase
4. **AI-Assisted Development**: Built with Claude Code assistance
5. **Clean Architecture**: Separation of concerns, maintainable code

## Getting Started

### Prerequisites

- Git
- Python 3.13+ (for Phase 1 & 2 backend)
- Node.js 18+ (for Phase 2 frontend)
- UV package manager (Python)
- npm (comes with Node.js)
- PostgreSQL or Neon account (for Phase 2)
- Docker (for Phase 4+)
- kubectl (for Phase 4)
- Cloud CLI tools (for Phase 5)

### Clone Repository

```bash
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd HackathonII-TODO-APP
```

### Navigate to Specific Phase

Each phase is self-contained with its own README and setup instructions:

```bash
# Phase 1 - Console App
cd phase-1-console-app
cat README.md

# Phase 2 - Web App
cd phase-2-web-app
cat README.md

# ... and so on
```

## Contributing

This is a hackathon project. Each phase has its own development workflow and contribution guidelines. See the README in each phase directory for details.

## Project Status

| Phase | Status | Completion | Key Features |
|-------|--------|------------|--------------|
| Phase 1: Console App | ✅ Complete | 100% | CLI CRUD, 56/56 tests |
| Phase 2: Web App | ✅ Complete | 100% | Full-stack, 42/42 tests |
| Phase 3: AI Chatbot | ✅ Complete | 100% | GPT-4o, MCP Tools, Chat UI |
| Phase 4: Kubernetes | ✅ Complete | 100% | Docker + K8s + Helm, Running on Minikube |
| Phase 5: Cloud Deploy | 📋 Planned | 0% | Production deployment |

## Timeline

- **Phase 1**: Completed - 2025-12-29 (56/56 tests passing)
- **Phase 2**: Completed - 2026-01-10 (42/42 tests passing, Production Ready)
- **Phase 3**: Completed - 2026-01-16 (AI Chatbot with MCP Tools)
- **Phase 4**: Completed - 2026-02-09 (Kubernetes Deployment with Minikube + Helm)
- **Phase 5**: Planned

## License

MIT License - See individual phase directories for specific licensing information.

## Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code) - AI-powered development assistant
- Using [Spec-Kit Plus](https://github.com/RichardRosenblat/spec-kit-plus) - Specification-driven development framework
- Powered by [UV](https://astral.sh/uv) - Modern Python package manager

---

**Last Updated:** 2026-02-09
**Current Phase:** Phase 4 - Kubernetes Deployment (COMPLETE ✅)
**Overall Progress:** 80% (4/5 phases complete)
**Total Tests:** 98+ tests passing (56 Phase 1 + 42 Phase 2 + Phase 3)
**Deployment Status:** Running on Minikube with 4 pods (2 frontend + 2 backend)
