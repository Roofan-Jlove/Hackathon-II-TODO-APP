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
    print(Fore.GREEN + "  🔍  9. " + Style.RESET_ALL + "Search & Filter")
    print(Fore.MAGENTA + "  🔀  10. " + Style.RESET_ALL + "Sort")
    print(Fore.GREEN + "  🔁  11. " + Style.RESET_ALL + "Set Recurrence")
    print(Fore.CYAN + "  👋  12. " + Style.RESET_ALL + "Exit")
    print()


def get_menu_choice() -> str:
    """
    Get user's menu choice (Phase III enhanced - includes Set Recurrence).

    Prompts the user with "Enter choice [1-12]: " and returns their input.

    Returns:
        str: User's menu choice (not validated - validation happens in main loop)

    Phase III Enhancement:
        - Updated prompt from [1-11] to [1-12] to include Set Recurrence
    """
    return input("Enter choice [1-12]: ")


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

    # Table header (Phase III enhanced with Priority, Tags, Recurrence, and Description)
    print(Fore.MAGENTA + Style.BRIGHT + "ID | Pri | Rec | St | Title           | Description        | Tags")
    print(Fore.MAGENTA + "---|-----|-----|----|-----------------|--------------------|------------------" + Style.RESET_ALL)

    # Data rows
    for todo in todos:
        todo_id = todo["id"]

        # Priority indicator with color (Phase II)
        priority = todo.get("priority", "Medium")  # Default to Medium if missing
        if priority == "High":
            priority_display = Fore.RED + "🔴H" + Style.RESET_ALL
        elif priority == "Low":
            priority_display = Fore.BLUE + "🔵L" + Style.RESET_ALL
        else:  # Medium
            priority_display = Fore.YELLOW + "🟡M" + Style.RESET_ALL

        # Recurrence indicator (Phase III - User Story 9)
        recurrence = todo.get("recurrence_pattern")
        if recurrence == "Daily":
            recurrence_display = Fore.GREEN + "🔁D" + Style.RESET_ALL
        elif recurrence == "Weekly":
            recurrence_display = Fore.BLUE + "🔁W" + Style.RESET_ALL
        elif recurrence == "Monthly":
            recurrence_display = Fore.MAGENTA + "🔁M" + Style.RESET_ALL
        else:
            recurrence_display = "   "  # No recurrence

        # Use emoji for status (shortened to fit better)
        if todo["completed"]:
            status = Fore.GREEN + "✅" + Style.RESET_ALL
        else:
            status = Fore.WHITE + "⬜" + Style.RESET_ALL

        title = todo["title"]

        # Description with truncation if needed
        description = todo.get("description", "")
        if len(description) > 18:
            description_display = description[:15] + "..."
        else:
            description_display = description

        # Tags display (Phase II - User Story 6)
        tags = todo.get("tags", [])
        if tags:
            # Display tags in square brackets with color
            tags_display = " ".join([Fore.CYAN + f"[{tag}]" + Style.RESET_ALL for tag in tags])
        else:
            tags_display = ""

        # Format: ID | Pri | Rec | St | Title | Description | Tags
        # Color completed todos differently
        if todo["completed"]:
            print(f"{Fore.GREEN}{todo_id:<2}{Style.RESET_ALL} | {priority_display:<3} | {recurrence_display:<3} | {status:<2} | {Fore.GREEN}{title:<15}{Style.RESET_ALL} | {description_display:<18} | {tags_display}")
        else:
            print(f"{Fore.CYAN}{todo_id:<2}{Style.RESET_ALL} | {priority_display:<3} | {recurrence_display:<3} | {status:<2} | {title:<15} | {description_display:<18} | {tags_display}")

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


