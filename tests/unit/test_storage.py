"""
Unit tests for storage operations in src/storage.py

Tests add_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo,
and mark_complete functions according to specs/001-cli-todo-app/spec.md
"""
import unittest
import sys
sys.path.insert(0, 'src')

import storage
from storage import add_todo, get_all_todos, get_todo_by_id, mark_complete, mark_incomplete, update_todo, delete_todo


class TestGetTodoById(unittest.TestCase):
    """Test cases for get_todo_by_id function."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_get_existing_todo_by_id(self):
        """Should return todo dict when ID exists."""
        # Add a todo
        add_todo("Buy groceries", "Milk")

        # Get it by ID
        todo = get_todo_by_id(1)

        # Verify
        self.assertIsNotNone(todo)
        self.assertEqual(todo["id"], 1)
        self.assertEqual(todo["title"], "Buy groceries")
        self.assertEqual(todo["description"], "Milk")

    def test_get_non_existent_todo_returns_none(self):
        """Should return None when ID does not exist."""
        result = get_todo_by_id(999)
        self.assertIsNone(result)

    def test_get_todo_by_id_with_invalid_id(self):
        """Should return None for invalid ID (not positive integer)."""
        result = get_todo_by_id("invalid")
        self.assertIsNone(result)


class TestMarkComplete(unittest.TestCase):
    """Test cases for mark_complete function."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_mark_incomplete_todo_as_complete(self):
        """Should set completed=True for incomplete todo."""
        # Add incomplete todo
        add_todo("Buy groceries", "")

        # Mark as complete
        success, message = mark_complete(1)

        # Verify
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as complete!")

        # Check todo is actually complete
        todo = get_todo_by_id(1)
        self.assertTrue(todo["completed"])

    def test_mark_complete_is_idempotent(self):
        """Marking already-complete todo should succeed (idempotent)."""
        # Add and mark complete
        add_todo("Buy groceries", "")
        mark_complete(1)

        # Mark complete again
        success, message = mark_complete(1)

        # Should still succeed
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as complete!")

    def test_mark_complete_invalid_id_returns_error(self):
        """Should return error for invalid ID."""
        success, message = mark_complete("invalid")
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_mark_complete_non_existent_id_returns_error(self):
        """Should return error when ID not found."""
        success, message = mark_complete(999)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")


