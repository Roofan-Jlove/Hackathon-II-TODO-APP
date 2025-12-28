"""
Contract tests for CLI interface compliance.

Verifies exact prompts, error messages, and output formats match
the contract specified in specs/001-cli-todo-app/contracts/cli-interface.md
"""
import unittest
import sys
import io
from unittest.mock import patch
sys.path.insert(0, 'src')

from storage import todos, next_id
import storage
from cli import display_menu, get_menu_choice


class TestMenuContract(unittest.TestCase):
    """Test cases for menu display and choice validation."""

    def test_menu_displays_exact_format(self):
        """Menu must display colorful format with emojis (Phase II enhanced)."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        display_menu()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify enhanced menu text with emojis and colors
        self.assertIn("WELCOME TO TODO APP", output)
        self.assertIn("MAIN MENU", output)
        self.assertIn("Add Todo", output)
        self.assertIn("List All Todos", output)
        self.assertIn("Update Todo", output)
        self.assertIn("Delete Todo", output)
        self.assertIn("Mark Todo Complete", output)
        self.assertIn("Mark Todo Incomplete", output)
        self.assertIn("Exit", output)
        # Verify numbered menu items exist
        for i in range(1, 8):
            self.assertIn(f"{i}.", output)


class TestAddTodoContract(unittest.TestCase):
    """Test cases for Add Todo operation contract compliance."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_add_todo_success_message_format(self):
        """Success message must match exact format: 'Todo added successfully! (ID: N)'"""
        from storage import add_todo

        # Test success message format
        success, todo_id, message = add_todo("Buy groceries", "Milk, eggs")

        # Verify exact message format
        self.assertTrue(success)
        self.assertEqual(message, f"Todo added successfully! (ID: {todo_id})")

    def test_add_todo_prompts_for_title(self):
        """Must prompt with exact text: 'Enter title: '"""
        from cli import handle_add

        # Mock input to capture prompts
        with patch('builtins.input', side_effect=["Buy groceries", "Milk"]) as mock_input:
            handle_add()

            # Verify first prompt is for title
            calls = mock_input.call_args_list
            self.assertEqual(calls[0][0][0], "Enter title: ")

    def test_add_todo_prompts_for_description(self):
        """Must prompt with exact text: 'Enter description (optional, press Enter to skip): '"""
        from cli import handle_add

        # Mock input to capture prompts
        with patch('builtins.input', side_effect=["Buy groceries", "Milk"]) as mock_input:
            handle_add()

            # Verify second prompt is for description
            calls = mock_input.call_args_list
            self.assertEqual(calls[1][0][0], "Enter description (optional, press Enter to skip): ")

    def test_add_todo_empty_title_error(self):
        """Empty title must produce exact error: 'Error: Title cannot be empty.'"""
        from storage import add_todo

        # Test empty title error
        success, todo_id, message = add_todo("", "Description")

        # Verify exact error message
        self.assertFalse(success)
        self.assertIsNone(todo_id)
        self.assertEqual(message, "Error: Title cannot be empty.")

    def test_add_todo_title_too_long_error(self):
        """Title >200 chars must produce exact error: 'Error: Title exceeds 200 character limit.'"""
        from storage import add_todo

        # Test title too long error (201 chars)
        long_title = "a" * 201
        success, todo_id, message = add_todo(long_title, "Description")

        # Verify exact error message
        self.assertFalse(success)
        self.assertIsNone(todo_id)
        self.assertEqual(message, "Error: Title exceeds 200 character limit.")

    def test_add_todo_description_too_long_error(self):
        """Description >1000 chars must produce exact error: 'Error: Description exceeds 1000 character limit.'"""
        from storage import add_todo

        # Test description too long error (1001 chars)
        long_desc = "a" * 1001
        success, todo_id, message = add_todo("Buy groceries", long_desc)

        # Verify exact error message
        self.assertFalse(success)
        self.assertIsNone(todo_id)
        self.assertEqual(message, "Error: Description exceeds 1000 character limit.")

    def test_add_todo_capacity_limit_error(self):
        """Adding 1001st todo must produce exact error: 'Error: Maximum 1000 todos reached.'"""
        from storage import add_todo

        # Add 1000 todos to reach capacity
        for i in range(1000):
            add_todo(f"Task {i+1}", "")

        # Try to add 1001st todo
        success, todo_id, message = add_todo("Overflow task", "")

        # Verify exact error message
        self.assertFalse(success)
        self.assertIsNone(todo_id)
        self.assertEqual(message, "Error: Maximum 1000 todos reached.")


