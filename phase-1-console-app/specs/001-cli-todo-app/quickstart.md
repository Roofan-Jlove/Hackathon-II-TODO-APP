# Quickstart Guide: CLI Todo Application

**Feature**: 001-cli-todo-app
**Date**: 2025-12-28
**Audience**: Developers implementing Phase I

## Purpose

This guide provides a quick reference for implementing the CLI Todo Application according to the specification. It summarizes key decisions, structure, and workflows for efficient code generation.

## Prerequisites

- **Python 3.13+** installed ([python.org](https://python.org))
- **UV** installed ([docs.astral.sh/uv](https://docs.astral.sh/uv))
- Terminal/command prompt access
- Git (for version control)

### Installing UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

## Project Overview

**What**: In-memory CLI todo manager with CRUD operations
**Why**: Educational project demonstrating Spec-Driven Development for system evolution
**Scope**: Phase I only - no persistence, no network, no GUI, single-user

## Key Architectural Decisions

1. **Project Management**: UV for virtual environments and project structure
2. **Python Version**: 3.13+ (latest stable)
3. **Data Structure**: List of dictionaries (not classes/objects)
4. **ID Strategy**: Sequential counter starting at 1
5. **Interface**: Menu-driven loop (not command-line args)
6. **Validation**: Validate-then-execute with early returns
7. **Testing**: Python unittest (standard library)
8. **Organization**: Functional programming, separate modules

## Directory Structure

```
HackathonII-TODO-APP/
├── src/
│   ├── models.py        # Data validation functions
│   ├── storage.py       # CRUD operations on todo list
│   ├── cli.py           # Menu display and user interaction
│   └── main.py          # Entry point and main loop
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_storage.py
│   │   └── test_cli.py
│   ├── integration/
│   │   └── test_workflows.py
│   └── contract/
│       └── test_cli_interface.py
├── specs/001-cli-todo-app/
│   ├── spec.md          # Full specification
│   ├── plan.md          # This implementation plan
│   ├── data-model.md    # Data structures and validation
│   ├── research.md      # Technical decisions
│   └── contracts/
│       └── cli-interface.md  # I/O contracts
└── README.md
```

## Implementation Modules

### src/models.py

**Purpose**: Data structure validation

**Functions**:
- `validate_title(title: str) -> tuple[bool, str]`: Returns (valid, error_message)
- `validate_description(description: str) -> tuple[bool, str]`: Returns (valid, error_message)
- `validate_id(id_value: any) -> tuple[bool, int, str]`: Returns (valid, parsed_id, error_message)
- `create_todo(id: int, title: str, description: str) -> dict`: Returns todo dictionary

**Key Logic**:
- Title: non-empty, max 200 chars
- Description: max 1000 chars (empty string OK)
- ID: positive integer only

### src/storage.py

**Purpose**: CRUD operations on in-memory todo list

**Global State**:
- `todos: list[dict]` - The todo list
- `next_id: int` - Next ID to assign

**Functions**:
- `add_todo(title: str, description: str) -> tuple[bool, int|str]`: Returns (success, id|error_message)
- `get_all_todos() -> list[dict]`: Returns all todos sorted by ID
- `get_todo_by_id(id: int) -> dict|None`: Returns todo or None
- `update_todo(id: int, title: str|None, description: str|None) -> tuple[bool, str]`: Returns (success, message)
- `delete_todo(id: int) -> tuple[bool, str]`: Returns (success, message)
- `mark_complete(id: int, completed: bool) -> tuple[bool, str]`: Returns (success, message)

**Key Logic**:
- Check capacity (1000 todos max) before add
- IDs never reused after deletion
- All functions return tuple: (success boolean, result/error message)

### src/cli.py

**Purpose**: User interaction and display

**Functions**:
- `display_menu()`: Prints main menu
- `get_menu_choice() -> str`: Gets and returns user's menu choice
- `display_todos(todos: list[dict])`: Prints formatted todo list
- `get_user_input(prompt: str) -> str`: Prompts and returns input
- `handle_add()`: Orchestrates add operation
- `handle_list()`: Orchestrates list operation
- `handle_update()`: Orchestrates update operation
- `handle_delete()`: Orchestrates delete operation
- `handle_mark_complete()`: Orchestrates mark complete operation
- `handle_mark_incomplete()`: Orchestrates mark incomplete operation

**Key Logic**:
- All error messages printed in these functions
- Each handler calls storage functions and displays results
- Exact message formats per specification

### src/main.py

**Purpose**: Application entry point

**Main Loop**:
```python
def main():
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == '1':
            handle_add()
        elif choice == '2':
            handle_list()
        elif choice == '3':
            handle_update()
        elif choice == '4':
            handle_delete()
        elif choice == '5':
            handle_mark_complete()
        elif choice == '6':
            handle_mark_incomplete()
        elif choice == '7':
            print("Goodbye! All todos will be lost.")
            break
        else:
            print("Error: Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()
```

## Implementation Workflow

### Step 1: Data Model (src/models.py)

1. Implement validation functions (title, description, ID)
2. Implement todo creation function
3. Write unit tests for all validation rules
4. Verify tests pass

### Step 2: Storage Layer (src/storage.py)

1. Initialize global state (todos list, next_id counter)
2. Implement add_todo with all validations
3. Implement get_all_todos (sorted by ID)
4. Implement get_todo_by_id
5. Implement update_todo
6. Implement delete_todo
7. Implement mark_complete
8. Write unit tests for each function
9. Verify tests pass

### Step 3: CLI Layer (src/cli.py)

1. Implement display_menu
2. Implement get_menu_choice
3. Implement display_todos (formatted table)
4. Implement get_user_input helper
5. Implement each handle_* function
6. Write unit tests for display functions (capture stdout)
7. Verify tests pass

### Step 4: Main Application (src/main.py)

1. Implement main loop
2. Wire up all handlers
3. Test manual execution
4. Write integration tests

### Step 5: Integration Testing

1. Test all user stories (P1-P4) end-to-end
2. Test all edge cases
3. Test all error messages
4. Verify contract compliance

## Testing Strategy

### Unit Tests (tests/unit/)

- **test_models.py**: All validation functions
- **test_storage.py**: All CRUD operations with mock data
- **test_cli.py**: Display functions (capture stdout)

### Integration Tests (tests/integration/)

- **test_workflows.py**: Complete user journeys (P1-P4 from spec)

### Contract Tests (tests/contract/)

- **test_cli_interface.py**: Verify exact message formats, menu structure

### Test Execution

```bash
# Run all tests with UV
uv run python -m unittest discover tests

# Run specific test module
uv run python -m unittest tests.unit.test_models

# Run with verbose output
uv run python -m unittest discover tests -v

# Or after activating virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m unittest discover tests -v
```

## Running the Application

```bash
# Using UV (recommended)
uv run python src/main.py

# Or activate virtual environment first
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python src/main.py
```

## Success Criteria Checklist

Phase I is complete when:

- [ ] All 10 functional requirements (FR-001 to FR-010) implemented
- [ ] All 17 non-functional requirements (NFR-001 to NFR-017) met
- [ ] All 6 success criteria (SC-001 to SC-006) verified
- [ ] All 4 user stories (P1-P4) testable and passing
- [ ] All edge cases handled correctly
- [ ] All error messages match specification exactly
- [ ] Application runs without crashes
- [ ] No external dependencies beyond Python stdlib
- [ ] No persistence (data lost on exit)
- [ ] All tests passing (unit, integration, contract)
- [ ] Code follows PEP 8
- [ ] Constitution principles adhered to

## Common Pitfalls to Avoid

1. **Don't add persistence**: Phase I explicitly excludes any file I/O or database
2. **Don't use classes**: Functional approach with dictionaries is specified
3. **Don't add features**: No priorities, due dates, categories, search, etc.
4. **Don't add runtime dependencies**: Keep application using stdlib only (UV is for development)
5. **Don't reuse IDs**: Once assigned, IDs never reused even after deletion
6. **Don't skip validation**: All inputs must be validated before execution
7. **Don't crash on errors**: All errors caught and converted to user-friendly messages
8. **Don't deviate from messages**: Error and success messages must match spec exactly
9. **Don't forget UV**: Always use `uv run` for running code and tests

## Forward Compatibility Notes

Design decisions that support future phases:

- **Function-based storage**: Easy to swap for database/file backend later
- **Validation separation**: Reusable when adding API layer
- **Dictionary structure**: Serializes cleanly to JSON for persistence
- **No hard-coded limits in business logic**: 1000-todo limit is a constant, easily changed
- **Clear separation of concerns**: CLI layer can be replaced with web/API without touching storage

## Quick Reference: Error Messages

All error messages from `contracts/cli-interface.md`:

- `"Error: Title cannot be empty."`
- `"Error: Title exceeds 200 character limit."`
- `"Error: Description exceeds 1000 character limit."`
- `"Error: Maximum 1000 todos reached."`
- `"Error: Todo with ID N not found."`
- `"Error: ID must be a positive integer."`
- `"Error: Invalid choice. Please enter 1-7."`

## Quick Reference: Success Messages

- Add: `"Todo added successfully! (ID: N)"`
- Update: `"Todo ID N updated successfully!"`
- Delete: `"Todo ID N deleted successfully!"`
- Mark Complete: `"Todo ID N marked as complete!"`
- Mark Incomplete: `"Todo ID N marked as incomplete!"`
- Exit: `"Goodbye! All todos will be lost."`

## Next Steps

After completing Phase I implementation:

1. Run `/sp.tasks` to generate task breakdown
2. Execute tasks in dependency order
3. Validate against specification
4. Create ADR for significant decisions
5. Prepare for Phase II (persistence)