class TestMarkIncomplete(unittest.TestCase):
    """Test cases for mark_incomplete function."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_mark_complete_todo_as_incomplete(self):
        """Should set completed=False for complete todo."""
        # Add and mark complete
        add_todo("Buy groceries", "")
        mark_complete(1)

        # Mark as incomplete
        success, message = mark_incomplete(1)

        # Verify
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as incomplete!")

        # Check todo is actually incomplete
        todo = get_todo_by_id(1)
        self.assertFalse(todo["completed"])

    def test_mark_incomplete_is_idempotent(self):
        """Marking already-incomplete todo should succeed (idempotent)."""
        # Add incomplete todo
        add_todo("Buy groceries", "")

        # Mark incomplete (already incomplete)
        success, message = mark_incomplete(1)

        # Should still succeed
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as incomplete!")

    def test_mark_incomplete_invalid_id_returns_error(self):
        """Should return error for invalid ID."""
        success, message = mark_incomplete("invalid")
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_mark_incomplete_non_existent_id_returns_error(self):
        """Should return error when ID not found."""
        success, message = mark_incomplete(999)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")


class TestUpdateTodo(unittest.TestCase):
    """Test cases for update_todo function."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_update_title_only(self):
        """Should update title and keep description unchanged."""
        # Add todo
        add_todo("Buy groceries", "Milk, eggs")

        # Update title only
        success, message = update_todo(1, "Buy organic groceries", None)

        # Verify success
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 updated successfully!")

        # Check title updated, description unchanged
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Buy organic groceries")
        self.assertEqual(todo["description"], "Milk, eggs")

    def test_update_description_only(self):
        """Should update description and keep title unchanged."""
        # Add todo
        add_todo("Buy groceries", "Milk, eggs")

        # Update description only
        success, message = update_todo(1, None, "Milk, eggs, bread, cheese")

        # Verify success
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 updated successfully!")

        # Check description updated, title unchanged
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Buy groceries")
        self.assertEqual(todo["description"], "Milk, eggs, bread, cheese")

    def test_update_both_title_and_description(self):
        """Should update both title and description."""
        # Add todo
        add_todo("Buy groceries", "Milk")

        # Update both
        success, message = update_todo(1, "Buy organic food", "Vegetables, fruits")

        # Verify success
        self.assertTrue(success)

        # Check both updated
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Buy organic food")
        self.assertEqual(todo["description"], "Vegetables, fruits")

    def test_update_with_none_keeps_current_values(self):
        """Passing None for title/description should keep current values."""
        # Add todo
        add_todo("Original title", "Original description")

        # Update with both None (keeps current)
        success, message = update_todo(1, None, None)

        # Should still succeed
        self.assertTrue(success)

        # Check values unchanged
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Original title")
        self.assertEqual(todo["description"], "Original description")

    def test_update_invalid_id_returns_error(self):
        """Should return error for invalid ID."""
        success, message = update_todo("invalid", "New title", None)
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_update_non_existent_id_returns_error(self):
        """Should return error when ID not found."""
        success, message = update_todo(999, "New title", None)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_update_empty_title_returns_error(self):
        """Should return error if new title is empty."""
        add_todo("Original", "Description")

        success, message = update_todo(1, "", None)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Title cannot be empty.")

    def test_update_title_too_long_returns_error(self):
        """Should return error if new title exceeds 200 chars."""
        add_todo("Original", "Description")

        long_title = "a" * 201
        success, message = update_todo(1, long_title, None)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Title exceeds 200 character limit.")

    def test_update_description_too_long_returns_error(self):
        """Should return error if new description exceeds 1000 chars."""
        add_todo("Title", "Original description")

        long_desc = "a" * 1001
        success, message = update_todo(1, None, long_desc)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Description exceeds 1000 character limit.")


class TestDeleteTodo(unittest.TestCase):
    """Test cases for delete_todo function."""

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_delete_existing_todo(self):
        """Should remove todo from storage."""
        # Add todos
        add_todo("Task 1", "")
        add_todo("Task 2", "")
        add_todo("Task 3", "")

        # Delete middle one
        success, message = delete_todo(2)

        # Verify success
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 2 deleted successfully!")

        # Verify only 2 remain
        todos = get_all_todos()
        self.assertEqual(len(todos), 2)

    def test_delete_preserves_other_todo_ids(self):
        """Deleting a todo should not affect IDs of remaining todos."""
        # Add 3 todos
        add_todo("Task 1", "")
        add_todo("Task 2", "")
        add_todo("Task 3", "")

        # Delete middle one (ID 2)
        delete_todo(2)

        # Verify IDs 1 and 3 still exist with original IDs
        todo1 = get_todo_by_id(1)
        todo3 = get_todo_by_id(3)

        self.assertIsNotNone(todo1)
        self.assertEqual(todo1["id"], 1)
        self.assertEqual(todo1["title"], "Task 1")

        self.assertIsNotNone(todo3)
        self.assertEqual(todo3["id"], 3)
        self.assertEqual(todo3["title"], "Task 3")

        # Verify ID 2 no longer exists
        todo2 = get_todo_by_id(2)
        self.assertIsNone(todo2)

    def test_delete_invalid_id_returns_error(self):
        """Should return error for invalid ID."""
        success, message = delete_todo("invalid")
        self.assertFalse(success)
        self.assertEqual(message, "Error: ID must be a positive integer.")

    def test_delete_non_existent_id_returns_error(self):
        """Should return error when ID not found."""
        success, message = delete_todo(999)
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_delete_last_remaining_todo(self):
        """Should successfully delete the last todo leaving empty list."""
        # Add one todo
        add_todo("Only task", "")

        # Delete it
        success, message = delete_todo(1)

        # Verify success
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 deleted successfully!")

        # Verify list is empty
        todos = get_all_todos()
        self.assertEqual(len(todos), 0)


if __name__ == "__main__":
    unittest.main()