class TestListTodosContract(unittest.TestCase):
    """Test cases for List Todos operation contract compliance."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_list_empty_message(self):
        """Empty list must display exact message: 'No todos found.'"""
        from cli import display_todos

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Display empty list
        display_todos([])

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify exact message
        self.assertIn("No todos found.", output)

    def test_list_table_header_format(self):
        """List must display table header with Priority and Tags columns (Phase II enhanced)."""
        from storage import add_todo, get_all_todos
        from cli import display_todos

        # Add a todo so table is displayed
        add_todo("Task 1", "Description")

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Display todos
        todos = get_all_todos()
        display_todos(todos)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify Phase II header format includes Priority and Tags columns
        self.assertIn("ID | Priority | Status | Title           | Tags", output)
        self.assertIn("---|----------|--------|-----------------|------------------", output)

    def test_list_incomplete_status_indicator(self):
        """Incomplete todos must show status as '⬜' (Phase II enhanced)"""
        from storage import add_todo, get_all_todos
        from cli import display_todos

        # Add incomplete todo
        add_todo("Task 1", "Description")

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Display todos
        todos = get_all_todos()
        display_todos(todos)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify incomplete status indicator (emoji)
        self.assertIn("⬜", output)

    def test_list_complete_status_indicator(self):
        """Complete todos must show status as '✅' (Phase II enhanced)"""
        from storage import add_todo, mark_complete, get_all_todos
        from cli import display_todos

        # Add and mark complete
        add_todo("Task 1", "Description")
        mark_complete(1)

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Display todos
        todos = get_all_todos()
        display_todos(todos)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify complete status indicator (emoji)
        self.assertIn("✅", output)

    def test_list_ordered_by_id_ascending(self):
        """Todos must be displayed ordered by ID ascending."""
        from storage import add_todo, get_all_todos

        # Add todos in random order
        add_todo("Task 3", "")
        add_todo("Task 1", "")
        add_todo("Task 2", "")

        # Get all todos
        todos = get_all_todos()

        # Verify ordered by ID ascending
        self.assertEqual(todos[0]["id"], 1)
        self.assertEqual(todos[1]["id"], 2)
        self.assertEqual(todos[2]["id"], 3)


class TestUpdateTodoContract(unittest.TestCase):
    """Test cases for Update Todo operation contract compliance."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_update_prompts_for_id(self):
        """Must prompt with exact text: 'Enter todo ID: '"""
        from storage import add_todo
        from cli import handle_update

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mock input to capture prompts
        with patch('builtins.input', side_effect=["1", "", ""]) as mock_input:
            with patch('builtins.print'):  # Suppress output
                handle_update()

            # Verify first prompt is for ID
            calls = mock_input.call_args_list
            self.assertEqual(calls[0][0][0], "Enter todo ID: ")

    def test_update_prompts_for_title(self):
        """Must prompt with exact text: 'Enter new title (leave blank to keep current): '"""
        from storage import add_todo
        from cli import handle_update

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mock input to capture prompts
        with patch('builtins.input', side_effect=["1", "New title", ""]) as mock_input:
            with patch('builtins.print'):
                handle_update()

            # Verify second prompt is for title
            calls = mock_input.call_args_list
            self.assertEqual(calls[1][0][0], "Enter new title (leave blank to keep current): ")

    def test_update_prompts_for_description(self):
        """Must prompt with exact text: 'Enter new description (leave blank to keep current): '"""
        from storage import add_todo
        from cli import handle_update

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mock input to capture prompts
        with patch('builtins.input', side_effect=["1", "", "New desc"]) as mock_input:
            with patch('builtins.print'):
                handle_update()

            # Verify third prompt is for description
            calls = mock_input.call_args_list
            self.assertEqual(calls[2][0][0], "Enter new description (leave blank to keep current): ")

    def test_update_success_message_format(self):
        """Success message must match exact format: 'Todo ID N updated successfully!'"""
        from storage import add_todo, update_todo

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Update it
        success, message = update_todo(1, "New title", None)

        # Verify exact message format
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 updated successfully!")

    def test_update_id_not_found_error(self):
        """ID not found must produce exact error: 'Error: Todo with ID N not found.'"""
        from storage import update_todo

        # Try to update non-existent ID
        success, message = update_todo(999, "New title", None)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_update_invalid_id_error(self):
        """Invalid ID must produce exact error: 'Error: ID must be a positive integer.'"""
        from storage import update_todo

        # Try to update with invalid ID
        success, message = update_todo("invalid", "New title", None)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_update_empty_title_error(self):
        """Empty new title must produce exact error: 'Error: Title cannot be empty.'"""
        from storage import add_todo, update_todo

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Try to update with empty title
        success, message = update_todo(1, "", None)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Title cannot be empty.")

    def test_update_title_too_long_error(self):
        """Title >200 chars must produce exact error: 'Error: Title exceeds 200 character limit.'"""
        from storage import add_todo, update_todo

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Try to update with too-long title
        long_title = "a" * 201
        success, message = update_todo(1, long_title, None)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Title exceeds 200 character limit.")

    def test_update_description_too_long_error(self):
        """Description >1000 chars must produce exact error: 'Error: Description exceeds 1000 character limit.'"""
        from storage import add_todo, update_todo

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Try to update with too-long description
        long_desc = "a" * 1001
        success, message = update_todo(1, None, long_desc)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Description exceeds 1000 character limit.")

    def test_update_blank_title_keeps_current(self):
        """Blank title input should keep current title unchanged."""
        from storage import add_todo, update_todo, get_todo_by_id

        # Add a todo first
        add_todo("Original title", "Original desc")

        # Update with None (blank) title
        success, message = update_todo(1, None, "New desc")

        # Verify title unchanged
        self.assertTrue(success)
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Original title")
        self.assertEqual(todo["description"], "New desc")

    def test_update_blank_description_keeps_current(self):
        """Blank description input should keep current description unchanged."""
        from storage import add_todo, update_todo, get_todo_by_id

        # Add a todo first
        add_todo("Original title", "Original desc")

        # Update with None (blank) description
        success, message = update_todo(1, "New title", None)

        # Verify description unchanged
        self.assertTrue(success)
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "New title")
        self.assertEqual(todo["description"], "Original desc")


