# Research: CLI Todo Application (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2025-12-28
**Purpose**: Resolve technical unknowns and establish best practices for Phase I implementation

## Technical Decisions

### 1. Project Management Tool Selection

**Decision**: UV (modern Python package and project manager)

**Rationale**:
- Mandatory requirement per project specification
- Fast, modern alternative to pip/poetry/pipenv
- Handles virtual environments, dependencies, and project structure
- Simplifies development workflow with single tool
- Integrates well with modern Python tooling
- Required for Agentic Dev Stack workflow

**Usage**:
- Project initialization: `uv init`
- Dependency management: `uv add`, `uv remove`
- Running application: `uv run python src/main.py`
- Running tests: `uv run python -m unittest discover tests`
- Virtual environment managed automatically by UV

### 2. Python Version Selection

**Decision**: Python 3.13+

**Rationale**:
- Mandatory requirement per project specification
- Latest stable Python with modern features
- Improved performance over earlier versions
- Better error messages and debugging capabilities
- Full support for modern type hints and pattern matching
- Future-proof for Phase II+ enhancements

**Alternatives Considered**:
- Python 3.8-3.12: Older versions, project requires latest
- Python 3.14+: Not yet stable/released

### 3. In-Memory Data Structure

**Decision**: List of dictionaries for todo storage

