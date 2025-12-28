"""
Data validation functions for todo items.

This module provides validation logic for todo entity fields
(title, description, ID) according to the specification in
specs/001-cli-todo-app/data-model.md

Validation Functions:
    validate_id: Validates and parses ID input (must be positive integer)
    validate_title: Validates todo title (required, 1-200 chars)
    validate_description: Validates todo description (optional, 0-1000 chars)
    create_todo: Creates a todo dictionary with validated fields

Returns:
    All validation functions return tuples indicating success/failure with error messages
"""


def validate_id(id_value: any) -> tuple[bool, int | None, str]:
    """
    Validate ID input and convert to positive integer.

    Args:
        id_value: User input for ID (any type)

    Returns:
        tuple: (valid, parsed_id, error_message)
            - valid (bool): True if validation passed
            - parsed_id (int | None): Parsed integer ID if valid, None otherwise
            - error_message (str): Error message if invalid, empty string if valid

    Validation Rules:
        - Must be convertible to integer
        - Must be positive (> 0)

    Error Messages:
        - Non-numeric: "Error: ID must be a positive integer."
        - Zero or negative: "Error: ID must be a positive integer."

    Examples:
        >>> validate_id("5")
        (True, 5, "")
        >>> validate_id("abc")
        (False, None, "Error: ID must be a positive integer.")
        >>> validate_id("-1")
        (False, None, "Error: ID must be a positive integer.")
    """
    try:
        # Try to convert to integer
        parsed_id = int(id_value)

        # Check if positive
        if parsed_id <= 0:
            return (False, None, "Error: ID must be a positive integer.")

        return (True, parsed_id, "")

    except (ValueError, TypeError):
        # Not convertible to integer
        return (False, None, "Error: ID must be a positive integer.")


def validate_title(title: str | None) -> tuple[bool, str]:
    """
    Validate todo title.

    Args:
        title: Title string to validate

    Returns:
        tuple: (valid, error_message)
            - valid (bool): True if validation passed
            - error_message (str): Error message if invalid, empty string if valid

    Validation Rules (data-model.md lines 79-81):
        - Title cannot be None or empty string
        - Title cannot be only whitespace
        - Title must be between 1-200 characters

    Error Messages:
        - Empty/None: "Error: Title cannot be empty."
        - Too long: "Error: Title exceeds 200 character limit."

    Examples:
        >>> validate_title("Buy groceries")
        (True, "")
        >>> validate_title("")
        (False, "Error: Title cannot be empty.")
        >>> validate_title("a" * 201)
        (False, "Error: Title exceeds 200 character limit.")
    """
    # Check for None or empty
    if title is None or title == "" or title.strip() == "":
        return (False, "Error: Title cannot be empty.")

    # Check length
    if len(title) > 200:
        return (False, "Error: Title exceeds 200 character limit.")

    return (True, "")


def validate_description(description: str | None) -> tuple[bool, str]:
    """
    Validate todo description.

    Args:
        description: Description string to validate (optional)

    Returns:
        tuple: (valid, error_message)
            - valid (bool): True if validation passed
            - error_message (str): Error message if invalid, empty string if valid

    Validation Rules (data-model.md lines 83-85):
        - Description is optional (None converts to empty string)
        - Description must be 0-1000 characters

    Error Messages:
        - Too long: "Error: Description exceeds 1000 character limit."

    Examples:
        >>> validate_description("Milk, eggs, bread")
        (True, "")
        >>> validate_description(None)
        (True, "")
        >>> validate_description("a" * 1001)
        (False, "Error: Description exceeds 1000 character limit.")
    """
    # None is valid (optional field, will be converted to empty string)
    if description is None:
        return (True, "")

    # Empty string is valid
    if description == "":
        return (True, "")

    # Check length
    if len(description) > 1000:
        return (False, "Error: Description exceeds 1000 character limit.")

    return (True, "")


def validate_priority(priority: str | None) -> tuple[bool, str | None, str]:
    """
    Validate and normalize priority value (Phase II - User Story 5).

    Args:
        priority: Priority string to validate ("High", "Medium", "Low")
                 Case-insensitive, will be normalized

    Returns:
        tuple: (valid, normalized_priority, error_message)
            - valid (bool): True if validation passed
            - normalized_priority (str | None): Normalized priority if valid, None otherwise
            - error_message (str): Error message if invalid, empty string if valid

    Validation Rules:
        - Must be one of: "High", "Medium", "Low" (case-insensitive)
        - Leading/trailing whitespace is trimmed
        - Normalized to proper case: "High", "Medium", "Low"

    Error Messages:
        - Invalid priority: "Error: Priority must be High, Medium, or Low."

    Examples:
        >>> validate_priority("high")
        (True, "High", "")
        >>> validate_priority("MEDIUM")
        (True, "Medium", "")
        >>> validate_priority("urgent")
        (False, None, "Error: Priority must be High, Medium, or Low.")
    """
    # Valid priority values (normalized)
    VALID_PRIORITIES = {"high": "High", "medium": "Medium", "low": "Low"}

    # Check for None or empty
    if priority is None or (isinstance(priority, str) and priority.strip() == ""):
        return (False, None, "Error: Priority must be High, Medium, or Low.")

    # Convert to string and normalize (strip whitespace, lowercase for comparison)
    priority_str = str(priority).strip().lower()

    # Check if valid
    if priority_str in VALID_PRIORITIES:
        normalized = VALID_PRIORITIES[priority_str]
        return (True, normalized, "")
    else:
        return (False, None, "Error: Priority must be High, Medium, or Low.")


