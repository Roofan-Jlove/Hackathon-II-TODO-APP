# Claude Code Instructions - CLI Todo Manager (Hackathon Phase 1)

This document provides Claude Code with project-specific instructions for working with the **Hackathon Phase 1** CLI Todo Manager application.

## Project Overview

**Name:** CLI Todo Manager - Hackathon Phase 1
**Type:** Console Application (Python 3.13+)
**Architecture:** Functional Programming (no classes)
**Package Manager:** UV (mandatory)
**Status:** Hackathon Phase 1 Complete - All features implemented with full test coverage

**Purpose:** A feature-rich command-line todo list manager with priorities, tags, search/filter, sorting, and recurring tasks - built as part of a hackathon project demonstrating rapid full-stack development.

## Hackathon Phase 1 - Project Details

### Development Timeline
- **Phase I (MVP)**: Basic CRUD operations
- **Phase II (Enhanced)**: Priorities, Tags, Search/Filter, Sort
- **Phase III (Advanced)**: Recurring Tasks with auto-recreation

### Technology Stack
- **Python 3.13+**: Latest stable Python
- **UV**: Modern Python package and project manager
- **Colorama**: Terminal colors and emoji support
- **python-dateutil**: Date arithmetic for recurring tasks
- **Claude Code**: AI-powered development assistant
- **Spec-Kit Plus**: Specification-driven development framework

### Architecture
- **Functional Programming**: Pure functions, no classes
- **In-Memory Storage**: No persistence (by design for Phase 1)
- **TDD Approach**: Test-Driven Development with 100% coverage
- **CLI-First**: Menu-driven interface with colorful output

## Quick Start

### Setup
```bash
# Clone repository
git clone https://github.com/Roofan-Jlove/Hackathon-II-TODO-APP.git
cd Hackathon-II-TODO-APP
git checkout console-app

# Install UV (if not already installed)
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
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
# All tests (56 unit tests)
uv run python -m unittest discover -s tests -p "test_*.py" -v

# Unit tests only
uv run python -m unittest tests.unit.test_models -v
```

## Project Structure

```
├── src/
│   ├── main.py         # Application entry point, main menu loop (Phase III)
│   ├── cli.py          # User interaction, colorful display (Phase II/III enhanced)
│   ├── storage.py      # CRUD operations, in-memory storage (Phase III enhanced)
│   └── models.py       # Data validation, todo creation (Phase III enhanced)
├── tests/
│   └── unit/           # 56 unit tests for all validation and features
├── specs/
│   ├── 001-cli-todo-app/          # Phase I specification
│   ├── 002-cli-todo-app-enhanced/ # Phase II specification
│   └── 003-cli-todo-app-advanced/ # Phase III specification
├── .specify/memory/
│   └── constitution.md            # Project principles and coding standards
├── history/prompts/               # Prompt history records (PHRs)
├── pyproject.toml                 # UV project configuration
├── README.md                      # User-facing documentation
└── CLAUDE.md                      # This file
```

## Implemented Features (Hackathon Phase 1)

### Phase I - MVP (User Stories 1-4)

#### User Story 1: Create and View Todos
- ✅ Add todo with title (required, 1-200 chars)
- ✅ Add optional description (0-1000 chars)
- ✅ List all todos with ID, status, title, description
- ✅ Status indicators: `⬜` incomplete, `✅` complete

#### User Story 2: Mark Completion Status
- ✅ Mark todo as complete by ID
- ✅ Mark todo as incomplete by ID
- ✅ Idempotent operations (no error if already in that state)

#### User Story 3: Update Todo Content
- ✅ Update title by ID (blank input keeps current)
- ✅ Update description by ID (blank input keeps current)
- ✅ Can update one or both fields

#### User Story 4: Delete Todos
- ✅ Delete todo by ID
- ✅ IDs are never reused (sequential assignment)
- ✅ Remaining todos preserve their original IDs

### Phase II - Enhanced (User Stories 5-8)

#### User Story 5: Task Priorities
- ✅ Set priority: High (🔴H), Medium (🟡M), Low (🔵L)
- ✅ Default priority: Medium
- ✅ Case-insensitive input with normalization
- ✅ Visual indicators in todo list

#### User Story 6: Tags and Categories
- ✅ Add/remove tags (comma-separated)
- ✅ Tags normalized to lowercase (case-insensitive)
- ✅ Duplicate tags removed automatically
- ✅ Tag length: 1-20 characters
- ✅ Visual tag display in list

#### User Story 7: Search and Filter
- ✅ Search by keyword (title/description)
- ✅ Filter by status (complete/incomplete/all)
- ✅ Filter by priority (High/Medium/Low)
- ✅ Filter by tags
- ✅ Case-insensitive search

#### User Story 8: Sort Tasks
- ✅ Sort by ID (ascending/descending)
- ✅ Sort by priority (High→Low, Low→High)
- ✅ Sort by title (A→Z, Z→A)
- ✅ Sort by status (incomplete first/complete first)

