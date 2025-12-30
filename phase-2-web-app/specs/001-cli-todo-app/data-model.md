# Data Model: CLI Todo Application (Phase I)

**Feature**: 001-cli-todo-app
**Date**: 2025-12-28
**Purpose**: Define data structures, validation rules, and state transitions

## Entity: Todo

### Fields

| Field | Type | Constraints | Default | Mutability |
|-------|------|-------------|---------|------------|
| `id` | Positive Integer | > 0, unique, sequential | Auto-assigned | Immutable |
| `title` | String | 1-200 characters, non-empty | None (required) | Mutable |
| `description` | String | 0-1000 characters | Empty string | Mutable |
| `completed` | Boolean | true or false | false | Mutable |

### Field Descriptions

**id** (Positive Integer):
- Purpose: Unique identifier for the todo item
- Generation: Auto-assigned sequentially starting from 1
- Uniqueness: No two todos ever share the same ID, even after deletion
- Immutability: Once assigned, never changes
- User interaction: Users reference todos by this ID for update/delete/status operations
- Source: FR-002, NFR-005

**title** (String):
- Purpose: Short description of the task
- Required: Must not be empty
- Length: Minimum 1 character, maximum 200 characters
- Validation: Enforced before todo creation or update
- Display: Primary identifying information in list view
- Source: FR-001, FR-010

**description** (String):
- Purpose: Optional detailed information about the task
- Optional: Can be empty string if user skips input
- Length: Maximum 1000 characters (empty string has length 0)
- Validation: Enforced before todo creation or update
- Display: Secondary information in list view
- Source: FR-001

**completed** (Boolean):
- Purpose: Track whether the task is done
- Values: `false` (incomplete) or `true` (complete)
- Default: All new todos start as `false` (incomplete)
- Toggle: Can be changed from false→true or true→false
- Display: Shown as `[ ]` when false, `[X]` when true
- Source: FR-006, specification User Interaction Flow

## Data Structure Representation

**In-Memory (Python)**:

```python
# Single Todo
todo = {
    "id": 1,                          # Positive integer
    "title": "Buy groceries",         # Non-empty string, max 200 chars
    "description": "Milk, eggs, bread",  # String, max 1000 chars
    "completed": False                # Boolean
}

# Todo Collection
todos = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "completed": False},
    {"id": 2, "title": "Call dentist", "description": "Schedule checkup", "completed": True},
]

# ID Counter
next_id = 3  # Next ID to assign
```

## Validation Rules

### On Todo Creation (Add Operation)

1. **Title Validation**:
   - `if title is None or title == ""`: Reject with "Error: Title cannot be empty."
   - `if len(title) > 200`: Reject with "Error: Title exceeds 200 character limit."

2. **Description Validation**:
   - `if description is None`: Convert to empty string `""`
   - `if len(description) > 1000`: Reject with "Error: Description exceeds 1000 character limit."

3. **ID Assignment**:
   - Assign `id = next_id`
   - Increment `next_id += 1`

4. **Completed Initialization**:
   - Always set `completed = False` for new todos

5. **Capacity Check**:
   - `if len(todos) >= 1000`: Reject with "Error: Maximum 1000 todos reached."

### On Todo Update (Update Operation)

1. **ID Validation**:
   - `if id not found in todos`: Reject with "Error: Todo with ID N not found."
   - `if id not a positive integer`: Reject with "Error: ID must be a positive integer."

2. **Title Update** (if provided):
   - Same validation as creation
   - If blank/skipped: keep existing title

3. **Description Update** (if provided):
   - Same validation as creation
   - If blank/skipped: keep existing description

4. **ID Preservation**:
   - ID field never changes during update

5. **Completed Preservation**:
   - Completed status unchanged during content update (separate operation)

### On Status Toggle (Mark Complete/Incomplete)

1. **ID Validation**:
   - `if id not found in todos`: Reject with "Error: Todo with ID N not found."
   - `if id not a positive integer`: Reject with "Error: ID must be a positive integer."

2. **Status Toggle**:
   - `completed = True` for mark complete
   - `completed = False` for mark incomplete

### On Todo Deletion (Delete Operation)

1. **ID Validation**:
   - `if id not found in todos`: Reject with "Error: Todo with ID N not found."
   - `if id not a positive integer`: Reject with "Error: ID must be a positive integer."

2. **Deletion**:
   - Remove todo from list
   - Do NOT reuse the ID for future todos
   - Other todos' IDs remain unchanged

## State Transitions

### Todo Lifecycle States

```
[Non-existent]
      |
      | (User adds todo with title + optional description)
      v
[Incomplete] (completed = false)
      |
      | (User marks complete)
      v
[Complete] (completed = true)
      |
      | (User marks incomplete)
      v
[Incomplete] (completed = false)
      |
      | (User deletes todo)
      v
[Non-existent]
```

### Valid State Transitions

| From State | Action | To State | Field Changes |
|------------|--------|----------|---------------|
| Non-existent | Add | Incomplete | id assigned, completed=false, title set, description set |
| Incomplete | Mark Complete | Complete | completed: false→true |
| Complete | Mark Incomplete | Incomplete | completed: true→false |
| Incomplete | Update | Incomplete | title and/or description changed |
| Complete | Update | Complete | title and/or description changed |
| Incomplete | Delete | Non-existent | Removed from list |
| Complete | Delete | Non-existent | Removed from list |

### Invalid State Transitions

- Cannot transition from Non-existent to Complete directly (must add first as Incomplete)
- Cannot change ID (immutable)
- Cannot create todo without title (validation prevents it)

## Invariants

These conditions MUST always be true:

1. **ID Uniqueness**: No two todos in the list have the same ID at any point in time
2. **ID Immutability**: Once a todo is created with ID N, that todo's ID never changes until deletion
3. **ID Sequential**: IDs are assigned in strictly increasing order (1, 2, 3, ...)
4. **Non-empty Titles**: Every todo in the list has a title with length ≥ 1
5. **Length Constraints**: All titles ≤ 200 chars, all descriptions ≤ 1000 chars
6. **Boolean Completed**: completed field is always exactly `true` or `false` (never null/undefined)
7. **List Ordering**: Todos displayed in ID ascending order
8. **Capacity Limit**: List never contains more than 1000 todos
9. **No Null Fields**: None of the four fields (id, title, description, completed) are ever null

## Relationships

**Phase I (In-Memory)**:
- No relationships between todos (independent items)
- No user/owner association (single-user application)
- No categories, tags, or hierarchies

**Forward Compatibility (Future Phases)**:
- Todo-to-User: Each todo owned by a user (Phase III: multi-user)
- Todo-to-Category: Optional categorization (future enhancement)
- Todo-to-Todo: Subtasks or dependencies (future enhancement)

## Data Model Evolution Path

### Phase I (Current):
- In-memory list of dictionaries
- No persistence
- Single session scope

### Phase II (Planned):
- Same field structure
- Add file/database serialization
- Persistence between sessions
- Migration: JSON serialization of current structure

### Phase III+ (Future):
- Add user_id field for multi-user
- Add created_at, updated_at timestamps
- Add priority, due_date fields
- Schema versioning for backward compatibility

**Key Design Decision**: Current data model is a strict subset of future models, enabling forward compatibility without breaking changes.