**Rationale**:
- Matches specification's "Python standard library collections (list, dict)" (NFR-015)
- Simple, predictable, meets all Phase I requirements
- List maintains insertion order for sequential ID assignment
- Dictionary for each todo provides clear field access
- No need for classes/objects for Phase I simplicity
- Easy to iterate for list/search operations
- Supports up to 1000 items efficiently (specification's limit)

**Structure**:
```python
todos = [
    {"id": 1, "title": "...", "description": "...", "completed": False},
    {"id": 2, "title": "...", "description": "...", "completed": True},
]
```

**Alternatives Considered**:
- Dictionary with ID keys: Requires manual ID tracking, no insertion order guarantee in older Python
- Custom classes: Over-engineering for Phase I, violates minimal scope principle
- Named tuples: Immutable, complicates updates

### 4. ID Generation Strategy

**Decision**: Counter variable tracking next ID to assign

**Rationale**:
- Meets specification: "sequential and predictable (1, 2, 3, ...)" (NFR-005)
- Simple implementation: `next_id` variable incremented on each add
- IDs never reused even after deletion (meets spec's immutability of ID)
- No collision risk
- Deterministic behavior guaranteed

**Implementation Approach**:
```python
next_id = 1  # Global or passed through functions
# On add:
new_todo = {"id": next_id, ...}
next_id += 1
```

**Alternatives Considered**:
- Max ID + 1: Works but requires list iteration on every add
- UUID: Overkill, not user-friendly for CLI, violates "positive integer" requirement
- Index-based: Breaks when items deleted

### 5. Menu-Driven Interface Pattern

**Decision**: Infinite loop with menu display, input collection, action dispatch

**Rationale**:
- Matches specification's "menu-driven interface" (FR-009)
- Meets NFR-004: "Menu MUST be redisplayed after each operation"
- Standard CLI pattern, familiar to users
- Simple control flow for generated code

**Pattern**:
```
while True:
    display_menu()
    choice = get_user_input()
    if choice == "7": break
    dispatch_action(choice)
```

**Alternatives Considered**:
- Command-line arguments (e.g., `todo add "title"`): Not specified, would violate spec
- REPL-style: More complex, unnecessary for Phase I

### 6. Input Validation Approach

**Decision**: Validate-then-execute pattern with early returns

**Rationale**:
- Clear error handling per specification requirements (FR-007)
- Prevents invalid state mutations
- User-friendly: errors displayed before any changes
- Matches specified error messages exactly

**Pattern**:
```
def add_todo(title, description):
    if not title:
        print("Error: Title cannot be empty.")
        return
    if len(title) > 200:
        print("Error: Title exceeds 200 character limit.")
        return
    # ... proceed with add
```

### 7. Testing Framework

**Decision**: Python's built-in `unittest` module

**Rationale**:
- Specification requires "no external dependencies" (NFR-017)
- Built into Python standard library
- Sufficient for Phase I test coverage
- Familiar pattern for generated test code
- Supports all required test types (unit, integration, contract)

**Alternatives Considered**:
- pytest: More features but adds complexity for simple project
- doctest: Too limited for comprehensive testing
- Manual testing only: Violates constitution's testability principle

### 8. Code Organization Pattern

**Decision**: Functional programming approach with pure functions

**Rationale**:
- Aligns with constitution's separation of concerns (Principle II)
- Data (todo list) separate from operations (functions)
- Easy to test: functions take inputs, return outputs
- Stateless functions (except for todo list mutation) are predictable
- Meets Pythonic design (NFR-014: PEP 8)

**Module Structure**:
- `models.py`: Todo data structure validation
- `storage.py`: In-memory todo list operations (CRUD)
- `cli.py`: Menu display and user interaction
- `main.py`: Application entry point and main loop

**Alternatives Considered**:
- Object-oriented (classes): Over-engineering for Phase I scope
- Single file: Violates separation of concerns, hard to test
- Package structure: Unnecessary complexity for Phase I

### 9. Error Handling Strategy

**Decision**: User-friendly messages without stack traces, no application termination

**Rationale**:
- Specification requirement: "user-friendly error messages without application termination" (SC-004)
- All errors caught and converted to messages
- Application continues running after errors
- Matches specified error message formats exactly

**Pattern**:
```
try:
    # operation
except ValueError:
    print("Error: ...")  # User-friendly message
    # Continue, don't exit
```

## Best Practices for Phase I

### Code Generation Principles

1. **Follow PEP 8 strictly**: Specification requires Pythonic code (NFR-014)
2. **Use type hints**: Improves generated code clarity (optional but recommended)
3. **Keep functions small**: Single responsibility per function
4. **Explicit over implicit**: No magic values, all constants named
5. **Comprehensive docstrings**: Explain what each function does

### Testing Principles

1. **Test each functional requirement independently**: FR-001 to FR-010 each get tests
2. **Test all edge cases enumerated in spec**: Empty title, length limits, invalid IDs
3. **Test all error messages exactly**: Match specification's error message strings
4. **Integration tests for user stories**: P1-P4 each get end-to-end test scenarios

### Forward Compatibility Considerations

While Phase I excludes persistence, the architecture should support:
- **Storage abstraction**: Functions that operate on todo list can later accept different storage backends
- **Stateless operations**: Functions don't rely on global state beyond the todo list
- **Clear data model**: Dictionary structure can easily serialize to JSON/database later
- **Validation separation**: Input validation separate from storage enables reuse

## Unknowns Resolved

All technical context items now have clear answers:

- **Project Manager**: UV (mandatory)
- **Language/Version**: Python 3.13+
- **Primary Dependencies**: None for runtime (Python standard library only)
- **Development Tools**: UV for project/environment management
- **Storage**: In-memory list of dictionaries
- **Testing**: unittest (standard library)
- **Target Platform**: Cross-platform (any OS with Python 3.13+ and UV)
- **Project Type**: Single project (CLI application)
- **Performance Goals**: <1 second for all operations up to 1000 todos
- **Constraints**: No runtime dependencies, no persistence, no network
- **Scale/Scope**: Up to 1000 todos in single session
- **Development Workflow**: Agentic Dev Stack via Claude Code and Spec-Kit Plus

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| User expectations of persistence | Users may expect data to save | Clear messaging on app exit: "Goodbye! All todos will be lost." (specified) |
| Very long input causing display issues | Poor UX with terminal wrapping | Specification enforces limits (200/1000 chars) preventing this |
| Non-English characters in input | Potential encoding issues | Python 3 handles Unicode well; use UTF-8 for terminal I/O |
| Platform-specific terminal behavior | Inconsistent display across OS | Use standard print(), avoid platform-specific codes unless optional (NFR-003) |

## Ready for Phase 1

All research complete. Technical context fully defined. No remaining NEEDS CLARIFICATION markers.

Proceed to Phase 1: Data model and contracts design.