def handle_search_filter() -> None:
    """
    Handle Search and Filter operation (Phase II - User Story 7).

    Interactive menu for searching and filtering todos:
        1. Search by keyword (title/description)
        2. Filter by status (complete/incomplete)
        3. Filter by priority (High/Medium/Low)
        4. Filter by tag
        5. Combined filters (chainable)

    Flow:
        1. Display filter options menu
        2. Get user selections
        3. Apply filters in sequence
        4. Display filtered results
    """
    from storage import get_all_todos, search_todos, filter_by_status, filter_by_priority, filter_by_tag

    print()
    print(Fore.CYAN + Style.BRIGHT + "🔍 SEARCH & FILTER" + Style.RESET_ALL)
    print()

    # Start with all todos
    results = get_all_todos()

    # Search by keyword
    print(Fore.YELLOW + "Search by keyword (leave blank to skip): " + Style.RESET_ALL)
    keyword = input(Fore.CYAN + "Enter keyword: " + Style.RESET_ALL).strip()

    if keyword:
        results = search_todos(keyword)
        print(Fore.GREEN + f"✓ Searching for '{keyword}'" + Style.RESET_ALL)

    # Filter by status
    print()
    print(Fore.YELLOW + "Filter by status? (Y/N): " + Style.RESET_ALL, end="")
    filter_status = input().strip().upper()

    if filter_status == "Y":
        print(Fore.YELLOW + "Status options: " + Fore.GREEN + "C" + Fore.YELLOW + "omplete / " +
              Fore.WHITE + "I" + Fore.YELLOW + "ncomplete" + Style.RESET_ALL)
        status_choice = input(Fore.CYAN + "Enter choice (C/I): " + Style.RESET_ALL).strip().upper()

        if status_choice == "C":
            results = filter_by_status(results, True)
            print(Fore.GREEN + "✓ Showing completed todos" + Style.RESET_ALL)
        elif status_choice == "I":
            results = filter_by_status(results, False)
            print(Fore.GREEN + "✓ Showing incomplete todos" + Style.RESET_ALL)

    # Filter by priority
    print()
    print(Fore.YELLOW + "Filter by priority? (Y/N): " + Style.RESET_ALL, end="")
    filter_priority = input().strip().upper()

    if filter_priority == "Y":
        print(Fore.YELLOW + "Priority options: " + Fore.RED + "H" + Fore.YELLOW + "igh / " +
              Fore.YELLOW + "M" + Fore.YELLOW + "edium / " + Fore.BLUE + "L" + Fore.YELLOW + "ow" + Style.RESET_ALL)
        priority_choice = input(Fore.CYAN + "Enter choice (H/M/L): " + Style.RESET_ALL).strip().upper()

        if priority_choice == "H":
            results = filter_by_priority(results, "High")
            print(Fore.GREEN + "✓ Showing High priority todos" + Style.RESET_ALL)
        elif priority_choice == "M":
            results = filter_by_priority(results, "Medium")
            print(Fore.GREEN + "✓ Showing Medium priority todos" + Style.RESET_ALL)
        elif priority_choice == "L":
            results = filter_by_priority(results, "Low")
            print(Fore.GREEN + "✓ Showing Low priority todos" + Style.RESET_ALL)

    # Filter by tag
    print()
    print(Fore.YELLOW + "Filter by tag? (Y/N): " + Style.RESET_ALL, end="")
    filter_tag = input().strip().upper()

    if filter_tag == "Y":
        tag = input(Fore.CYAN + "Enter tag: " + Style.RESET_ALL).strip()
        if tag:
            results = filter_by_tag(results, tag)
            print(Fore.GREEN + f"✓ Showing todos tagged with '{tag}'" + Style.RESET_ALL)

    # Display filtered results
    print()
    print(Fore.CYAN + Style.BRIGHT + f"📊 FILTERED RESULTS ({len(results)} todos):" + Style.RESET_ALL)
    print()
    display_todos(results)


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


