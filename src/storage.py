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
    Retrieve all todos sorted by ID ascending (Phase III enhanced with migration).

    Returns:
        list[dict]: List of all todo dictionaries, sorted by ID ascending
            Returns empty list if no todos exist
            All todos guaranteed to have Phase III fields (priority, tags, created_at, recurrence)

    Sorting Rules:
        - Per CLI contract (line 110): Todos displayed in ID ascending order
        - Ensures consistent display order regardless of insertion order

    Migration Behavior (Phase III):
        - Automatically migrates Phase I/II todos to Phase III format
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
        >>> todos[0]['recurrence_pattern']  # Phase III field
        None
    """
    from models import migrate_todo_to_phase2, migrate_todo_to_phase3

    # Migrate all todos to Phase III format in-place (idempotent)
    # This ensures backward compatibility with Phase I and Phase II todos
    global todos
    for i in range(len(todos)):
        todos[i] = migrate_todo_to_phase2(todos[i])  # Phase I → Phase II
        todos[i] = migrate_todo_to_phase3(todos[i])  # Phase II → Phase III

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
    Mark a todo as complete (Phase III enhanced with recurring tasks).

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
        - Phase III: If todo has recurrence pattern, creates next instance

    Error Messages (from CLI contract):
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."

    Success Message (from CLI contract):
        - "Todo ID {id} marked as complete!"
        - Phase III: "Todo ID {id} marked as complete! Next occurrence created (ID: {new_id})."

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
    from models import validate_id, create_todo
    from datetime import datetime
    global next_id

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

    # Phase III: Handle recurring tasks
    recurrence_pattern = todo.get("recurrence_pattern")
    if recurrence_pattern is not None and recurrence_pattern in ["Daily", "Weekly", "Monthly"]:
        # Calculate next occurrence
        interval = todo.get("recurrence_interval", 1)
        base_date = datetime.now()
        next_date = calculate_next_occurrence(base_date, recurrence_pattern, interval)

        # Create new instance of the recurring todo
        new_id = next_id
        new_todo = create_todo(
            new_id,
            todo["title"],
            todo["description"],
            priority=todo.get("priority", "Medium"),
            tags=todo.get("tags", []).copy(),  # Copy tags list
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=interval
        )
        new_todo["next_occurrence"] = next_date

        # Add to global list and increment counter
        todos.append(new_todo)
        next_id += 1

        return (True, f"Todo ID {parsed_id} marked as complete! Next occurrence created (ID: {new_id}).")

    # Return success (non-recurring todo)
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


def add_tags(todo_id: any, new_tags: str | list[str]) -> tuple[bool, str]:
    """
    Add tags to an existing todo (Phase II - User Story 6).

    Args:
        todo_id: ID of todo to update (any type, will be validated)
        new_tags: Tags to add (string or list)

    Returns:
        tuple: (success, message)
            - success (bool): True if tags were added
            - message (str): Success message or error message

    Behavior:
        - Validates todo ID
        - Validates and normalizes new tags
        - Adds tags to existing tags (no duplicates)
        - Preserves existing tags

    Error Messages:
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."
        - Invalid tags: "Error: Each tag must be 1-20 characters."

    Success Message:
        - "Tags added to todo ID {id}!"

    Examples:
        >>> add_todo("Buy groceries", "Milk")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> add_tags(1, "work, urgent")
        (True, "Tags added to todo ID 1!")
    """
    from models import validate_id, validate_tags

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Validate new tags
    tags_valid, normalized_tags, tags_error = validate_tags(new_tags)
    if not tags_valid:
        return (False, tags_error)

    # Get existing tags
    existing_tags = todo.get("tags", [])

    # Merge tags (avoid duplicates)
    existing_tags_set = set(existing_tags)
    for tag in normalized_tags:
        if tag not in existing_tags_set:
            existing_tags.append(tag)
            existing_tags_set.add(tag)

    # Update tags
    todo["tags"] = existing_tags

    # Return success
    return (True, f"Tags added to todo ID {parsed_id}!")


def remove_tags(todo_id: any, tags_to_remove: str | list[str]) -> tuple[bool, str]:
    """
    Remove tags from an existing todo (Phase II - User Story 6).

    Args:
        todo_id: ID of todo to update (any type, will be validated)
        tags_to_remove: Tags to remove (string or list)

    Returns:
        tuple: (success, message)
            - success (bool): True if tags were removed
            - message (str): Success message or error message

    Behavior:
        - Validates todo ID
        - Normalizes tags to remove (case-insensitive)
        - Removes specified tags from todo
        - Silently ignores tags that don't exist

    Error Messages:
        - Invalid ID: "Error: ID must be a positive integer."
        - Not found: "Error: Todo with ID {id} not found."

    Success Message:
        - "Tags removed from todo ID {id}!"

    Examples:
        >>> add_todo("Buy groceries", "Milk")
        (True, 1, "Todo added successfully! (ID: 1)")
        >>> add_tags(1, "work, urgent")
        (True, "Tags added to todo ID 1!")
        >>> remove_tags(1, "urgent")
        (True, "Tags removed from todo ID 1!")
    """
    from models import validate_id, validate_tags

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Validate tags to remove (for normalization)
    tags_valid, normalized_tags, tags_error = validate_tags(tags_to_remove)
    if not tags_valid:
        return (False, tags_error)

    # Get existing tags
    existing_tags = todo.get("tags", [])

    # Remove specified tags (case-insensitive)
    tags_to_remove_set = set(normalized_tags)
    updated_tags = [tag for tag in existing_tags if tag not in tags_to_remove_set]

    # Update tags
    todo["tags"] = updated_tags

    # Return success
    return (True, f"Tags removed from todo ID {parsed_id}!")


def search_todos(keyword: str) -> list[dict]:
    """
    Search todos by keyword in title and description (Phase II - User Story 7).

    Args:
        keyword: Search keyword (case-insensitive)

    Returns:
        list[dict]: List of todos matching the keyword

    Behavior:
        - Searches both title and description fields
        - Case-insensitive matching
        - Partial matches allowed (substring search)
        - Empty keyword returns all todos
        - Returns empty list if no matches

    Examples:
        >>> add_todo("Buy groceries", "Milk, eggs")
        >>> add_todo("Call dentist", "Schedule checkup")
        >>> results = search_todos("buy")
        >>> len(results)
        1
        >>> results[0]["title"]
        'Buy groceries'
    """
    # Empty keyword returns all todos
    if not keyword or keyword.strip() == "":
        return get_all_todos()

    # Normalize keyword to lowercase for case-insensitive search
    keyword_lower = keyword.lower()

    # Filter todos by keyword match in title or description
    results = []
    for todo in get_all_todos():
        title_lower = todo["title"].lower()
        description_lower = todo["description"].lower()

        # Check if keyword appears in title or description
        if keyword_lower in title_lower or keyword_lower in description_lower:
            results.append(todo)

    return results


def filter_by_status(todos: list[dict], completed: bool) -> list[dict]:
    """
    Filter todos by completion status (Phase II - User Story 7).

    Args:
        todos: List of todos to filter
        completed: True for completed todos, False for incomplete

    Returns:
        list[dict]: Filtered list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Returns todos matching the specified status
        - Empty input returns empty list

    Examples:
        >>> todos = get_all_todos()
        >>> incomplete = filter_by_status(todos, False)
        >>> completed = filter_by_status(todos, True)
    """
    return [todo for todo in todos if todo["completed"] == completed]


def filter_by_priority(todos: list[dict], priority: str) -> list[dict]:
    """
    Filter todos by priority level (Phase II - User Story 7).

    Args:
        todos: List of todos to filter
        priority: Priority level ("High", "Medium", "Low") - case-insensitive

    Returns:
        list[dict]: Filtered list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Case-insensitive priority matching
        - Returns todos matching the specified priority
        - Empty input returns empty list

    Examples:
        >>> todos = get_all_todos()
        >>> high_priority = filter_by_priority(todos, "High")
        >>> medium_priority = filter_by_priority(todos, "medium")
    """
    # Normalize priority to lowercase for case-insensitive comparison
    priority_lower = priority.lower()

    return [
        todo for todo in todos
        if todo.get("priority", "Medium").lower() == priority_lower
    ]


def filter_by_tag(todos: list[dict], tag: str) -> list[dict]:
    """
    Filter todos by tag (Phase II - User Story 7).

    Args:
        todos: List of todos to filter
        tag: Tag to filter by (case-insensitive)

    Returns:
        list[dict]: Filtered list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Case-insensitive tag matching
        - Returns todos that have the specified tag
        - Empty input returns empty list
        - Handles todos without tags field

    Examples:
        >>> todos = get_all_todos()
        >>> work_todos = filter_by_tag(todos, "work")
        >>> urgent_todos = filter_by_tag(todos, "URGENT")
    """
    # Normalize tag to lowercase for case-insensitive comparison
    tag_lower = tag.lower()

    results = []
    for todo in todos:
        # Get tags list (default to empty list if missing)
        todo_tags = todo.get("tags", [])

        # Check if tag exists in todo's tags (case-insensitive)
        if tag_lower in todo_tags:
            results.append(todo)

    return results


def sort_by_title(todos: list[dict], ascending: bool = True) -> list[dict]:
    """
    Sort todos alphabetically by title (Phase II - User Story 8).

    Args:
        todos: List of todos to sort
        ascending: True for A-Z, False for Z-A (default: True)

    Returns:
        list[dict]: Sorted list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Case-insensitive sorting
        - Alphabetical order (A-Z or Z-A)

    Examples:
        >>> todos = get_all_todos()
        >>> sorted_asc = sort_by_title(todos, ascending=True)
        >>> sorted_desc = sort_by_title(todos, ascending=False)
    """
    return sorted(todos, key=lambda todo: todo["title"].lower(), reverse=not ascending)


def sort_by_priority(todos: list[dict], high_first: bool = True) -> list[dict]:
    """
    Sort todos by priority level (Phase II - User Story 8).

    Args:
        todos: List of todos to sort
        high_first: True for High→Medium→Low, False for Low→Medium→High (default: True)

    Returns:
        list[dict]: Sorted list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Priority order: High (1) → Medium (2) → Low (3)
        - Reverse priority order: Low (3) → Medium (2) → High (1)

    Examples:
        >>> todos = get_all_todos()
        >>> high_first = sort_by_priority(todos, high_first=True)
        >>> low_first = sort_by_priority(todos, high_first=False)
    """
    # Priority ranking for sorting
    priority_rank = {"High": 1, "Medium": 2, "Low": 3}

    # Get priority rank, default to Medium if missing
    def get_priority_rank(todo):
        priority = todo.get("priority", "Medium")
        return priority_rank.get(priority, 2)

    return sorted(todos, key=get_priority_rank, reverse=not high_first)


def sort_by_created_date(todos: list[dict], newest_first: bool = True) -> list[dict]:
    """
    Sort todos by creation date (Phase II - User Story 8).

    Args:
        todos: List of todos to sort
        newest_first: True for newest first, False for oldest first (default: True)

    Returns:
        list[dict]: Sorted list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Sorts by created_at timestamp
        - Newest first (descending) or oldest first (ascending)

    Examples:
        >>> todos = get_all_todos()
        >>> newest = sort_by_created_date(todos, newest_first=True)
        >>> oldest = sort_by_created_date(todos, newest_first=False)
    """
    return sorted(todos, key=lambda todo: todo.get("created_at"), reverse=newest_first)


def sort_by_status(todos: list[dict], incomplete_first: bool = True) -> list[dict]:
    """
    Sort todos by completion status (Phase II - User Story 8).

    Args:
        todos: List of todos to sort
        incomplete_first: True for incomplete first, False for completed first (default: True)

    Returns:
        list[dict]: Sorted list of todos

    Behavior:
        - Pure function: doesn't modify input list
        - Incomplete (False) first or completed (True) first
        - Within same status, maintains original order

    Examples:
        >>> todos = get_all_todos()
        >>> incomplete_first = sort_by_status(todos, incomplete_first=True)
        >>> completed_first = sort_by_status(todos, incomplete_first=False)
    """
    # Convert boolean to sort key: False (incomplete) = 0, True (complete) = 1
    # If incomplete_first=True: incomplete (0) comes before complete (1)
    # If incomplete_first=False: complete (1) comes before incomplete (0) → reverse
    return sorted(todos, key=lambda todo: todo["completed"], reverse=not incomplete_first)


def set_recurrence(todo_id: any, pattern: str, interval: int = 1) -> tuple[bool, str]:
    """
    Set recurrence pattern for an existing todo (Phase III - User Story 9).

    Args:
        todo_id: ID of todo to update
        pattern: Recurrence pattern ("None", "Daily", "Weekly", "Monthly")
        interval: Recurrence interval (default 1)

    Returns:
        tuple: (success, message)

    Examples:
        >>> set_recurrence(1, "Daily")
        (True, "Todo ID 1 recurrence set to Daily!")
        >>> set_recurrence(1, "None")
        (True, "Todo ID 1 recurrence removed!")
    """
    from models import validate_id, validate_recurrence_pattern

    # Validate ID
    valid, parsed_id, error = validate_id(todo_id)
    if not valid:
        return (False, error)

    # Get todo
    todo = get_todo_by_id(parsed_id)
    if todo is None:
        return (False, f"Error: Todo with ID {parsed_id} not found.")

    # Validate recurrence pattern
    pattern_valid, normalized_pattern, pattern_error = validate_recurrence_pattern(pattern)
    if not pattern_valid:
        return (False, pattern_error)

    # Set recurrence
    todo["recurrence_pattern"] = normalized_pattern
    todo["recurrence_interval"] = interval if normalized_pattern is not None else 1
    todo["next_occurrence"] = None  # Will be calculated when needed

    # Return success message
    if normalized_pattern is None:
        return (True, f"Todo ID {parsed_id} recurrence removed!")
    else:
        return (True, f"Todo ID {parsed_id} recurrence set to {normalized_pattern}!")


def calculate_next_occurrence(base_date, pattern: str, interval: int = 1):
    """
    Calculate the next occurrence date based on recurrence pattern.

    Args:
        base_date: Starting date (datetime object)
        pattern: Recurrence pattern ("Daily", "Weekly", "Monthly")
        interval: Recurrence interval (default 1)

    Returns:
        datetime: Next occurrence date

    Examples:
        >>> from datetime import datetime
        >>> base = datetime(2025, 1, 1)
        >>> calculate_next_occurrence(base, "Daily", 1)
        datetime(2025, 1, 2, ...)
        >>> calculate_next_occurrence(base, "Weekly", 2)
        datetime(2025, 1, 15, ...)
    """
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta

    if pattern == "Daily":
        return base_date + timedelta(days=interval)
    elif pattern == "Weekly":
        return base_date + timedelta(weeks=interval)
    elif pattern == "Monthly":
        return base_date + relativedelta(months=interval)
    else:
        return None
