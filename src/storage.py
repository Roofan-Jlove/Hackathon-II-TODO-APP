"""
In-memory storage operations for todo items.

This module manages the todo list and next_id counter in memory,
providing CRUD operations (add, get, update, delete, mark complete)
according to the specification in specs/001-cli-todo-app/spec.md

Global State:
    todos (list): List of todo dictionaries, each with keys:
        - id (int): Unique positive integer, sequential
        - title (str): Task description (1-200 chars)
        - description (str): Optional details (0-1000 chars)
        - completed (bool): Completion status (default False)

    next_id (int): Counter for sequential ID assignment, starts at 1

Data Structure Example:
    todos = [
        {"id": 1, "title": "Buy groceries", "description": "Milk, eggs", "completed": False},
        {"id": 2, "title": "Call dentist", "description": "", "completed": True}
    ]
    next_id = 3
"""

# Global storage state
# In-memory list of todo dictionaries
todos: list[dict] = []

# Counter for sequential ID assignment (starts at 1, never reused)
next_id: int = 1


def add_todo(title: str, description: str | None) -> tuple[bool, int | None, str]:
    """
    Add a new todo to storage with validation.

    Args:
        title: Todo title (required, 1-200 chars)
        description: Todo description (optional, 0-1000 chars)

    Returns:
        tuple: (success, todo_id, message)
            - success (bool): True if todo was added
            - todo_id (int | None): ID of created todo if successful, None otherwise
            - message (str): Success message with ID or error message

    Validation and Business Rules:
        1. Check capacity (max 1000 todos per NFR-007)
        2. Validate title (required, 1-200 chars)
        3. Validate description (optional, 0-1000 chars)
        4. Assign sequential ID from next_id counter
        5. Create todo with completed=False
        6. Append to global todos list
        7. Increment next_id counter

    Error Messages (from CLI contract):
        - Capacity: "Error: Maximum 1000 todos reached."
        - Title: "Error: Title cannot be empty." or "Error: Title exceeds 200 character limit."
        - Description: "Error: Description exceeds 1000 character limit."

    Success Message (from CLI contract):
        - "Todo added successfully! (ID: {id})"

    Examples:
        >>> add_todo("Buy groceries", "Milk, eggs")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> add_todo("", None)
        (False, None, "Error: Title cannot be empty.")
    """
    global next_id

    # Import validation functions (avoid circular import by importing here)
    from models import validate_title, validate_description, create_todo

    # Check capacity (max 1000 todos per NFR-007)
    if len(todos) >= 1000:
        return (False, None, "Error: Maximum 1000 todos reached.")

    # Validate title
    title_valid, title_error = validate_title(title)
    if not title_valid:
        return (False, None, title_error)

    # Validate description
    desc_valid, desc_error = validate_description(description)
    if not desc_valid:
        return (False, None, desc_error)

    # Convert None description to empty string
    if description is None:
        description = ""

    # Assign ID from counter
    todo_id = next_id

    # Create todo dictionary
    new_todo = create_todo(todo_id, title, description)

    # Append to global list
    todos.append(new_todo)

    # Increment counter
    next_id += 1

    # Return success with ID
    return (True, todo_id, f"Todo added successfully! (ID: {todo_id})")


def get_all_todos() -> list[dict]:
    """
    Retrieve all todos sorted by ID ascending (Phase II enhanced with migration).

    Returns:
        list[dict]: List of all todo dictionaries, sorted by ID ascending
            Returns empty list if no todos exist
            All todos guaranteed to have Phase II fields (priority, tags, created_at)

    Sorting Rules:
        - Per CLI contract (line 110): Todos displayed in ID ascending order
        - Ensures consistent display order regardless of insertion order

    Migration Behavior (Phase II):
        - Automatically migrates Phase I todos to Phase II format
        - Migration is transparent and idempotent
        - Modifies global todos list in-place to persist migration

    Examples:
        >>> get_all_todos()
        []
        >>> add_todo("First", "")
        >>> add_todo("Second", "")
        >>> todos = get_all_todos()
        >>> todos[0]['id']
        1
        >>> todos[1]['id']
        2
        >>> todos[0]['priority']  # Phase II field
        'Medium'
    """
    from models import migrate_todo_to_phase2

    # Migrate all todos to Phase II format in-place (idempotent)
    # This ensures backward compatibility with Phase I todos
    global todos
    for i in range(len(todos)):
        todos[i] = migrate_todo_to_phase2(todos[i])

    # Return sorted copy (sort by 'id' key ascending)
    return sorted(todos, key=lambda todo: todo["id"])