def handle_search_filter() -> None:
    """
    Handle Search and Filter operation (Phase II - User Story 7).

    Interactive menu for searching and filtering todos:
        1. Search by keyword (title/description)
        2. Filter by status (complete/incomplete)
        3. Filter by priority (High/Medium/Low)
        4. Filter by tag
        5. Combined filters (chainable)

    Flow:
        1. Display filter options menu
        2. Get user selections
        3. Apply filters in sequence
        4. Display filtered results
    """
    from storage import get_all_todos, search_todos, filter_by_status, filter_by_priority, filter_by_tag

    print()
    print(Fore.CYAN + Style.BRIGHT + "🔍 SEARCH & FILTER" + Style.RESET_ALL)
    print()

    # Start with all todos
    results = get_all_todos()

    # Search by keyword
    print(Fore.YELLOW + "Search by keyword (leave blank to skip): " + Style.RESET_ALL)
    keyword = input(Fore.CYAN + "Enter keyword: " + Style.RESET_ALL).strip()

    if keyword:
        results = search_todos(keyword)
        print(Fore.GREEN + f"✓ Searching for '{keyword}'" + Style.RESET_ALL)

    # Filter by status
    print()
    print(Fore.YELLOW + "Filter by status? (Y/N): " + Style.RESET_ALL, end="")
    filter_status = input().strip().upper()

    if filter_status == "Y":
        print(Fore.YELLOW + "Status options: " + Fore.GREEN + "C" + Fore.YELLOW + "omplete / " +
              Fore.WHITE + "I" + Fore.YELLOW + "ncomplete" + Style.RESET_ALL)
        status_choice = input(Fore.CYAN + "Enter choice (C/I): " + Style.RESET_ALL).strip().upper()

        if status_choice == "C":
            results = filter_by_status(results, True)
            print(Fore.GREEN + "✓ Showing completed todos" + Style.RESET_ALL)
        elif status_choice == "I":
            results = filter_by_status(results, False)
            print(Fore.GREEN + "✓ Showing incomplete todos" + Style.RESET_ALL)

    # Filter by priority
    print()
    print(Fore.YELLOW + "Filter by priority? (Y/N): " + Style.RESET_ALL, end="")
    filter_priority = input().strip().upper()

    if filter_priority == "Y":
        print(Fore.YELLOW + "Priority options: " + Fore.RED + "H" + Fore.YELLOW + "igh / " +
              Fore.YELLOW + "M" + Fore.YELLOW + "edium / " + Fore.BLUE + "L" + Fore.YELLOW + "ow" + Style.RESET_ALL)
        priority_choice = input(Fore.CYAN + "Enter choice (H/M/L): " + Style.RESET_ALL).strip().upper()

        if priority_choice == "H":
            results = filter_by_priority(results, "High")
            print(Fore.GREEN + "✓ Showing High priority todos" + Style.RESET_ALL)
        elif priority_choice == "M":
            results = filter_by_priority(results, "Medium")
            print(Fore.GREEN + "✓ Showing Medium priority todos" + Style.RESET_ALL)
        elif priority_choice == "L":
            results = filter_by_priority(results, "Low")
            print(Fore.GREEN + "✓ Showing Low priority todos" + Style.RESET_ALL)

    # Filter by tag
    print()
    print(Fore.YELLOW + "Filter by tag? (Y/N): " + Style.RESET_ALL, end="")
    filter_tag = input().strip().upper()

    if filter_tag == "Y":
        tag = input(Fore.CYAN + "Enter tag: " + Style.RESET_ALL).strip()
        if tag:
            results = filter_by_tag(results, tag)
            print(Fore.GREEN + f"✓ Showing todos tagged with '{tag}'" + Style.RESET_ALL)

    # Display filtered results
    print()
    print(Fore.CYAN + Style.BRIGHT + f"📊 FILTERED RESULTS ({len(results)} todos):" + Style.RESET_ALL)
    print()
    display_todos(results)


