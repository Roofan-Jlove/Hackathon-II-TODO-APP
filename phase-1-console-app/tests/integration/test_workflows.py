"""
Integration tests for complete user workflows.

Tests all user stories (P1-P4) end-to-end with acceptance scenarios
from specs/001-cli-todo-app/spec.md
"""
import unittest
import sys
sys.path.insert(0, 'src')

import storage


class TestUserStory1(unittest.TestCase):
    """
    Integration tests for User Story 1: Create and View Todos.

    Acceptance Scenarios from spec.md (lines 26-30):
    1. Empty list → add todo with title + description → verify creation
    2. 3 existing todos → list view → verify all 3 displayed with status
    3. Add todo with only title (no description) → verify accepted
    """

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_scenario_1_add_todo_with_title_and_description(self):
        """
        Scenario 1: Given empty todo list, When user adds todo with title
        "Buy groceries" and description "Milk, eggs, bread", Then system
        confirms creation and assigns unique ID.
        """
        from storage import add_todo

        # Given: empty todo list (from setUp)
        # When: user adds todo with title "Buy groceries" and description "Milk, eggs, bread"
        success, todo_id, message = add_todo("Buy groceries", "Milk, eggs, bread")

        # Then: system confirms creation and assigns unique ID
        self.assertTrue(success)
        self.assertEqual(todo_id, 1)
        self.assertEqual(message, "Todo added successfully! (ID: 1)")

    def test_scenario_2_list_shows_all_todos_with_status(self):
        """
        Scenario 2: Given 3 existing todos, When user requests list view,
        Then system displays all 3 todos with ID, title, status (incomplete
        by default), formatted clearly.
        """
        from storage import add_todo, get_all_todos

        # Given: 3 existing todos
        add_todo("Task 1", "Description 1")
        add_todo("Task 2", "Description 2")
        add_todo("Task 3", "Description 3")

        # When: user requests list view
        todos = get_all_todos()

        # Then: system displays all 3 todos with ID, title, status (incomplete by default)
        self.assertEqual(len(todos), 3)

        # Verify first todo
        self.assertEqual(todos[0]["id"], 1)
        self.assertEqual(todos[0]["title"], "Task 1")
        self.assertEqual(todos[0]["description"], "Description 1")
        self.assertFalse(todos[0]["completed"])

        # Verify second todo
        self.assertEqual(todos[1]["id"], 2)
        self.assertEqual(todos[1]["title"], "Task 2")
        self.assertEqual(todos[1]["description"], "Description 2")
        self.assertFalse(todos[1]["completed"])

        # Verify third todo
        self.assertEqual(todos[2]["id"], 3)
        self.assertEqual(todos[2]["title"], "Task 3")
        self.assertEqual(todos[2]["description"], "Description 3")
        self.assertFalse(todos[2]["completed"])

    def test_scenario_3_add_todo_with_only_title(self):
        """
        Scenario 3: Given user wants to add todo, When user provides only
        title without description, Then system accepts and stores todo with
        empty description.
        """
        from storage import add_todo, get_todo_by_id

        # Given: user wants to add todo
        # When: user provides only title without description (None)
        success, todo_id, message = add_todo("Call dentist", None)

        # Then: system accepts and stores todo with empty description
        self.assertTrue(success)
        self.assertEqual(todo_id, 1)
        self.assertEqual(message, "Todo added successfully! (ID: 1)")

        # Verify stored with empty description
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Call dentist")
        self.assertEqual(todo["description"], "")  # None converted to empty string
        self.assertFalse(todo["completed"])


class TestUserStory2(unittest.TestCase):
    """Integration tests for User Story 2: Mark Completion Status.

    Acceptance Scenarios from spec.md (lines 50-52):
    1. Given incomplete todo → mark as complete → verify status changes
    2. Given complete todo → mark as incomplete → verify status changes
    3. Given non-existent ID → mark as complete → verify error message
    """

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_scenario_1_mark_incomplete_todo_as_complete(self):
        """
        Scenario 1: Given todo with ID 1 exists with status incomplete,
        When user marks ID 1 as complete, Then status changes to complete
        and listing reflects this.
        """
        from storage import add_todo, mark_complete, get_todo_by_id

        # Given: todo with ID 1 exists with status incomplete
        success, todo_id, msg = add_todo("Buy groceries", "Milk, eggs")
        self.assertTrue(success)
        self.assertEqual(todo_id, 1)

        # Verify initially incomplete
        todo = get_todo_by_id(1)
        self.assertFalse(todo["completed"])

        # When: user marks ID 1 as complete
        success, message = mark_complete(1)
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 marked as complete!")

        # Then: status changes to complete
        todo = get_todo_by_id(1)
        self.assertTrue(todo["completed"])

    def test_scenario_2_mark_complete_todo_as_incomplete(self):
        """
        Scenario 2: Given todo with ID 2 exists with status complete,
        When user marks ID 2 as incomplete, Then status changes to incomplete.
        """
        from storage import add_todo, mark_complete, mark_incomplete, get_todo_by_id

        # Given: todo with ID 2 exists with status complete
        add_todo("Call dentist", "")
        add_todo("Write report", "")
        mark_complete(2)

        # Verify initially complete
        todo = get_todo_by_id(2)
        self.assertTrue(todo["completed"])

        # When: user marks ID 2 as incomplete
        success, message = mark_incomplete(2)
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 2 marked as incomplete!")

        # Then: status changes to incomplete
        todo = get_todo_by_id(2)
        self.assertFalse(todo["completed"])

    def test_scenario_3_mark_non_existent_todo_shows_error(self):
        """
        Scenario 3: Given user attempts to mark non-existent ID 999 as complete,
        Then system displays clear error message indicating ID not found.
        """
        from storage import mark_complete

        # Given: no todos exist (storage is empty from setUp)
        # When: user attempts to mark non-existent ID 999 as complete
        success, message = mark_complete(999)

        # Then: system displays clear error message indicating ID not found
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")


