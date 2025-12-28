# CLI Todo App - Quick Start Guide

## Installation & Setup

This project uses UV and Python 3.13+.

### Prerequisites
- Python 3.13 or higher
- UV package manager

### Verify Setup
```bash
uv run python --version
```
Should show Python 3.13+ (currently 3.14.0)

## Running the Application

From the project root directory:

```bash
uv run python src/main.py
```

## Usage Guide

### Available Features (Phase 3 - User Story 1 Complete)

#### 1️⃣ Add Todo
1. Select option `1` from the menu
2. Enter title (required, 1-200 chars)
3. Enter description (optional, 0-1000 chars, or press Enter to skip)
4. Confirmation: "Todo added successfully! (ID: N)"

**Example:**
```
Enter choice [1-7]: 1
Enter title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread
Todo added successfully! (ID: 1)
```

#### 2️⃣ List All Todos
1. Select option `2` from the menu
2. View formatted table of all todos

**Example Output:**
```
ID | Status | Title           | Description
---|--------|-----------------|------------------
1  | [ ]    | Buy groceries   | Milk, eggs, bread
2  | [ ]    | Call dentist    | Schedule checkup
3  | [ ]    | Write report    |
```

- Status: `[ ]` = incomplete, `[X]` = complete
- Empty description shown as blank

#### 7️⃣ Exit
1. Select option `7` from the menu
2. Message: "Goodbye! All todos will be lost."
3. Application closes

**⚠️ Important:** Data is stored in-memory only. When you exit, all todos are lost.

### Coming Soon (Not Yet Implemented)

- 3️⃣ Update Todo
- 4️⃣ Delete Todo
- 5️⃣ Mark Todo Complete
- 6️⃣ Mark Todo Incomplete

These options will show placeholder messages until implemented in future User Stories.

## Validation Rules

### Title Validation
- ✅ Required (cannot be empty or whitespace only)
- ✅ Maximum 200 characters
- ❌ Error: "Error: Title cannot be empty."
- ❌ Error: "Error: Title exceeds 200 character limit."

### Description Validation
- ✅ Optional (press Enter to skip)
- ✅ Maximum 1000 characters
- ❌ Error: "Error: Description exceeds 1000 character limit."

### System Limits
- ✅ Maximum 1000 todos
- ❌ Error: "Error: Maximum 1000 todos reached."

## Sample Session

```
Welcome to Todo Manager
-----------------------
1. Add Todo
2. List All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo Complete
6. Mark Todo Incomplete
7. Exit

Enter choice [1-7]: 1
Enter title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread
Todo added successfully! (ID: 1)

Welcome to Todo Manager
-----------------------
[menu repeats]

Enter choice [1-7]: 1
Enter title: Call dentist
Enter description (optional, press Enter to skip):
Todo added successfully! (ID: 2)

Welcome to Todo Manager
-----------------------
[menu repeats]

Enter choice [1-7]: 2
ID | Status | Title           | Description
---|--------|-----------------|------------------
1  | [ ]    | Buy groceries   | Milk, eggs, bread
2  | [ ]    | Call dentist    |

Welcome to Todo Manager
-----------------------
[menu repeats]

Enter choice [1-7]: 7
Goodbye! All todos will be lost.
```

## Testing

### Run Unit Tests
```bash
uv run python -m unittest tests.unit.test_models -v
```

### Run Contract Tests
```bash
uv run python -m unittest tests.contract.test_cli_interface -v
```

### Run All Tests
```bash
uv run python -m unittest tests.unit.test_models tests.contract.test_cli_interface
```

## Project Structure

```
src/
  main.py          # Application entry point
  cli.py           # User interface functions
  models.py        # Data validation functions
  storage.py       # In-memory data storage

tests/
  unit/            # Unit tests for validation
  contract/        # CLI contract compliance tests
  integration/     # End-to-end workflow tests

specs/
  001-cli-todo-app/  # Feature specifications
```

## Development Status

**✅ Completed:**
- Phase 1: Setup (UV, project structure)
- Phase 2: Foundational (storage, menu, main loop)
- Phase 3: User Story 1 - Create and View Todos (MVP)

**🚧 In Progress:**
- Phase 4: User Story 2 - Mark Completion Status
- Phase 5: User Story 3 - Update Todo Content
- Phase 6: User Story 4 - Delete Todos

**Current Stats:**
- 21 of 60 tasks complete (35%)
- MVP functional and tested
- 18 tests passing

## Need Help?

- Check specs: `specs/001-cli-todo-app/spec.md`
- View CLI contract: `specs/001-cli-todo-app/contracts/cli-interface.md`
- Review tasks: `specs/001-cli-todo-app/tasks.md`