### Phase III - Advanced (User Story 9)

#### User Story 9: Recurring Tasks
- ✅ Set recurrence pattern: Daily, Weekly, Monthly
- ✅ Custom recurrence intervals (e.g., every 2 weeks)
- ✅ Auto-create next occurrence when completed
- ✅ Visual indicators: 🔁D (Daily), 🔁W (Weekly), 🔁M (Monthly)
- ✅ Remove recurrence (set to None)
- ✅ Backward compatible with Phase I/II todos

### Additional Features
- ✅ Colorful CLI with emojis for better UX
- ✅ Capacity limit: Maximum 1000 todos (NFR-007)
- ✅ Invalid choice handling with clear error messages
- ✅ Automatic data migration (Phase I → Phase II → Phase III)
- ✅ All error messages match CLI contract specification

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

### Data Model (Phase III)
```python
{
    "id": int,                          # Phase I: Sequential ID
    "title": str,                       # Phase I: 1-200 chars
    "description": str,                 # Phase I: 0-1000 chars
    "completed": bool,                  # Phase I: Default False
    "priority": str,                    # Phase II: High/Medium/Low
    "tags": list[str],                  # Phase II: Lowercase normalized
    "created_at": datetime,             # Phase II: Auto-assigned
    "recurrence_pattern": str | None,   # Phase III: Daily/Weekly/Monthly/None
    "recurrence_interval": int,         # Phase III: Default 1
    "next_occurrence": datetime | None  # Phase III: Calculated on complete
}
```

### Storage Pattern
- In-memory list of dictionaries
- Sequential ID counter (starts at 1, never reused)
- No persistence (data lost on exit - by design for Phase 1)
- Automatic migration on read operations

### Validation Pattern
- Separate validation functions in models.py
- Returns tuple: `(valid, normalized_value, error_message)`
- Storage layer calls validators before operations

### Return Patterns
- Storage operations return tuples:
  - `add_todo()`: `(success, todo_id, message)`
  - `set_recurrence()`: `(success, message)`
  - Other operations: `(success, message)`
- Consistent error message format across all operations

## Coding Conventions

### Function Signatures (Phase III)
```python
# Validation functions
def validate_title(title: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)"""

def validate_priority(priority: str | None) -> tuple[bool, str | None, str]:
    """Returns (valid, normalized_priority, error_message)"""

def validate_recurrence_pattern(pattern: str | None) -> tuple[bool, str | None, str]:
    """Returns (valid, normalized_pattern, error_message)"""

# Storage operations
def add_todo(title: str, description: str | None) -> tuple[bool, int | None, str]:
    """Returns (success, todo_id, message)"""

def set_priority(todo_id: any, priority: str) -> tuple[bool, str]:
    """Returns (success, message)"""

def set_recurrence(todo_id: any, pattern: str, interval: int = 1) -> tuple[bool, str]:
    """Returns (success, message)"""
```

### Error Messages (Exact Format Required)
```python
# Phase I
"Error: Title cannot be empty."
"Error: Title exceeds 200 character limit."
"Error: Description exceeds 1000 character limit."
"Error: Maximum 1000 todos reached."
"Error: ID must be a positive integer."
"Error: Todo with ID {id} not found."

# Phase II
"Error: Priority must be High, Medium, or Low."
"Error: Each tag must be 1-20 characters."

# Phase III
"Error: Recurrence pattern must be None, Daily, Weekly, or Monthly."
```

### Success Messages (Exact Format Required)
```python
# Phase I
"Todo added successfully! (ID: {id})"
"Todo ID {id} updated successfully!"
"Todo ID {id} deleted successfully!"
"Todo ID {id} marked as complete!"
"Todo ID {id} marked as incomplete!"

# Phase II
"Todo ID {id} priority set to {priority}!"
"Todo ID {id} tags updated!"

# Phase III
"Todo ID {id} recurrence set to {pattern}!"
"Todo ID {id} marked as complete! Next occurrence created (ID: {new_id})."
```

## Development Workflow

### Making Changes
1. **Read specification** in appropriate `specs/` directory
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
4. Write tests (unit tests)
5. Implement feature
6. Verify all tests still pass

### Test-Driven Development
```bash
# 1. Write test first
# tests/unit/test_models.py - add new test

# 2. Run test (should FAIL)
uv run python -m unittest tests.unit.test_models.TestNewFeature -v

# 3. Implement feature
# src/models.py - add minimal code

# 4. Run test (should PASS)
uv run python -m unittest tests.unit.test_models.TestNewFeature -v

# 5. Run all tests (should all PASS)
uv run python -m unittest discover -s tests -p "test_*.py" -v
```

## Key Constraints

### MUST Follow
- ✅ Use UV for all package management (no pip, pipenv, poetry)
- ✅ Python 3.13+ only
- ✅ Functional programming (no classes)
- ✅ Exact CLI contract compliance (prompts, messages, formats)
- ✅ All tests must pass (56/56 - 100%)
- ✅ In-memory storage only (no database, no files)

