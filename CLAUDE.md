# Claude Code Instructions - CLI Todo Manager

This document provides Claude Code with project-specific instructions for working with the CLI Todo Manager application.

## Project Overview

**Name:** CLI Todo Manager
**Type:** Console Application (Python 3.13+)
**Architecture:** Functional Programming (no classes)
**Package Manager:** UV (mandatory)
**Status:** Feature-complete with 100% test coverage (93/93 tests passing)

**Purpose:** A command-line todo list manager that allows users to create, view, update, delete, and manage completion status of tasks.

## Quick Start

### Setup
```bash
# Clone repository
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP
git checkout console-app

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Run Application
```bash
uv run python src/main.py
```

### Run Tests
```bash
# All tests
uv run python -m unittest discover -s tests -p "test_*.py" -v

# Unit tests only
uv run python -m unittest discover -s tests/unit -p "test_*.py" -v

# Integration tests only
uv run python -m unittest discover -s tests/integration -p "test_*.py" -v

# Contract tests only
uv run python -m unittest discover -s tests/contract -p "test_*.py" -v
```

## Project Structure

```
├── src/
│   ├── main.py         # Application entry point, main menu loop
│   ├── cli.py          # User interaction, prompts, display formatting
│   ├── storage.py      # CRUD operations, in-memory storage
│   └── models.py       # Data validation, todo creation
├── tests/
│   ├── unit/           # 42 unit tests for individual functions
│   ├── integration/    # 12 integration tests for user stories
│   └── contract/       # 39 contract tests for CLI compliance
├── specs/001-cli-todo-app/
│   ├── spec.md         # Feature specification with user stories
│   ├── plan.md         # Implementation plan and architecture
│   ├── tasks.md        # Task breakdown by phase
│   ├── contracts/      # CLI interface contracts
│   ├── data-model.md   # Data structure documentation
│   ├── research.md     # Research and decisions
│   └── quickstart.md   # Quick testing scenarios
├── .specify/memory/
│   └── constitution.md # Project principles and coding standards
├── history/prompts/    # Prompt history records (PHRs)
├── pyproject.toml      # UV project configuration
├── README.md           # User-facing documentation
└── CLAUDE.md           # This file
```

## Implemented Features

### User Story 1: Create and View Todos
- Add todo with title (required, 1-200 chars)
- Add optional description (0-1000 chars)
- List all todos with ID, status, title, description
- Status indicators: `[ ]` incomplete, `[X]` complete

### User Story 2: Mark Completion Status
- Mark todo as complete by ID
- Mark todo as incomplete by ID
- Idempotent operations (no error if already in that state)

### User Story 3: Update Todo Content
- Update title by ID (blank input keeps current)
- Update description by ID (blank input keeps current)
- Can update one or both fields

### User Story 4: Delete Todos
- Delete todo by ID
- IDs are never reused (sequential assignment)
- Remaining todos preserve their original IDs

### Additional Features
- Capacity limit: Maximum 1000 todos (NFR-007)
- Invalid choice handling with clear error messages
- Exit with confirmation message
- All error messages match CLI contract specification

## Architecture Decisions

### Functional Programming
- **NO classes** - Pure functions only
- Data passed as dictionaries
- Separation of concerns: models, storage, CLI, main

### Data Flow
```
User Input (main.py)
  → CLI handlers (cli.py)
    → Storage operations (storage.py)
      → Validation (models.py)
        → In-memory storage (todos list)
