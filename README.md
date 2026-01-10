# Hackathon II - TODO App (Mono Repo)

A comprehensive 5-phase hackathon project demonstrating full-stack development, AI integration, and cloud deployment of a TODO application.

## Project Overview

This mono repository contains all 5 phases of the Hackathon II TODO App project. Each phase builds upon the previous one, showcasing different technologies and deployment strategies.

## Repository Structure

```
HackathonII-TODO-APP/
├── phase-1-console-app/          # ✅ Phase 1: CLI Application (COMPLETE)
├── phase-2-web-app/              # ✅ Phase 2: Web Application (COMPLETE)
├── phase-3-ai-chatbot/           # 📋 Phase 3: AI-Powered Chatbot (PLANNED)
├── phase-4-kubernetes/           # 📋 Phase 4: Kubernetes Deployment (PLANNED)
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

### Phase 3: AI-Powered Chatbot 📋 PLANNED

**Technology:** TBD (LangChain, OpenAI API, etc.)

Conversational AI interface for TODO management:
- Natural language task creation
- Smart task suggestions
- Context-aware responses
- Voice input support

**Location:** `phase-3-ai-chatbot/`
**Status:** Folder structure created

---

### Phase 4: Kubernetes Deployment 📋 PLANNED

**Technology:** Kubernetes, Helm, Docker

Container orchestration and deployment:
- Kubernetes manifests
- Helm charts
- Service configuration
- Auto-scaling setup
- Health checks and monitoring

**Location:** `phase-4-kubernetes/`
**Status:** Folder structure created

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

| Phase | Status | Completion | Test Coverage |
|-------|--------|------------|---------------|
| Phase 1: Console App | ✅ Complete | 100% | 56/56 tests |
| Phase 2: Web App | ✅ Complete | 100% | 42/42 tests (28 backend + 14 frontend) |
| Phase 3: AI Chatbot | 📋 Planned | 0% | - |
| Phase 4: Kubernetes | 📋 Planned | 0% | - |
| Phase 5: Cloud Deploy | 📋 Planned | 0% | - |

## Timeline

- **Phase 1**: Completed - 2025-12-29 (56/56 tests passing)
- **Phase 2**: Completed - 2026-01-10 (42/42 tests passing, Production Ready)
- **Phase 3**: Planned
- **Phase 4**: Planned
- **Phase 5**: Planned

## License

MIT License - See individual phase directories for specific licensing information.

## Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code) - AI-powered development assistant
- Using [Spec-Kit Plus](https://github.com/RichardRosenblat/spec-kit-plus) - Specification-driven development framework
- Powered by [UV](https://astral.sh/uv) - Modern Python package manager

---

**Last Updated:** 2026-01-11
**Current Phase:** Phase 3 (AI-Powered Chatbot) - Planning
**Overall Progress:** 40% (2/5 phases complete)
**Total Tests:** 98/98 passing (56 Phase 1 + 42 Phase 2)