class TestDeleteTodoContract(unittest.TestCase):
    """Test cases for Delete Todo operation contract compliance."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_delete_prompts_for_id(self):
        """Must prompt with exact text: 'Enter todo ID to delete: '"""
        from storage import add_todo
        from cli import handle_delete

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mock input to capture prompts
        with patch('builtins.input', return_value="1") as mock_input:
            with patch('builtins.print'):
                handle_delete()

            # Verify prompt is correct
            mock_input.assert_called_once_with("Enter todo ID to delete: ")

    def test_delete_success_message_format(self):
        """Success message must match exact format: 'Todo ID N deleted successfully!'"""
        from storage import add_todo, delete_todo

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Delete it
        success, message = delete_todo(1)

        # Verify exact message format
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 deleted successfully!")

    def test_delete_id_not_found_error(self):
        """ID not found must produce exact error: 'Error: Todo with ID N not found.'"""
        from storage import delete_todo

        # Try to delete non-existent ID
        success, message = delete_todo(999)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_delete_invalid_id_error(self):
        """Invalid ID must produce exact error: 'Error: ID must be a positive integer.'"""
        from storage import delete_todo

        # Try to delete with invalid ID
        success, message = delete_todo("invalid")

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_delete_preserves_other_todo_ids(self):
        """Deleting a todo should not affect IDs of remaining todos."""
        from storage import add_todo, delete_todo, get_all_todos

        # Add 3 todos
        add_todo("Task 1", "Desc 1")
        add_todo("Task 2", "Desc 2")
        add_todo("Task 3", "Desc 3")

        # Delete middle one
        delete_todo(2)

        # Verify IDs 1 and 3 still exist with original IDs
        todos = get_all_todos()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0]["id"], 1)
        self.assertEqual(todos[1]["id"], 3)


class TestMarkCompleteContract(unittest.TestCase):
    """Test cases for Mark Complete operation contract compliance."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_mark_complete_prompts_for_id(self):
        """Must prompt with exact text: 'Enter todo ID: '"""
        from storage import add_todo
        from cli import handle_mark_complete

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mock input to capture prompts
        with patch('builtins.input', return_value="1") as mock_input:
            with patch('builtins.print'):
                handle_mark_complete()

            # Verify prompt is correct
            mock_input.assert_called_once_with("Enter todo ID: ")

    def test_mark_complete_success_message_format(self):
        """Success message must match exact format: 'Todo ID N marked as complete!'"""
        from storage import add_todo, mark_complete

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mark it complete
        success, message = mark_complete(1)

        # Verify exact message format
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as complete!")

    def test_mark_complete_id_not_found_error(self):
        """ID not found must produce exact error: 'Error: Todo with ID N not found.'"""
        from storage import mark_complete

        # Try to mark non-existent ID as complete
        success, message = mark_complete(999)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_mark_complete_invalid_id_error(self):
        """Invalid ID must produce exact error: 'Error: ID must be a positive integer.'"""
        from storage import mark_complete

        # Try to mark with invalid ID
        success, message = mark_complete("invalid")

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_mark_complete_is_idempotent(self):
        """Marking already-complete todo as complete should succeed (idempotent)."""
        from storage import add_todo, mark_complete

        # Add a todo and mark it complete
        add_todo("Task 1", "Desc")
        mark_complete(1)

        # Mark it complete again (idempotent)
        success, message = mark_complete(1)

        # Verify still succeeds
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as complete!")


