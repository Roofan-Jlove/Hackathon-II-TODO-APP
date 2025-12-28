"""
CLI user interaction functions for todo manager.

This module handles menu display, user input collection, and
output formatting according to the CLI interface contract in
specs/001-cli-todo-app/contracts/cli-interface.md

Functions:
    display_menu: Display main menu options (with colors and emojis)
    get_menu_choice: Get and validate user menu choice
    display_todos: Format and display todo list
    get_user_input: Helper for prompting user input
"""

from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


def display_menu() -> None:
    """
    Display the main menu to the user with colors and emojis.

    Enhanced with:
        - Colorful welcome banner
        - Emoji icons for each menu option
        - Color-coded menu items

    Output:
        ╔════════════════════════════════════════╗
        ║  🎯  WELCOME TO TODO APP  🎯           ║
        ╚════════════════════════════════════════╝

        📌 MAIN MENU:
        ➕  1. Add Todo
        📋  2. List All Todos
        ✏️   3. Update Todo
        🗑️   4. Delete Todo
        ✅  5. Mark Todo Complete
        ⬜  6. Mark Todo Incomplete
        👋  7. Exit

        Enter choice [1-7]:
    """
    # Colorful banner
    print()
    print(Fore.CYAN + Style.BRIGHT + "=" * 45)
    print(Fore.YELLOW + Style.BRIGHT + "   🎯  WELCOME TO TODO APP  🎯   ")
    print(Fore.CYAN + Style.BRIGHT + "=" * 45)
    print(Style.RESET_ALL)

    # Menu header
    print(Fore.MAGENTA + Style.BRIGHT + "📌 MAIN MENU:")
    print()

    # Menu options with emojis and colors
    print(Fore.GREEN + "  ➕  1. " + Style.RESET_ALL + "Add Todo")
    print(Fore.BLUE + "  📋  2. " + Style.RESET_ALL + "List All Todos")
    print(Fore.YELLOW + "  ✏️   3. " + Style.RESET_ALL + "Update Todo")
    print(Fore.RED + "  🗑️   4. " + Style.RESET_ALL + "Delete Todo")
    print(Fore.GREEN + "  ✅  5. " + Style.RESET_ALL + "Mark Todo Complete")
    print(Fore.WHITE + "  ⬜  6. " + Style.RESET_ALL + "Mark Todo Incomplete")
    print(Fore.MAGENTA + "  🎯  7. " + Style.RESET_ALL + "Set Priority")
    print(Fore.BLUE + "  🏷️   8. " + Style.RESET_ALL + "Manage Tags")
    print(Fore.CYAN + "  👋  9. " + Style.RESET_ALL + "Exit")
    print()


def get_menu_choice() -> str:
    """
    Get user's menu choice (Phase II enhanced - includes Set Priority and Manage Tags).

    Prompts the user with "Enter choice [1-9]: " and returns their input.

    Returns:
        str: User's menu choice (not validated - validation happens in main loop)

    Phase II Enhancement:
        - Updated prompt from [1-7] to [1-9] to include Set Priority and Manage Tags
    """
    return input("Enter choice [1-9]: ")


