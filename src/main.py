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

from cli import display_menu, get_menu_choice, handle_add, handle_list, handle_mark_complete, handle_mark_incomplete, handle_update, handle_delete
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def main():
    """
    Main application loop with enhanced colorful output.

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
            print()
            print(Fore.CYAN + "👋 " + Fore.YELLOW + Style.BRIGHT + "Goodbye! Thanks for using TODO APP!" + Style.RESET_ALL)
            print(Fore.YELLOW + "⚠️  Note: All todos will be lost (in-memory only).")
            print()
            break

        # Handle invalid choices
        elif choice not in ["1", "2", "3", "4", "5", "6"]:
            print(Fore.RED + "❌ Error: Invalid choice. Please enter 1-7.")

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
