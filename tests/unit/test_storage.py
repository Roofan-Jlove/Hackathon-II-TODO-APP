"""
Unit tests for storage operations in src/storage.py

Tests add_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo,
mark_complete functions, and search/filter functions (Phase II - User Story 7)
according to specs/001-cli-todo-app/spec.md
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


class TestSearchTodos(unittest.TestCase):
    """Test cases for search_todos function (Phase II - User Story 7)."""

    def setUp(self):
        """Reset storage and add test data."""
        storage.todos.clear()
        storage.next_id = 1

        # Add diverse test todos
        add_todo("Buy groceries", "Milk, eggs, bread")
        add_todo("Call dentist", "Schedule checkup appointment")
        add_todo("Write report", "Quarterly sales report")
        add_todo("Buy birthday gift", "For mom's birthday party")

        # Add tags and priorities for comprehensive testing
        from storage import add_tags, update_priority
        add_tags(1, "shopping, urgent")
        add_tags(2, "health, personal")
        add_tags(3, "work, deadline")
        add_tags(4, "shopping, personal")

        update_priority(1, "High")
        update_priority(2, "Medium")
        update_priority(3, "High")
        update_priority(4, "Low")

    def test_search_by_keyword_in_title(self):
        """Should find todos with keyword in title (case-insensitive)."""
        from storage import search_todos
        results = search_todos("buy")

        self.assertEqual(len(results), 2)
        titles = [todo["title"] for todo in results]
        self.assertIn("Buy groceries", titles)
        self.assertIn("Buy birthday gift", titles)

    def test_search_by_keyword_in_description(self):
        """Should find todos with keyword in description (case-insensitive)."""
        from storage import search_todos
        results = search_todos("report")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Write report")

    def test_search_case_insensitive(self):
        """Search should be case-insensitive."""
        from storage import search_todos
        results_lower = search_todos("buy")
        results_upper = search_todos("BUY")
        results_mixed = search_todos("BuY")

        self.assertEqual(len(results_lower), len(results_upper))
        self.assertEqual(len(results_lower), len(results_mixed))
        self.assertEqual(len(results_lower), 2)

    def test_search_partial_match(self):
        """Should find partial matches in title and description."""
        from storage import search_todos
        results = search_todos("birth")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Buy birthday gift")

    def test_search_no_matches(self):
        """Should return empty list when no matches found."""
        from storage import search_todos
        results = search_todos("nonexistent")

        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

    def test_search_empty_keyword_returns_all(self):
        """Empty keyword should return all todos."""
        from storage import search_todos
        results = search_todos("")

        self.assertEqual(len(results), 4)


class TestFilterByStatus(unittest.TestCase):
    """Test cases for filter_by_status function (Phase II - User Story 7)."""

    def setUp(self):
        """Reset storage and add test data."""
        storage.todos.clear()
        storage.next_id = 1

        # Add todos with different statuses
        add_todo("Task 1", "Incomplete")
        add_todo("Task 2", "Complete")
        add_todo("Task 3", "Incomplete")
        add_todo("Task 4", "Complete")

        # Mark some as complete
        from storage import mark_complete
        mark_complete(2)
        mark_complete(4)

    def test_filter_completed_only(self):
        """Should return only completed todos."""
        from storage import filter_by_status
        all_todos = get_all_todos()
        results = filter_by_status(all_todos, True)

        self.assertEqual(len(results), 2)
        for todo in results:
            self.assertTrue(todo["completed"])

    def test_filter_incomplete_only(self):
        """Should return only incomplete todos."""
        from storage import filter_by_status
        all_todos = get_all_todos()
        results = filter_by_status(all_todos, False)

        self.assertEqual(len(results), 2)
        for todo in results:
            self.assertFalse(todo["completed"])

    def test_filter_empty_list(self):
        """Filtering empty list should return empty list."""
        from storage import filter_by_status
        results = filter_by_status([], True)

        self.assertEqual(len(results), 0)


class TestFilterByPriority(unittest.TestCase):
    """Test cases for filter_by_priority function (Phase II - User Story 7)."""

    def setUp(self):
        """Reset storage and add test data."""
        storage.todos.clear()
        storage.next_id = 1

        # Add todos with different priorities
        add_todo("Task 1", "High priority")
        add_todo("Task 2", "Medium priority")
        add_todo("Task 3", "Low priority")
        add_todo("Task 4", "High priority")

        from storage import update_priority
        update_priority(1, "High")
        update_priority(2, "Medium")
        update_priority(3, "Low")
        update_priority(4, "High")

    def test_filter_high_priority(self):
        """Should return only high priority todos."""
        from storage import filter_by_priority
        all_todos = get_all_todos()
        results = filter_by_priority(all_todos, "High")

        self.assertEqual(len(results), 2)
        for todo in results:
            self.assertEqual(todo["priority"], "High")

    def test_filter_medium_priority(self):
        """Should return only medium priority todos."""
        from storage import filter_by_priority
        all_todos = get_all_todos()
        results = filter_by_priority(all_todos, "Medium")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["priority"], "Medium")

    def test_filter_low_priority(self):
        """Should return only low priority todos."""
        from storage import filter_by_priority
        all_todos = get_all_todos()
        results = filter_by_priority(all_todos, "Low")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["priority"], "Low")

    def test_filter_case_insensitive(self):
        """Priority filter should be case-insensitive."""
        from storage import filter_by_priority
        all_todos = get_all_todos()
        results_high = filter_by_priority(all_todos, "high")
        results_HIGH = filter_by_priority(all_todos, "HIGH")

        self.assertEqual(len(results_high), len(results_HIGH))
        self.assertEqual(len(results_high), 2)


class TestFilterByTag(unittest.TestCase):
    """Test cases for filter_by_tag function (Phase II - User Story 7)."""

    def setUp(self):
        """Reset storage and add test data."""
        storage.todos.clear()
        storage.next_id = 1

        # Add todos with different tags
        add_todo("Task 1", "Work task")
        add_todo("Task 2", "Personal task")
        add_todo("Task 3", "Work and urgent")
        add_todo("Task 4", "No tags")

        from storage import add_tags
        add_tags(1, "work, deadline")
        add_tags(2, "personal, health")
        add_tags(3, "work, urgent")
        # Task 4 has no tags

    def test_filter_by_single_tag(self):
        """Should return todos with specified tag."""
        from storage import filter_by_tag
        all_todos = get_all_todos()
        results = filter_by_tag(all_todos, "work")

        self.assertEqual(len(results), 2)
        for todo in results:
            self.assertIn("work", todo["tags"])

    def test_filter_by_tag_case_insensitive(self):
        """Tag filter should be case-insensitive."""
        from storage import filter_by_tag
        all_todos = get_all_todos()
        results_lower = filter_by_tag(all_todos, "work")
        results_upper = filter_by_tag(all_todos, "WORK")

        self.assertEqual(len(results_lower), len(results_upper))
        self.assertEqual(len(results_lower), 2)

    def test_filter_no_matching_tag(self):
        """Should return empty list when no todos have the tag."""
        from storage import filter_by_tag
        all_todos = get_all_todos()
        results = filter_by_tag(all_todos, "nonexistent")

        self.assertEqual(len(results), 0)

    def test_filter_todos_without_tags(self):
        """Should handle todos without tags field."""
        from storage import filter_by_tag
        all_todos = get_all_todos()
        results = filter_by_tag(all_todos, "work")

        # Task 4 has no tags, should not be in results
        self.assertEqual(len(results), 2)


class TestCombinedFilters(unittest.TestCase):
    """Test cases for combined search and filter operations (Phase II - User Story 7)."""

    def setUp(self):
        """Reset storage and add comprehensive test data."""
        storage.todos.clear()
        storage.next_id = 1

        # Add diverse todos
        add_todo("Buy groceries", "Milk, eggs, bread")
        add_todo("Call dentist", "Schedule checkup")
        add_todo("Write work report", "Quarterly sales")
        add_todo("Buy birthday gift", "For mom")

        # Set priorities
        from storage import update_priority, add_tags, mark_complete
        update_priority(1, "High")
        update_priority(2, "Medium")
        update_priority(3, "High")
        update_priority(4, "Low")

        # Add tags
        add_tags(1, "shopping, urgent")
        add_tags(2, "health, personal")
        add_tags(3, "work, deadline")
        add_tags(4, "shopping, personal")

        # Mark some complete
        mark_complete(2)
        mark_complete(3)

    def test_search_then_filter_by_priority(self):
        """Should apply search then filter by priority."""
        from storage import search_todos, filter_by_priority

        # Search for "buy"
        search_results = search_todos("buy")
        self.assertEqual(len(search_results), 2)

        # Filter search results by High priority
        filtered = filter_by_priority(search_results, "High")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Buy groceries")

    def test_search_then_filter_by_status(self):
        """Should apply search then filter by status."""
        from storage import search_todos, filter_by_status

        # Search for all todos (empty keyword)
        search_results = search_todos("")

        # Filter by completed
        filtered = filter_by_status(search_results, True)
        self.assertEqual(len(filtered), 2)

    def test_filter_by_tag_then_priority(self):
        """Should apply tag filter then priority filter."""
        from storage import filter_by_tag, filter_by_priority
        all_todos = get_all_todos()

        # Filter by "shopping" tag
        tag_filtered = filter_by_tag(all_todos, "shopping")
        self.assertEqual(len(tag_filtered), 2)

        # Then filter by High priority
        priority_filtered = filter_by_priority(tag_filtered, "High")
        self.assertEqual(len(priority_filtered), 1)
        self.assertEqual(priority_filtered[0]["title"], "Buy groceries")

    def test_multiple_filters_chain(self):
        """Should chain multiple filters (search + tag + priority + status)."""
        from storage import search_todos, filter_by_tag, filter_by_priority, filter_by_status

        # Start with all todos
        results = get_all_todos()

        # Apply tag filter
        results = filter_by_tag(results, "work")
        self.assertEqual(len(results), 1)

        # Apply priority filter
        results = filter_by_priority(results, "High")
        self.assertEqual(len(results), 1)

        # Apply status filter
        results = filter_by_status(results, True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Write work report")


if __name__ == "__main__":
    unittest.main()
