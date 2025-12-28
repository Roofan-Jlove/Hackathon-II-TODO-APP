"""
Main entry point for the CLI Todo Manager application.

This module provides the main loop that displays the menu,
dispatches user commands, and orchestrates the todo manager
according to the specification in specs/001-cli-todo-app/spec.md
"""

import sys
import os

# Set UTF-8 encoding for Windows console to support emojis
if sys.platform == "win32":
    try:
        # Try to set UTF-8 encoding for console
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from cli import display_menu, get_menu_choice, handle_add, handle_list, handle_mark_complete, handle_mark_incomplete, handle_update, handle_delete, handle_set_priority, handle_manage_tags, handle_search_filter
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def main():
    """
    Main application loop with Phase II enhanced menu.

    Displays menu, gets user choice, and dispatches commands.
    Continues until user selects Exit (choice 10).

    Menu Choices:
        1: Add Todo (handler in User Story 1)
        2: List All Todos (handler in User Story 1)
        3: Update Todo (handler in User Story 3)
        4: Delete Todo (handler in User Story 4)
        5: Mark Todo Complete (handler in User Story 2)
        6: Mark Todo Incomplete (handler in User Story 2)
        7: Set Priority (handler in User Story 5 - Phase II)
        8: Manage Tags (handler in User Story 6 - Phase II)
        9: Search & Filter (handler in User Story 7 - Phase II)
        10: Exit

    Contract: Implements menu-driven loop pattern per research.md and CLI contract
    """
    while True:
        # Display menu
        display_menu()

        # Get user choice
        choice = get_menu_choice()

        # Handle Exit
        if choice == "10":
            print()
            print(Fore.CYAN + "👋 " + Fore.YELLOW + Style.BRIGHT + "Goodbye! Thanks for using TODO APP!" + Style.RESET_ALL)
            print(Fore.YELLOW + "⚠️  Note: All todos will be lost (in-memory only).")
            print()
            break

        # Handle invalid choices
        elif choice not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print(Fore.RED + "❌ Error: Invalid choice. Please enter 1-10.")

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

        # User Story 5: Set Priority handler (Phase II)
        elif choice == "7":
            handle_set_priority()

        # User Story 6: Manage Tags handler (Phase II)
        elif choice == "8":
            handle_manage_tags()

        # User Story 7: Search & Filter handler (Phase II)
        elif choice == "9":
            handle_search_filter()


if __name__ == "__main__":
    main()
