# CLI Todo Application - Phase I

In-memory Python console todo application built with Spec-Driven Development (SDD) using Claude Code and Spec-Kit Plus.

## Overview

This is an educational project demonstrating the Agentic Dev Stack workflow:
**Spec → Plan → Tasks → Implement**

Phase I focuses on basic CRUD operations for managing todo items in memory (no persistence).

## Technology Stack

- **Python 3.13+**: Latest stable Python
- **UV**: Modern Python package and project manager
- **Claude Code**: AI-powered development tool
- **Spec-Kit Plus**: Specification-driven development framework

## Prerequisites

- Python 3.13+ ([python.org](https://python.org))
- UV ([docs.astral.sh/uv](https://docs.astral.sh/uv))

### Installing UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd HackathonII-TODO-APP

# Create virtual environment (UV handles this automatically)
uv venv

# Run the application
uv run python src/main.py

# Run tests
uv run python -m unittest discover tests -v
```

## Features (Phase I)

- ✅ Add new todo items with title and description
- ✅ List all todos with status indicators
- ✅ Update todo title and description
- ✅ Delete todos by ID
- ✅ Mark todos as complete/incomplete
- ⚠️ In-memory storage only (no persistence between sessions)

## Project Structure

```
HackathonII-TODO-APP/
├── pyproject.toml          # UV project configuration
├── src/
│   ├── models.py           # Data validation functions
│   ├── storage.py          # CRUD operations (in-memory)
│   ├── cli.py              # User interaction and display
│   └── main.py             # Application entry point
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── contract/           # CLI contract tests
└── specs/001-cli-todo-app/ # Specification documents
    ├── spec.md             # Feature specification
    ├── plan.md             # Implementation plan
    ├── tasks.md            # Task breakdown
    ├── research.md         # Technical decisions
    ├── data-model.md       # Data model and validation
    ├── quickstart.md       # Developer guide
    └── contracts/          # Interface contracts
```

## Development Workflow

This project follows the **Agentic Dev Stack** methodology:

1. **Specification** (`spec.md`): Define requirements, user stories, acceptance criteria
2. **Planning** (`plan.md`): Architecture decisions, technical context, constitution check
3. **Tasks** (`tasks.md`): Dependency-ordered implementation tasks
4. **Implementation**: Execute tasks via Claude Code (AI-assisted development)

## Running Tests

```bash
# All tests
uv run python -m unittest discover tests -v

# Unit tests only
uv run python -m unittest discover tests/unit -v

# Integration tests only
uv run python -m unittest discover tests/integration -v

# Contract tests only
uv run python -m unittest discover tests/contract -v
```

## Constitution Principles

This project adheres to strict constitution principles:

- **Explicitness Over Implicitness**: All behavior explicitly specified
- **Separation of Concerns**: Clean layer boundaries (models, storage, CLI, main)
- **Testability First**: Every feature has acceptance criteria and tests
- **Minimal Viable Scope**: Simplest solution, no over-engineering
- **Error Transparency**: Clear error messages, no silent failures
- **Documentation as Contract**: Code reflects specifications exactly

## Phase I Constraints

**In Scope**:
- CLI menu-driven interface
- In-memory data storage
- CRUD operations for todos
- Input validation and error handling

**Out of Scope** (for Phase I):
- Persistence (file/database)
- Networking or APIs
- Multi-user support
- GUI
- Advanced features (priorities, due dates, search, etc.)

## Future Phases

- **Phase II**: Add persistence (file or database)
- **Phase III**: Multi-user with authentication
- **Phase IV**: REST API
- **Phase V**: Distributed architecture
- **Phase VI**: AI/ML enhancements

## License

Educational project - Phase I of The Evolution of Todo

## Documentation

See `specs/001-cli-todo-app/` for complete specification documents:
- `spec.md`: Complete feature specification
- `plan.md`: Implementation plan and architecture
- `tasks.md`: Detailed task breakdown
- `quickstart.md`: Developer quick reference