class TestMarkIncompleteContract(unittest.TestCase):
    """Test cases for Mark Incomplete operation contract compliance."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_mark_incomplete_prompts_for_id(self):
        """Must prompt with exact text: 'Enter todo ID: '"""
        from storage import add_todo
        from cli import handle_mark_incomplete

        # Add a todo first
        add_todo("Task 1", "Desc")

        # Mock input to capture prompts
        with patch('builtins.input', return_value="1") as mock_input:
            with patch('builtins.print'):
                handle_mark_incomplete()

            # Verify prompt is correct
            mock_input.assert_called_once_with("Enter todo ID: ")

    def test_mark_incomplete_success_message_format(self):
        """Success message must match exact format: 'Todo ID N marked as incomplete!'"""
        from storage import add_todo, mark_complete, mark_incomplete

        # Add a todo and mark it complete first
        add_todo("Task 1", "Desc")
        mark_complete(1)

        # Mark it incomplete
        success, message = mark_incomplete(1)

        # Verify exact message format
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as incomplete!")

    def test_mark_incomplete_id_not_found_error(self):
        """ID not found must produce exact error: 'Error: Todo with ID N not found.'"""
        from storage import mark_incomplete

        # Try to mark non-existent ID as incomplete
        success, message = mark_incomplete(999)

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_mark_incomplete_invalid_id_error(self):
        """Invalid ID must produce exact error: 'Error: ID must be a positive integer.'"""
        from storage import mark_incomplete

        # Try to mark with invalid ID
        success, message = mark_incomplete("invalid")

        # Verify exact error message
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_mark_incomplete_is_idempotent(self):
        """Marking already-incomplete todo as incomplete should succeed (idempotent)."""
        from storage import add_todo, mark_incomplete

        # Add a todo (starts incomplete)
        add_todo("Task 1", "Desc")

        # Mark it incomplete (idempotent - already incomplete)
        success, message = mark_incomplete(1)

        # Verify still succeeds
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as incomplete!")


class TestExitContract(unittest.TestCase):
    """Test cases for Exit operation contract compliance."""

    pass


if __name__ == "__main__":
    unittest.main()
