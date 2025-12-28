"""
Main entry point for the CLI Todo Manager application.

This module provides the main loop that displays the menu,
dispatches user commands, and orchestrates the todo manager
according to the specification in specs/001-cli-todo-app/spec.md
"""

from cli import display_menu, get_menu_choice, handle_add, handle_list, handle_mark_complete, handle_mark_incomplete, handle_update, handle_delete


def main():
    """
    Main application loop.

    Displays menu, gets user choice, and dispatches commands.
    Continues until user selects Exit (choice 7).

    Menu Choices:
        1: Add Todo (handler in User Story 1)
        2: List All Todos (handler in User Story 1)
        3: Update Todo (handler in User Story 3)
        4: Delete Todo (handler in User Story 4)
        5: Mark Todo Complete (handler in User Story 2)
        6: Mark Todo Incomplete (handler in User Story 2)
        7: Exit

    Contract: Implements menu-driven loop pattern per research.md and CLI contract
    """
    while True:
        # Display menu
        display_menu()

        # Get user choice
        choice = get_menu_choice()

        # Handle Exit
        if choice == "7":
            print("Goodbye! All todos will be lost.")
            break

        # Handle invalid choices
        elif choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Error: Invalid choice. Please enter 1-7.")

        # User Story 1: Add and List handlers (MVP)
        elif choice == "1":
            handle_add()
        elif choice == "2":
            handle_list()

        # User Story 2: Mark Completion Status handlers
        elif choice == "5":
            handle_mark_complete()
        elif choice == "6":
            handle_mark_incomplete()

        # User Story 3: Update Todo Content handler
        elif choice == "3":
            handle_update()

        # User Story 4: Delete Todo handler
        elif choice == "4":
            handle_delete()


if __name__ == "__main__":
    main()