def get_todo_by_id(todo_id: any) -> dict | None:
    """
    Retrieve a single todo by its ID.

    Args:
        todo_id: ID to search for (any type, will be validated)

    Returns:
        dict | None: Todo dictionary if found, None if not found or invalid ID

    Validation:
        - ID must be convertible to positive integer
        - Returns None for invalid IDs instead of raising error
        - Used by update, delete, and mark completion operations

    Examples:
        >>> add_todo("Buy groceries", "Milk")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> get_todo_by_id(1)
        {'id': 1, 'title': 'Buy groceries', 'description': 'Milk', 'completed': False}
        >>> get_todo_by_id(999)
        None
        >>> get_todo_by_id("invalid")
        None
    """
    from models import validate_id

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return None

    # Search for todo with matching ID
    for todo in todos:
        if todo["id"] == parsed_id:
            return todo

    # Not found
    return None


def mark_complete(todo_id: any) -> tuple[bool, str]:
    """
    Mark a todo as complete.

    Args:
        todo_id: ID of todo to mark complete (any type, will be validated)

    Returns:
        tuple: (success, message)
            - success (bool): True if todo was marked complete
            - message (str): Success message or error message

    Behavior:
        - Sets completed=True on the todo
        - Idempotent: marking already-complete todo succeeds
        - Validates ID and checks existence before modifying

    Error Messages (from CLI contract):
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."

    Success Message (from CLI contract):
        - "Todo ID {id} marked as complete!"

    Examples:
        >>> add_todo("Buy groceries", "")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> mark_complete(1)
        (True, "Todo ID 1 marked as complete!")
        >>> mark_complete(1)  # Idempotent
        (True, "Todo ID 1 marked as complete!")
        >>> mark_complete(999)
        (False, "Error: Todo with ID 999 not found.")
    """
    from models import validate_id

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Mark as complete (idempotent - no check if already complete)
    todo["completed"] = True

    # Return success
    return (True, f"Todo ID {parsed_id} marked as complete!")


def mark_incomplete(todo_id: any) -> tuple[bool, str]:
    """
    Mark a todo as incomplete.

    Args:
        todo_id: ID of todo to mark incomplete (any type, will be validated)

    Returns:
        tuple: (success, message)
            - success (bool): True if todo was marked incomplete
            - message (str): Success message or error message

    Behavior:
        - Sets completed=False on the todo
        - Idempotent: marking already-incomplete todo succeeds
        - Validates ID and checks existence before modifying

    Error Messages (from CLI contract):
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."

    Success Message (from CLI contract):
        - "Todo ID {id} marked as incomplete!"

    Examples:
        >>> add_todo("Buy groceries", "")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> mark_complete(1)
        (True, "Todo ID 1 marked as complete!")
        >>> mark_incomplete(1)
        (True, "Todo ID 1 marked as incomplete!")
        >>> mark_incomplete(1)  # Idempotent
        (True, "Todo ID 1 marked as incomplete!")
    """
    from models import validate_id

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Mark as incomplete (idempotent - no check if already incomplete)
    todo["completed"] = False

    # Return success
    return (True, f"Todo ID {parsed_id} marked as incomplete!")