class TestUserStory3(unittest.TestCase):
    """Integration tests for User Story 3: Update Todo Content.

    Acceptance Scenarios from spec.md (lines 66-68):
    1. Update title of existing todo → verify change in listing
    2. Update description of existing todo → verify change in listing
    3. Try to update non-existent ID → verify error message
    """

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_scenario_1_update_todo_title(self):
        """
        Scenario 1: Given todo with ID 1 has title "Buy groceries",
        When user updates ID 1 title to "Buy organic groceries",
        Then listing shows updated title.
        """
        from storage import add_todo, update_todo, get_todo_by_id

        # Given: todo with ID 1 has title "Buy groceries"
        success, todo_id, msg = add_todo("Buy groceries", "Milk, eggs")
        self.assertTrue(success)
        self.assertEqual(todo_id, 1)

        # When: user updates ID 1 title to "Buy organic groceries"
        success, message = update_todo(1, "Buy organic groceries", None)
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 updated successfully!")

        # Then: listing shows updated title
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Buy organic groceries")
        self.assertEqual(todo["description"], "Milk, eggs")  # Description unchanged

    def test_scenario_2_update_todo_description(self):
        """
        Scenario 2: Given todo with ID 1 has description "Milk, eggs",
        When user updates ID 1 description to "Milk, eggs, bread, cheese",
        Then listing shows updated description.
        """
        from storage import add_todo, update_todo, get_todo_by_id

        # Given: todo with ID 1 has description "Milk, eggs"
        add_todo("Buy groceries", "Milk, eggs")

        # When: user updates ID 1 description to "Milk, eggs, bread, cheese"
        success, message = update_todo(1, None, "Milk, eggs, bread, cheese")
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 1 updated successfully!")

        # Then: listing shows updated description
        todo = get_todo_by_id(1)
        self.assertEqual(todo["title"], "Buy groceries")  # Title unchanged
        self.assertEqual(todo["description"], "Milk, eggs, bread, cheese")

    def test_scenario_3_update_non_existent_todo_shows_error(self):
        """
        Scenario 3: Given user attempts to update non-existent ID 999,
        Then system displays clear error message indicating ID not found.
        """
        from storage import update_todo

        # Given: no todos exist (storage is empty from setUp)
        # When: user attempts to update non-existent ID 999
        success, message = update_todo(999, "New title", None)

        # Then: system displays clear error message indicating ID not found
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")


class TestUserStory4(unittest.TestCase):
    """Integration tests for User Story 4: Delete Todos.

    Acceptance Scenarios from spec.md (lines 82-84):
    1. Delete middle todo from 3 → verify only 2 remain with preserved IDs
    2. Try to delete non-existent ID → verify error message
    3. Delete the only remaining todo → verify empty list
    """

    def setUp(self):
        """Reset storage before each test."""
        storage.todos.clear()
        storage.next_id = 1

    def test_scenario_1_delete_middle_todo_preserves_ids(self):
        """
        Scenario 1: Given todos with IDs 1, 2, 3 exist,
        When user deletes ID 2,
        Then only IDs 1 and 3 remain in the list.
        """
        from storage import add_todo, delete_todo, get_all_todos

        # Given: todos with IDs 1, 2, 3 exist
        add_todo("Task 1", "First")
        add_todo("Task 2", "Second")
        add_todo("Task 3", "Third")

        # When: user deletes ID 2
        success, message = delete_todo(2)
        self.assertTrue(success)
        self.assertEqual(message, "Todo ID 2 deleted successfully!")

        # Then: only IDs 1 and 3 remain in the list
        todos = get_all_todos()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0]["id"], 1)
        self.assertEqual(todos[1]["id"], 3)

    def test_scenario_2_delete_non_existent_todo_shows_error(self):
        """
        Scenario 2: Given user attempts to delete non-existent ID 999,
        Then system displays clear error message indicating ID not found.
        """
        from storage import delete_todo

        # Given: no todos exist (storage is empty from setUp)
        # When: user attempts to delete non-existent ID 999
        success, message = delete_todo(999)

        # Then: system displays clear error message indicating ID not found
        self.assertFalse(success)
        self.assertEqual(message, "Error: Todo with ID 999 not found.")

    def test_scenario_3_delete_last_todo_shows_empty_list(self):
        """
        Scenario 3: Given user deletes the only remaining todo,
        When user requests list view,
        Then system indicates list is empty.
        """
        from storage import add_todo, delete_todo, get_all_todos

        # Given: one todo exists
        add_todo("Only task", "Description")

        # When: user deletes the only remaining todo
        success, message = delete_todo(1)
        self.assertTrue(success)

        # Then: system indicates list is empty
        todos = get_all_todos()
        self.assertEqual(len(todos), 0)


if __name__ == "__main__":
    unittest.main()