def handle_sort() -> None:
    """
    Handle Sort operation (Phase II - User Story 8).

    Interactive menu for sorting todos:
        1. Sort by title (A-Z or Z-A)
        2. Sort by priority (High→Low or Low→High)
        3. Sort by created date (Newest or Oldest first)
        4. Sort by status (Incomplete or Completed first)

    Flow:
        1. Display sort options menu
        2. Get user selection
        3. Apply selected sort
        4. Display sorted results
    """
    from storage import get_all_todos, sort_by_title, sort_by_priority, sort_by_created_date, sort_by_status

    print()
    print(Fore.CYAN + Style.BRIGHT + "🔀 SORT TODOS" + Style.RESET_ALL)
    print()

    # Get all todos
    todos = get_all_todos()

    # Display sort options
    print(Fore.YELLOW + "Sort by:" + Style.RESET_ALL)
    print(Fore.GREEN + "  1. " + Style.RESET_ALL + "Title (A-Z or Z-A)")
    print(Fore.MAGENTA + "  2. " + Style.RESET_ALL + "Priority (High→Low or Low→High)")
    print(Fore.BLUE + "  3. " + Style.RESET_ALL + "Created Date (Newest or Oldest)")
    print(Fore.WHITE + "  4. " + Style.RESET_ALL + "Status (Incomplete or Completed first)")
    print()

    # Get sort choice
    sort_choice = input(Fore.CYAN + "Enter choice [1-4]: " + Style.RESET_ALL).strip()

    sorted_todos = None

    # Sort by title
    if sort_choice == "1":
        print(Fore.YELLOW + "Order: " + Fore.GREEN + "A" + Fore.YELLOW + "-Z / " +
              Fore.RED + "Z" + Fore.YELLOW + "-A" + Style.RESET_ALL)
        order = input(Fore.CYAN + "Enter choice (A/Z): " + Style.RESET_ALL).strip().upper()

        if order == "A":
            sorted_todos = sort_by_title(todos, ascending=True)
            print(Fore.GREEN + "✓ Sorted alphabetically A-Z" + Style.RESET_ALL)
        elif order == "Z":
            sorted_todos = sort_by_title(todos, ascending=False)
            print(Fore.GREEN + "✓ Sorted alphabetically Z-A" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Invalid choice" + Style.RESET_ALL)
            return

    # Sort by priority
    elif sort_choice == "2":
        print(Fore.YELLOW + "Order: " + Fore.RED + "H" + Fore.YELLOW + "igh→Low / " +
              Fore.BLUE + "L" + Fore.YELLOW + "ow→High" + Style.RESET_ALL)
        order = input(Fore.CYAN + "Enter choice (H/L): " + Style.RESET_ALL).strip().upper()

        if order == "H":
            sorted_todos = sort_by_priority(todos, high_first=True)
            print(Fore.GREEN + "✓ Sorted by priority: High → Medium → Low" + Style.RESET_ALL)
        elif order == "L":
            sorted_todos = sort_by_priority(todos, high_first=False)
            print(Fore.GREEN + "✓ Sorted by priority: Low → Medium → High" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Invalid choice" + Style.RESET_ALL)
            return

    # Sort by created date
    elif sort_choice == "3":
        print(Fore.YELLOW + "Order: " + Fore.GREEN + "N" + Fore.YELLOW + "ewest first / " +
              Fore.BLUE + "O" + Fore.YELLOW + "ldest first" + Style.RESET_ALL)
        order = input(Fore.CYAN + "Enter choice (N/O): " + Style.RESET_ALL).strip().upper()

        if order == "N":
            sorted_todos = sort_by_created_date(todos, newest_first=True)
            print(Fore.GREEN + "✓ Sorted by date: Newest first" + Style.RESET_ALL)
        elif order == "O":
            sorted_todos = sort_by_created_date(todos, newest_first=False)
            print(Fore.GREEN + "✓ Sorted by date: Oldest first" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Invalid choice" + Style.RESET_ALL)
            return

    # Sort by status
    elif sort_choice == "4":
        print(Fore.YELLOW + "Order: " + Fore.WHITE + "I" + Fore.YELLOW + "ncomplete first / " +
              Fore.GREEN + "C" + Fore.YELLOW + "ompleted first" + Style.RESET_ALL)
        order = input(Fore.CYAN + "Enter choice (I/C): " + Style.RESET_ALL).strip().upper()

        if order == "I":
            sorted_todos = sort_by_status(todos, incomplete_first=True)
            print(Fore.GREEN + "✓ Sorted by status: Incomplete first" + Style.RESET_ALL)
        elif order == "C":
            sorted_todos = sort_by_status(todos, incomplete_first=False)
            print(Fore.GREEN + "✓ Sorted by status: Completed first" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Invalid choice" + Style.RESET_ALL)
            return

    else:
        print(Fore.RED + "❌ Invalid choice. Please enter 1-4." + Style.RESET_ALL)
        return

    # Display sorted results
    if sorted_todos is not None:
        print()
        print(Fore.CYAN + Style.BRIGHT + f"📊 SORTED RESULTS ({len(sorted_todos)} todos):" + Style.RESET_ALL)
        print()
        display_todos(sorted_todos)


def handle_set_recurrence() -> None:
    """
    Handle Set Recurrence operation (Phase III - User Story 9).

    Input Prompts:
        1. "Enter todo ID: "
        2. "Enter recurrence pattern (None/Daily/Weekly/Monthly): "
        3. "Enter interval (default 1): " (optional)

    Output:
        - Success: "Todo ID N recurrence set to {pattern}!"
        - Remove: "Todo ID N recurrence removed!"
        - Error: Various validation errors from storage layer

    Flow:
        1. Prompt for todo ID
        2. Prompt for recurrence pattern
        3. Optionally prompt for interval
        4. Call storage.set_recurrence()
        5. Display result message
    """
    from storage import set_recurrence

    # Prompt for ID
    todo_id = input(Fore.CYAN + "Enter todo ID: " + Style.RESET_ALL)

    # Prompt for recurrence pattern
    print(Fore.YELLOW + "Recurrence options: " + Fore.WHITE + "None" + Fore.YELLOW + " / " +
          Fore.GREEN + "Daily" + Fore.YELLOW + " / " + Fore.BLUE + "Weekly" + Fore.YELLOW + " / " +
          Fore.MAGENTA + "Monthly" + Style.RESET_ALL)
    pattern = input(Fore.CYAN + "Enter pattern: " + Style.RESET_ALL)

    # Prompt for interval (optional, default 1)
    interval_input = input(Fore.CYAN + "Enter interval (press Enter for 1): " + Style.RESET_ALL).strip()
    if interval_input:
        try:
            interval = int(interval_input)
        except ValueError:
            print(Fore.RED + "❌ Error: Interval must be a positive integer." + Style.RESET_ALL)
            return
    else:
        interval = 1

    # Call storage layer
    success, message = set_recurrence(todo_id, pattern, interval)

    # Display result with color
    if success:
        print(Fore.GREEN + "✅ " + message + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ " + message + Style.RESET_ALL)