def validate_tags(tags: str | list[str] | None) -> tuple[bool, list[str] | None, str]:
    """
    Validate and normalize tags (Phase II - User Story 6).

    Args:
        tags: Tags to validate - can be:
              - String: comma-separated tags "work, urgent, personal"
              - List: ["work", "urgent", "personal"]
              - None: returns empty list

    Returns:
        tuple: (valid, normalized_tags, error_message)
            - valid (bool): True if validation passed
            - normalized_tags (list[str] | None): Normalized tag list if valid, None otherwise
            - error_message (str): Error message if invalid, empty string if valid

    Validation Rules:
        - Each tag must be 1-20 characters
        - Tags normalized to lowercase (case-insensitive)
        - Leading/trailing whitespace trimmed
        - Duplicate tags removed
        - Empty tags ignored

    Error Messages:
        - Tag too long: "Error: Each tag must be 1-20 characters."

    Examples:
        >>> validate_tags("work, urgent")
        (True, ["work", "urgent"], "")
        >>> validate_tags("Work, URGENT, work")
        (True, ["work", "urgent"], "")
        >>> validate_tags(["Personal", "Shopping"])
        (True, ["personal", "shopping"], "")
    """
    # Handle None - return empty list
    if tags is None:
        return (True, [], "")

    # Handle empty string - return empty list
    if isinstance(tags, str) and tags.strip() == "":
        return (True, [], "")

    # Convert to list if string (split by comma)
    if isinstance(tags, str):
        tag_list = [tag.strip() for tag in tags.split(",")]
    elif isinstance(tags, list):
        tag_list = [str(tag).strip() for tag in tags]
    else:
        tag_list = [str(tags).strip()]

    # Remove empty tags and normalize
    normalized_tags = []
    seen = set()  # Track duplicates (case-insensitive)

    for tag in tag_list:
        # Skip empty tags
        if not tag:
            continue

        # Check length
        if len(tag) > 20:
            return (False, None, "Error: Each tag must be 1-20 characters.")

        # Normalize to lowercase
        tag_lower = tag.lower()

        # Skip duplicates (case-insensitive)
        if tag_lower in seen:
            continue

        seen.add(tag_lower)
        normalized_tags.append(tag_lower)

    return (True, normalized_tags, "")


def migrate_todo_to_phase2(todo: dict) -> dict:
    """
    Migrate a Phase I todo to Phase II by adding priority, tags, and created_at fields.

    This function is idempotent - it safely handles todos that already have Phase II fields.

    Args:
        todo: Todo dictionary (Phase I or Phase II format)

    Returns:
        dict: Todo with Phase II fields guaranteed to exist

    Phase II Migration Rules:
        - If "priority" missing: Add with default "Medium"
        - If "tags" missing: Add with default []
        - If "created_at" missing: Add with current timestamp
        - All Phase I fields (id, title, description, completed) preserved unchanged

    Examples:
        >>> phase1_todo = {"id": 1, "title": "Buy milk", "description": "", "completed": False}
        >>> migrated = migrate_todo_to_phase2(phase1_todo)
        >>> migrated["priority"]
        'Medium'
        >>> migrated["tags"]
        []
        >>> "created_at" in migrated
        True
    """
    from datetime import datetime

    # Create new dict to avoid mutating input
    migrated = todo.copy()

    # Add Phase II fields with defaults if missing
    if "priority" not in migrated:
        migrated["priority"] = "Medium"

    if "tags" not in migrated:
        migrated["tags"] = []

    if "created_at" not in migrated:
        migrated["created_at"] = datetime.now()

    return migrated


def create_todo(id: int, title: str, description: str,
                priority: str = "Medium", tags: list[str] | None = None) -> dict:
    """
    Create a todo dictionary with validated fields (Phase II enhanced).

    Args:
        id: Unique positive integer ID
        title: Todo title (already validated)
        description: Todo description (already validated, None converted to "")
        priority: Priority level - "High", "Medium" (default), or "Low"
        tags: List of tags (optional, default empty list)

    Returns:
        dict: Todo dictionary with Phase I and Phase II fields

    Data Structure (Phase II - specs/002-cli-todo-app-enhanced/spec.md):
        {
            "id": int,
            "title": str,
            "description": str,
            "completed": bool (default False),
            "priority": str (default "Medium"),
            "tags": list[str] (default []),
            "created_at": datetime (auto-assigned)
        }

    Examples:
        >>> create_todo(1, "Buy groceries", "Milk, eggs")
        {'id': 1, 'title': 'Buy groceries', 'description': 'Milk, eggs',
         'completed': False, 'priority': 'Medium', 'tags': [], 'created_at': ...}
        >>> create_todo(1, "Fix bug", "Auth issue", priority="High", tags=["work", "urgent"])
        {..., 'priority': 'High', 'tags': ['work', 'urgent'], ...}
    """
    from datetime import datetime

    # Convert None description to empty string
    if description is None:
        description = ""

    # Convert None tags to empty list
    if tags is None:
        tags = []

    return {
        "id": id,
        "title": title,
        "description": description,
        "completed": False,  # All new todos start as incomplete
        "priority": priority,  # Phase II: Default "Medium"
        "tags": tags,  # Phase II: Default []
        "created_at": datetime.now()  # Phase II: Auto-assigned timestamp
    }