def display_todos(todos: list[dict]) -> None:
    """
    Display all todos in formatted table with colors and emojis.

    Args:
        todos: List of todo dictionaries (already sorted by ID ascending)

    Enhanced Output:
        - Colorful header with emojis
        - Green ✅ for completed todos
        - White ⬜ for incomplete todos
        - Color-coded rows
        - Empty list message in yellow

    Examples:
        Empty list:
            ⚠️  No todos found.

        Populated list:
            📋 YOUR TODO LIST
            ID | Status | Title           | Description
            ---|--------|-----------------|------------------
            1  | ⬜     | Buy groceries   | Milk, eggs, bread
            2  | ✅     | Call dentist    | Schedule checkup
            3  | ⬜     | Write report    |
    """
    # Empty list case
    if not todos:
        print(Fore.YELLOW + "⚠️  No todos found.")
        return

    # List header
    print()
    print(Fore.CYAN + Style.BRIGHT + "📋 YOUR TODO LIST:")
    print()

    # Table header (Phase II enhanced with Priority and Tags columns)
    print(Fore.MAGENTA + Style.BRIGHT + "ID | Priority | Status | Title           | Tags")
    print(Fore.MAGENTA + "---|----------|--------|-----------------|------------------" + Style.RESET_ALL)

    # Data rows
    for todo in todos:
        todo_id = todo["id"]

        # Priority indicator with color (Phase II)
        priority = todo.get("priority", "Medium")  # Default to Medium if missing
        if priority == "High":
            priority_display = Fore.RED + "🔴 H" + Style.RESET_ALL
        elif priority == "Low":
            priority_display = Fore.BLUE + "🔵 L" + Style.RESET_ALL
        else:  # Medium
            priority_display = Fore.YELLOW + "🟡 M" + Style.RESET_ALL

        # Use emoji for status
        if todo["completed"]:
            status = Fore.GREEN + "✅" + Style.RESET_ALL
        else:
            status = Fore.WHITE + "⬜" + Style.RESET_ALL

        title = todo["title"]

        # Tags display (Phase II - User Story 6)
        tags = todo.get("tags", [])
        if tags:
            # Display tags in square brackets with color
            tags_display = " ".join([Fore.CYAN + f"[{tag}]" + Style.RESET_ALL for tag in tags])
        else:
            tags_display = ""

        # Format: ID | Priority | Status | Title | Tags
        # Color completed todos differently
        if todo["completed"]:
            print(f"{Fore.GREEN}{todo_id:<2}{Style.RESET_ALL} | {priority_display:<10} | {status:<6} | {Fore.GREEN}{title:<15}{Style.RESET_ALL} | {tags_display}")
        else:
            print(f"{Fore.CYAN}{todo_id:<2}{Style.RESET_ALL} | {priority_display:<10} | {status:<6} | {title:<15} | {tags_display}")

    print()  # Empty line after list


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


def handle_set_priority() -> None:
    """
    Handle Set Priority operation (Phase II - User Story 5).

    Input Prompts:
        1. "Enter todo ID: "
        2. "Enter priority (High/Medium/Low): "

    Output:
        - Success: "Todo ID N priority updated to {priority}!"
        - Error: Various validation errors from storage layer

    Flow:
        1. Prompt for todo ID
        2. Prompt for new priority
        3. Call storage.update_priority()
        4. Display result message
    """
    from storage import update_priority

    # Prompt for ID
    todo_id = input(Fore.CYAN + "Enter todo ID: " + Style.RESET_ALL)

    # Prompt for priority
    print(Fore.YELLOW + "Priority options: " + Fore.RED + "High" + Fore.YELLOW + " / " +
          Fore.YELLOW + "Medium" + Fore.YELLOW + " / " + Fore.BLUE + "Low" + Style.RESET_ALL)
    new_priority = input(Fore.CYAN + "Enter priority: " + Style.RESET_ALL)

    # Call storage layer
    success, message = update_priority(todo_id, new_priority)

    # Display result with color
    if success:
        print(Fore.GREEN + "✅ " + message + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ " + message + Style.RESET_ALL)


def handle_manage_tags() -> None:
    """
    Handle Manage Tags operation (Phase II - User Story 6).

    Input Prompts:
        1. "Enter todo ID: "
        2. "Add or Remove tags? (A/R): "
        3. "Enter tags (comma-separated): "

    Output:
        - Success: "Tags added to todo ID N!" or "Tags removed from todo ID N!"
        - Error: Various validation errors from storage layer

    Flow:
        1. Prompt for todo ID
        2. Prompt for action (Add/Remove)
        3. Prompt for tags
        4. Call storage.add_tags() or storage.remove_tags()
        5. Display result message
    """
    from storage import add_tags, remove_tags

    # Prompt for ID
    todo_id = input(Fore.CYAN + "Enter todo ID: " + Style.RESET_ALL)

    # Prompt for action
    print(Fore.YELLOW + "Actions: " + Fore.GREEN + "A" + Fore.YELLOW + "dd / " +
          Fore.RED + "R" + Fore.YELLOW + "emove" + Style.RESET_ALL)
    action = input(Fore.CYAN + "Add or Remove tags? (A/R): " + Style.RESET_ALL).strip().upper()

    # Prompt for tags
    print(Fore.YELLOW + "💡 Example: work, urgent, personal" + Style.RESET_ALL)
    tags_input = input(Fore.CYAN + "Enter tags (comma-separated): " + Style.RESET_ALL)

    # Call storage layer based on action
    if action == "A":
        success, message = add_tags(todo_id, tags_input)
    elif action == "R":
        success, message = remove_tags(todo_id, tags_input)
    else:
        print(Fore.RED + "❌ Error: Invalid action. Please enter A or R." + Style.RESET_ALL)
        return

    # Display result with color
    if success:
        print(Fore.GREEN + "✅ " + message + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ " + message + Style.RESET_ALL)