```

### Storage Pattern
- In-memory list of dictionaries
- Sequential ID counter (starts at 1, never reused)
- No persistence (data lost on exit - by design for MVP)

### Validation Pattern
- Separate validation functions in models.py
- Returns tuple: `(is_valid: bool, error_message: str)`
- Storage layer calls validators before operations

### Return Patterns
- Storage operations return tuples:
  - `add_todo()`: `(success, todo_id, message)`
  - Other operations: `(success, message)`
- Consistent error message format across all operations

## Coding Conventions

### Function Signatures
```python
# Validation functions
def validate_title(title: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)"""

# Storage operations
def add_todo(title: str, description: str | None) -> tuple[bool, int | None, str]:
    """Returns (success, todo_id, message)"""

def update_todo(todo_id: any, new_title: str | None, new_description: str | None) -> tuple[bool, str]:
    """Returns (success, message)"""
```

### Error Messages (Exact Format Required)
```python
# From CLI contract - must match exactly
"Error: Title cannot be empty."
"Error: Title exceeds 200 character limit."
"Error: Description exceeds 1000 character limit."
"Error: Maximum 1000 todos reached."
"Error: ID must be a positive integer."
"Error: Todo with ID {id} not found."
```

### Success Messages (Exact Format Required)
```python
"Todo added successfully! (ID: {id})"
"Todo ID {id} updated successfully!"
"Todo ID {id} deleted successfully!"
"Todo ID {id} marked as complete!"
"Todo ID {id} marked as incomplete!"
```

### CLI Prompts (Exact Format Required)
```python
"Enter title: "
"Enter description (optional, press Enter to skip): "
"Enter todo ID: "
"Enter todo ID to delete: "
"Enter new title (leave blank to keep current): "
"Enter new description (leave blank to keep current): "
```

## Development Workflow

### Making Changes
1. **Read specification** in `specs/001-cli-todo-app/spec.md`
2. **Follow TDD approach**:
   - Write test first (red)
   - Implement minimal code to pass (green)
   - Refactor if needed
3. **Run all tests** to ensure no regressions
4. **Update documentation** if behavior changes

### Adding New Features
1. Update `spec.md` with new user story
2. Update `plan.md` with implementation approach
3. Add tasks to `tasks.md`
4. Write tests (unit, integration, contract)
5. Implement feature
6. Verify all 93 tests still pass

### Test-Driven Development
```bash
# 1. Write test first
# tests/unit/test_storage.py - add new test

# 2. Run test (should FAIL)
uv run python -m unittest tests.unit.test_storage.TestNewFeature -v

# 3. Implement feature
# src/storage.py - add minimal code

# 4. Run test (should PASS)
uv run python -m unittest tests.unit.test_storage.TestNewFeature -v

# 5. Run all tests (should all PASS)
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

## Key Constraints

### MUST Follow
- ✅ Use UV for all package management (no pip, pipenv, poetry)
- ✅ Python 3.13+ only
- ✅ Functional programming (no classes)
- ✅ Exact CLI contract compliance (prompts, messages, formats)
- ✅ All tests must pass (93/93 - 100%)
- ✅ In-memory storage only (no database, no files)

### MUST NOT Do
- ❌ Create classes or OOP patterns
- ❌ Add persistence (files, databases)
- ❌ Change error message formats
- ❌ Change CLI prompt formats
- ❌ Use global mutable state (except todos list and next_id in storage.py)

## Testing Strategy

### Test Coverage (93 tests total)

**Unit Tests (42 tests):**
- `test_models.py`: 13 tests for validation functions
- `test_cli.py`: 4 tests for display functions
- `test_storage.py`: 25 tests for CRUD operations

**Integration Tests (12 tests):**
- `test_workflows.py`: 3 tests per user story (4 stories)
- End-to-end scenarios from spec.md

**Contract Tests (39 tests):**
- `test_cli_interface.py`: Exact prompt and message verification
- Menu, Add, List, Update, Delete, Mark Complete/Incomplete

### Running Specific Tests
```bash
# Single test file
uv run python -m unittest tests.unit.test_storage -v

# Single test class
uv run python -m unittest tests.unit.test_storage.TestAddTodo -v

# Single test method
uv run python -m unittest tests.unit.test_storage.TestAddTodo.test_add_todo_with_valid_inputs -v
```

## Common Tasks

### Add a New Storage Operation
```python
# 1. Write test in tests/unit/test_storage.py
def test_new_operation(self):
    from storage import new_operation
    success, message = new_operation(...)
    self.assertTrue(success)
    self.assertEqual(message, "Expected message")

# 2. Implement in src/storage.py
def new_operation(...) -> tuple[bool, str]:
    """Docstring with contract details."""
    # Validate inputs
    # Perform operation
    # Return (success, message)
    pass

# 3. Add CLI handler in src/cli.py if needed
def handle_new_operation() -> None:
    """Handle new operation with user prompts."""
    pass

# 4. Wire up in src/main.py if new menu item
```

### Fix a Failing Test
```bash
# 1. Run the specific failing test
uv run python -m unittest tests.unit.test_storage.TestSomething.test_failing -v

# 2. Read the error message
# 3. Check the test expectations
# 4. Fix the implementation
# 5. Re-run the specific test
# 6. Run all tests to ensure no regressions
```

## References

- **Specification**: `specs/001-cli-todo-app/spec.md`
- **Architecture Plan**: `specs/001-cli-todo-app/plan.md`
- **Task Breakdown**: `specs/001-cli-todo-app/tasks.md`
- **CLI Contracts**: `specs/001-cli-todo-app/contracts/cli-interface.md`
- **Constitution**: `.specify/memory/constitution.md`

## Success Criteria

When working on this project, ensure:
- ✅ All 93 tests pass
- ✅ CLI contract compliance maintained
- ✅ Functional programming patterns followed
- ✅ Error messages match specification exactly
- ✅ Code is well-documented with docstrings
- ✅ No classes introduced
- ✅ UV used for all Python operations

---

**Last Updated:** 2025-12-29
**Project Status:** Feature-complete, production-ready
**Test Coverage:** 100% (93/93 tests passing)