### MUST NOT Do
- ❌ Create classes or OOP patterns
- ❌ Add persistence (files, databases) - Phase 1 constraint
- ❌ Change error message formats
- ❌ Change CLI prompt formats
- ❌ Use global mutable state (except todos list and next_id in storage.py)

## Testing Strategy

### Test Coverage (56 unit tests)

**Unit Tests (56 tests in test_models.py):**
- `TestValidateId`: 5 tests for ID validation
- `TestValidateTitle`: 6 tests for title validation
- `TestValidateDescription`: 5 tests for description validation
- `TestValidatePriority`: 7 tests for priority validation (Phase II)
- `TestValidateTags`: 9 tests for tag validation (Phase II)
- `TestValidateRecurrencePattern`: 8 tests for recurrence validation (Phase III)
- `TestMigrateTodoToPhase2`: 3 tests for Phase II migration
- `TestMigrateTodoToPhase3`: 2 tests for Phase III migration
- `TestCreateTodoPhase2`: 5 tests for Phase II todo creation
- `TestCreateTodoPhase3`: 3 tests for Phase III todo creation

### Running Specific Tests
```bash
# Single test file
uv run python -m unittest tests.unit.test_models -v

# Single test class
uv run python -m unittest tests.unit.test_models.TestValidateRecurrencePattern -v

# Single test method
uv run python -m unittest tests.unit.test_models.TestValidateRecurrencePattern.test_valid_pattern_daily -v
```

## Menu Structure (Phase III)

```
📋 TODO MANAGER - MAIN MENU

  ➕  1. Add Todo
  📋  2. List All Todos
  ✏️   3. Update Todo
  🗑️   4. Delete Todo
  ✅  5. Mark Todo Complete
  ⬜  6. Mark Todo Incomplete
  🎯  7. Set Priority
  🏷️   8. Manage Tags
  🔍  9. Search & Filter
  🔀  10. Sort
  🔁  11. Set Recurrence
  👋  12. Exit

Enter choice [1-12]:
```

## Common Tasks

### Add a New Validation Function
```python
# 1. Write test in tests/unit/test_models.py
def test_new_validation(self):
    from models import validate_new_field
    valid, normalized, error = validate_new_field("input")
    self.assertTrue(valid)
    self.assertEqual(normalized, "expected")

# 2. Implement in src/models.py
def validate_new_field(value: any) -> tuple[bool, any, str]:
    """Validate and normalize new field."""
    # Validation logic
    return (True, normalized_value, "")
```

### Add a New Storage Operation
```python
# 1. Implement in src/storage.py
def new_operation(todo_id: any, value: str) -> tuple[bool, str]:
    """Docstring with contract details."""
    from models import validate_id, validate_new_field

    # Validate inputs
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Validate value
    field_valid, normalized, field_error = validate_new_field(value)
    if not field_valid:
        return (False, field_error)

    # Update todo
    todo["new_field"] = normalized

    return (True, f"Todo ID {parsed_id} new field set!")

# 2. Add CLI handler in src/cli.py
def handle_new_operation() -> None:
    """Handle new operation with user prompts."""
    from storage import new_operation

    todo_id = input("Enter todo ID: ")
    value = input("Enter value: ")

    success, message = new_operation(todo_id, value)

    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

# 3. Wire up in src/main.py
elif choice == "13":
    handle_new_operation()
```

## References

- **Phase I Specification**: `specs/001-cli-todo-app/spec.md`
- **Phase II Specification**: `specs/002-cli-todo-app-enhanced/spec.md`
- **Phase III Specification**: `specs/003-cli-todo-app-advanced/spec.md`
- **Constitution**: `.specify/memory/constitution.md`

## Success Criteria (Hackathon Phase 1)

When working on this project, ensure:
- ✅ All 56 unit tests pass
- ✅ CLI contract compliance maintained
- ✅ Functional programming patterns followed
- ✅ Error messages match specification exactly
- ✅ Code is well-documented with docstrings
- ✅ No classes introduced
- ✅ UV used for all Python operations
- ✅ Colorful CLI with emojis works across platforms
- ✅ Recurring tasks auto-create next occurrences
- ✅ Backward compatibility maintained (Phase I → II → III)

## Hackathon Achievements

✅ **MVP Complete**: Full CRUD operations with validation
✅ **Enhanced Features**: Priorities, Tags, Search/Filter, Sort
✅ **Advanced Features**: Recurring tasks with auto-recreation
✅ **100% Test Coverage**: 56/56 tests passing
✅ **Production Ready**: Clean architecture, documented, tested
✅ **User Experience**: Colorful CLI with visual indicators

---

**Last Updated:** 2025-12-29
**Project Status:** Hackathon Phase 1 Complete
**Test Coverage:** 100% (56/56 tests passing)
**Total Features:** 9 User Stories Fully Implemented
