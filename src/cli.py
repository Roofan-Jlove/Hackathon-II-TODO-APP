"""
CLI user interaction functions for todo manager.

This module handles menu display, user input collection, and
output formatting according to the CLI interface contract in
specs/001-cli-todo-app/contracts/cli-interface.md

Functions:
    display_menu: Display main menu options
    get_menu_choice: Get and validate user menu choice
    display_todos: Format and display todo list
    get_user_input: Helper for prompting user input
"""


def display_menu() -> None:
    """
    Display the main menu to the user.

    Contract: Must display exact menu format per CLI contract
    (specs/001-cli-todo-app/contracts/cli-interface.md lines 10-25)

    Output:
        Welcome to Todo Manager
        -----------------------
        1. Add Todo
        2. List All Todos
        3. Update Todo
        4. Delete Todo
        5. Mark Todo Complete
        6. Mark Todo Incomplete
        7. Exit

        Enter choice [1-7]:
    """
    print("Welcome to Todo Manager")
    print("-----------------------")
    print("1. Add Todo")
    print("2. List All Todos")
    print("3. Update Todo")
    print("4. Delete Todo")
    print("5. Mark Todo Complete")
    print("6. Mark Todo Incomplete")
    print("7. Exit")
    print()


def get_menu_choice() -> str:
    """
    Get user's menu choice.

    Prompts the user with "Enter choice [1-7]: " and returns their input.

    Returns:
        str: User's menu choice (not validated - validation happens in main loop)

    Contract: Exact prompt format per CLI contract
    (specs/001-cli-todo-app/contracts/cli-interface.md line 24)
    """
    return input("Enter choice [1-7]: ")


def display_todos(todos: list[dict]) -> None:
    """
    Display all todos in formatted table or empty message.

    Args:
        todos: List of todo dictionaries (already sorted by ID ascending)

    Output Format (per CLI contract lines 90-111):
        - Empty list: "No todos found."
        - Table with header, separator, and data rows
        - Status: [ ] for incomplete, [X] for complete
        - Empty description shown as blank

    Examples:
        Empty list:
            No todos found.

        Populated list:
            ID | Status | Title           | Description
            ---|--------|-----------------|------------------
            1  | [ ]    | Buy groceries   | Milk, eggs, bread
            2  | [X]    | Call dentist    | Schedule checkup
            3  | [ ]    | Write report    |
    """
    # Empty list case
    if not todos:
        print("No todos found.")
        return

    # Table header
    print("ID | Status | Title           | Description")
    print("---|--------|-----------------|------------------")

    # Data rows
    for todo in todos:
        todo_id = todo["id"]
        status = "[X]" if todo["completed"] else "[ ]"
        title = todo["title"]
        description = todo["description"]

        # Format: ID | Status | Title | Description
        print(f"{todo_id:<2} | {status:<6} | {title:<15} | {description}")


def handle_add() -> None:
    """
    Handle Add Todo operation with user prompts and validation.

    Input Prompts (per CLI contract lines 42-54):
        1. "Enter title: "
        2. "Enter description (optional, press Enter to skip): "

    Output (per CLI contract lines 58-71):
        - Success: "Todo added successfully! (ID: N)"
        - Error: Validation error message from storage layer

    Flow:
        1. Prompt for title
        2. Prompt for description (optional)
        3. Call storage.add_todo()
        4. Display result message
    """
    from storage import add_todo

    # Prompt for title
    title = input("Enter title: ")

    # Prompt for description (optional)
    description = input("Enter description (optional, press Enter to skip): ")

    # Convert empty string to None for optional description
    if description == "":
        description = None

    # Call storage layer
    success, todo_id, message = add_todo(title, description)

    # Display result
    print(message)


def handle_list() -> None:
    """
    Handle List All Todos operation.

    No additional input required (per CLI contract line 86)

    Flow:
        1. Get all todos from storage (already sorted)
        2. Display using display_todos()
    """
    from storage import get_all_todos

    # Get all todos (already sorted by ID ascending)
    todos = get_all_todos()

    # Display todos
    display_todos(todos)


def handle_mark_complete() -> None:
    """
    Handle Mark Todo Complete operation.

    Input Prompt (per CLI contract line 188):
        "Enter todo ID: "

    Output (per CLI contract lines 196-205):
        - Success: "Todo ID N marked as complete!"
        - Error: "Error: Todo with ID N not found." or "Error: ID must be a positive integer."

    Flow:
        1. Prompt for todo ID
        2. Call storage.mark_complete()
        3. Display result message
    """
    from storage import mark_complete

    # Prompt for ID
    todo_id = input("Enter todo ID: ")

    # Call storage layer
    success, message = mark_complete(todo_id)

    # Display result
    print(message)


def handle_mark_incomplete() -> None:
    """
    Handle Mark Todo Incomplete operation.

    Input Prompt (per CLI contract line 215):
        "Enter todo ID: "

    Output (per CLI contract lines 224-229):
        - Success: "Todo ID N marked as incomplete!"
        - Error: "Error: Todo with ID N not found." or "Error: ID must be a positive integer."

    Flow:
        1. Prompt for todo ID
        2. Call storage.mark_incomplete()
        3. Display result message
    """
    from storage import mark_incomplete

    # Prompt for ID
    todo_id = input("Enter todo ID: ")

    # Call storage layer
    success, message = mark_incomplete(todo_id)

    # Display result
    print(message)


def handle_update() -> None:
    """
    Handle Update Todo operation.

    Input Prompts (per CLI contract lines 119-138):
        1. "Enter todo ID: "
        2. "Enter new title (leave blank to keep current): "
        3. "Enter new description (leave blank to keep current): "

    Output (per CLI contract lines 142-155):
        - Success: "Todo ID N updated successfully!"
        - Error: Various validation errors from storage layer

    Behavior:
        - Blank input (press Enter) preserves current value
        - Empty string for title converts to None (keeps current)
        - Empty string for description converts to None (keeps current)

    Flow:
        1. Prompt for todo ID
        2. Prompt for new title (blank to keep current)
        3. Prompt for new description (blank to keep current)
        4. Call storage.update_todo()
        5. Display result message
    """
    from storage import update_todo

    # Prompt for ID
    todo_id = input("Enter todo ID: ")

    # Prompt for new title (blank to keep current)
    new_title = input("Enter new title (leave blank to keep current): ")
    if new_title == "":
        new_title = None  # None means keep current value

    # Prompt for new description (blank to keep current)
    new_description = input("Enter new description (leave blank to keep current): ")
    if new_description == "":
        new_description = None  # None means keep current value

    # Call storage layer
    success, message = update_todo(todo_id, new_title, new_description)

    # Display result
    print(message)


def handle_delete() -> None:
    """
    Handle Delete Todo operation.

    Input Prompt (per CLI contract line 163):
        "Enter todo ID to delete: "

    Output (per CLI contract lines 170-180):
        - Success: "Todo ID N deleted successfully!"
        - Error: "Error: Todo with ID N not found." or "Error: ID must be a positive integer."

    Flow:
        1. Prompt for todo ID
        2. Call storage.delete_todo()
        3. Display result message
    """
    from storage import delete_todo

    # Prompt for ID
    todo_id = input("Enter todo ID to delete: ")

    # Call storage layer
    success, message = delete_todo(todo_id)

    # Display result
    print(message)