def update_todo(todo_id: any, new_title: str | None, new_description: str | None) -> tuple[bool, str]:
    """
    Update title and/or description of an existing todo.

    Args:
        todo_id: ID of todo to update (any type, will be validated)
        new_title: New title (None to keep current)
        new_description: New description (None to keep current)

    Returns:
        tuple: (success, message)
            - success (bool): True if todo was updated
            - message (str): Success message or error message

    Behavior:
        - None values preserve current field values
        - Validates new values before updating
        - At least one field must be provided (can't both be None)

    Error Messages (from CLI contract):
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."
        - Empty title: "Error: Title cannot be empty."
        - Title too long: "Error: Title exceeds 200 character limit."
        - Description too long: "Error: Description exceeds 1000 character limit."

    Success Message (from CLI contract):
        - "Todo ID {id} updated successfully!"

    Examples:
        >>> add_todo("Buy groceries", "Milk")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> update_todo(1, "Buy organic groceries", None)
        (True, "Todo ID 1 updated successfully!")
        >>> update_todo(1, None, "Milk, eggs, bread")
        (True, "Todo ID 1 updated successfully!")
        >>> update_todo(999, "New title", None)
        (False, "Error: Todo with ID 999 not found.")
    """
    from models import validate_id, validate_title, validate_description

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Update title if provided
    if new_title is not None:
        # Validate new title
        title_valid, title_error = validate_title(new_title)
        if not title_valid:
            return (False, title_error)

        # Update title
        todo["title"] = new_title

    # Update description if provided
    if new_description is not None:
        # Validate new description
        desc_valid, desc_error = validate_description(new_description)
        if not desc_valid:
            return (False, desc_error)

        # Update description
        todo["description"] = new_description

    # Return success
    return (True, f"Todo ID {parsed_id} updated successfully!")


def delete_todo(todo_id: any) -> tuple[bool, str]:
    """
    Delete a todo from storage by ID.

    Args:
        todo_id: ID of todo to delete (any type, will be validated)

    Returns:
        tuple: (success, message)
            - success (bool): True if todo was deleted
            - message (str): Success message or error message

    Behavior:
        - Removes todo from global todos list
        - IDs are never reused (next_id counter not affected)
        - Remaining todos keep their original IDs

    Error Messages (from CLI contract):
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."

    Success Message (from CLI contract):
        - "Todo ID {id} deleted successfully!"

    Examples:
        >>> add_todo("Task 1", "")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> add_todo("Task 2", "")
        (True, 2, "Todo added successfully! (ID: 2)")
        >>> delete_todo(1)
        (True, "Todo ID 1 deleted successfully!")
        >>> get_all_todos()
        [{'id': 2, 'title': 'Task 2', ...}]  # Only ID 2 remains
        >>> delete_todo(999)
        (False, "Error: Todo with ID 999 not found.")
    """
    from models import validate_id

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Find todo in list
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Remove from list
    todos.remove(todo)

    # Return success
    return (True, f"Todo ID {parsed_id} deleted successfully!")


def update_priority(todo_id: any, new_priority: str) -> tuple[bool, str]:
    """
    Update priority of an existing todo (Phase II - User Story 5).

    Args:
        todo_id: ID of todo to update (any type, will be validated)
        new_priority: New priority value ("High", "Medium", "Low")

    Returns:
        tuple: (success, message)
            - success (bool): True if priority was updated
            - message (str): Success message or error message

    Behavior:
        - Validates todo ID
        - Validates new priority value
        - Updates priority field in todo
        - Case-insensitive priority input (normalized to proper case)

    Error Messages:
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."
        - Invalid priority: "Error: Priority must be High, Medium, or Low."

    Success Message:
        - "Todo ID {id} priority updated to {priority}!"

    Examples:
        >>> add_todo("Buy groceries", "Milk")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> update_priority(1, "High")
        (True, "Todo ID 1 priority updated to High!")
        >>> update_priority(1, "urgent")
        (False, "Error: Priority must be High, Medium, or Low.")
        >>> update_priority(999, "High")
        (False, "Error: Todo with ID 999 not found.")
    """
    from models import validate_id, validate_priority

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Validate priority
    priority_valid, normalized_priority, priority_error = validate_priority(new_priority)
    if not priority_valid:
        return (False, priority_error)

    # Update priority
    todo["priority"] = normalized_priority

    # Return success
    return (True, f"Todo ID {parsed_id} priority updated to {normalized_priority}!")
