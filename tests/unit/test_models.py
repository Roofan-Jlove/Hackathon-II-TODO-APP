"""
Unit tests for data validation functions in src/models.py

Tests validate_title, validate_description, validate_id, and create_todo
functions according to validation rules in specs/001-cli-todo-app/data-model.md
"""
import unittest
import sys
sys.path.insert(0, 'src')

from models import validate_id, validate_title, validate_description


class TestValidateTitle(unittest.TestCase):
    """
    Test cases for validate_title function.

    Validation Rules (data-model.md lines 79-81):
    - if title is None or title == "": Reject with "Error: Title cannot be empty."
    - if len(title) > 200: Reject with "Error: Title exceeds 200 character limit."
    """

    def test_valid_title(self):
        """Valid titles (1-200 chars) should pass validation."""
        valid, error = validate_title("Buy groceries")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_empty_title_returns_error(self):
        """Empty string title must return exact error message."""
        valid, error = validate_title("")
        self.assertFalse(valid)
        self.assertEqual(error, "Error: Title cannot be empty.")

    def test_none_title_returns_error(self):
        """None title must return exact error message."""
        valid, error = validate_title(None)
        self.assertFalse(valid)
        self.assertEqual(error, "Error: Title cannot be empty.")

    def test_whitespace_only_title_should_fail(self):
        """Title with only whitespace should be treated as empty."""
        valid, error = validate_title("   ")
        self.assertFalse(valid)
        self.assertEqual(error, "Error: Title cannot be empty.")

    def test_title_exactly_200_chars_passes(self):
        """Title with exactly 200 characters should pass."""
        title_200 = "a" * 200
        valid, error = validate_title(title_200)
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_title_201_chars_returns_error(self):
        """Title with 201 characters must return exact error message."""
        title_201 = "a" * 201
        valid, error = validate_title(title_201)
        self.assertFalse(valid)
        self.assertEqual(error, "Error: Title exceeds 200 character limit.")


class TestValidateDescription(unittest.TestCase):
    """
    Test cases for validate_description function.

    Validation Rules (data-model.md lines 83-85):
    - if description is None: Convert to empty string ""
    - if len(description) > 1000: Reject with "Error: Description exceeds 1000 character limit."
    """

    def test_valid_description(self):
        """Valid descriptions (0-1000 chars) should pass validation."""
        valid, error = validate_description("Milk, eggs, bread")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_none_description_converts_to_empty_string(self):
        """None description should convert to empty string."""
        valid, error = validate_description(None)
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_empty_description_is_valid(self):
        """Empty string description is valid (optional field)."""
        valid, error = validate_description("")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_description_exactly_1000_chars_passes(self):
        """Description with exactly 1000 characters should pass."""
        desc_1000 = "a" * 1000
        valid, error = validate_description(desc_1000)
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_description_1001_chars_returns_error(self):
        """Description with 1001 characters must return exact error message."""
        desc_1001 = "a" * 1001
        valid, error = validate_description(desc_1001)
        self.assertFalse(valid)
        self.assertEqual(error, "Error: Description exceeds 1000 character limit.")


class TestValidateId(unittest.TestCase):
    """Test cases for validate_id function (already implemented in Phase 2)."""

    def test_valid_positive_integer_string(self):
        """String containing positive integer should be parsed correctly."""
        valid, parsed_id, error = validate_id("5")
        self.assertTrue(valid)
        self.assertEqual(parsed_id, 5)
        self.assertEqual(error, "")

    def test_valid_positive_integer(self):
        """Positive integer should pass validation."""
        valid, parsed_id, error = validate_id(10)
        self.assertTrue(valid)
        self.assertEqual(parsed_id, 10)
        self.assertEqual(error, "")

    def test_zero_returns_error(self):
        """Zero should fail validation with correct error message."""
        valid, parsed_id, error = validate_id("0")
        self.assertFalse(valid)
        self.assertIsNone(parsed_id)
        self.assertEqual(error, "Error: ID must be a positive integer.")

    def test_negative_returns_error(self):
        """Negative number should fail validation with correct error message."""
        valid, parsed_id, error = validate_id("-5")
        self.assertFalse(valid)
        self.assertIsNone(parsed_id)
        self.assertEqual(error, "Error: ID must be a positive integer.")

    def test_non_numeric_returns_error(self):
        """Non-numeric string should fail validation with correct error message."""
        valid, parsed_id, error = validate_id("abc")
        self.assertFalse(valid)
        self.assertIsNone(parsed_id)
        self.assertEqual(error, "Error: ID must be a positive integer.")

    def test_float_returns_error(self):
        """Float should fail validation (not a positive integer)."""
        valid, parsed_id, error = validate_id("1.5")
        self.assertFalse(valid)
        self.assertIsNone(parsed_id)
        self.assertEqual(error, "Error: ID must be a positive integer.")


class TestMigrateTodoToPhase2(unittest.TestCase):
    """Test cases for migrate_todo_to_phase2 function (data migration)."""

    def test_migrate_phase1_todo_adds_all_phase2_fields(self):
        """Should add priority, tags, and created_at to Phase I todo."""
        from models import migrate_todo_to_phase2
        from datetime import datetime

        # Phase I todo (no Phase II fields)
        phase1_todo = {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs",
            "completed": False
        }

        before_migration = datetime.now()
        migrated = migrate_todo_to_phase2(phase1_todo)
        after_migration = datetime.now()

        # Should preserve Phase I fields
        self.assertEqual(migrated["id"], 1)
        self.assertEqual(migrated["title"], "Buy groceries")
        self.assertEqual(migrated["description"], "Milk, eggs")
        self.assertEqual(migrated["completed"], False)

        # Should add Phase II fields with defaults
        self.assertEqual(migrated["priority"], "Medium")
        self.assertEqual(migrated["tags"], [])
        self.assertIn("created_at", migrated)
        self.assertGreaterEqual(migrated["created_at"], before_migration)
        self.assertLessEqual(migrated["created_at"], after_migration)

    def test_migrate_already_migrated_todo_is_idempotent(self):
        """Should not modify todo that already has Phase II fields."""
        from models import migrate_todo_to_phase2
        from datetime import datetime

        # Already migrated todo
        already_migrated = {
            "id": 2,
            "title": "Fix bug",
            "description": "Auth error",
            "completed": True,
            "priority": "High",
            "tags": ["work", "urgent"],
            "created_at": datetime(2025, 1, 1, 12, 0, 0)
        }

        result = migrate_todo_to_phase2(already_migrated)

        # Should preserve ALL fields unchanged
        self.assertEqual(result["id"], 2)
        self.assertEqual(result["title"], "Fix bug")
        self.assertEqual(result["description"], "Auth error")
        self.assertEqual(result["completed"], True)
        self.assertEqual(result["priority"], "High")
        self.assertEqual(result["tags"], ["work", "urgent"])
        self.assertEqual(result["created_at"], datetime(2025, 1, 1, 12, 0, 0))

    def test_migrate_preserves_completion_status(self):
        """Should preserve completed=True from Phase I todos."""
        from models import migrate_todo_to_phase2

        completed_todo = {
            "id": 3,
            "title": "Completed task",
            "description": "Done",
            "completed": True
        }

        migrated = migrate_todo_to_phase2(completed_todo)

        # Should preserve completed status
        self.assertEqual(migrated["completed"], True)
        # Should add Phase II fields
        self.assertEqual(migrated["priority"], "Medium")
        self.assertEqual(migrated["tags"], [])
        self.assertIn("created_at", migrated)


class TestCreateTodoPhase2(unittest.TestCase):
    """Test cases for create_todo function with Phase II fields (priority, tags, created_at)."""

    def test_create_todo_with_default_priority(self):
        """Should create todo with default priority 'Medium' when not specified."""
        from models import create_todo

        todo = create_todo(1, "Buy groceries", "Milk, eggs")

        # Verify Phase II fields exist with defaults
        self.assertEqual(todo["priority"], "Medium")
        self.assertEqual(todo["tags"], [])
        self.assertIn("created_at", todo)

    def test_create_todo_with_custom_priority(self):
        """Should create todo with specified priority."""
        from models import create_todo

        todo = create_todo(1, "Buy groceries", "Milk", priority="High")

        self.assertEqual(todo["priority"], "High")

    def test_create_todo_with_tags(self):
        """Should create todo with specified tags list."""
        from models import create_todo

        todo = create_todo(1, "Buy groceries", "Milk", tags=["work", "urgent"])

        self.assertEqual(todo["tags"], ["work", "urgent"])

    def test_create_todo_with_all_phase2_fields(self):
        """Should create todo with all Phase II fields specified."""
        from models import create_todo
        from datetime import datetime

        before_creation = datetime.now()
        todo = create_todo(1, "Buy groceries", "Milk", priority="Low", tags=["personal"])
        after_creation = datetime.now()

        # Verify all fields
        self.assertEqual(todo["id"], 1)
        self.assertEqual(todo["title"], "Buy groceries")
        self.assertEqual(todo["description"], "Milk")
        self.assertEqual(todo["completed"], False)
        self.assertEqual(todo["priority"], "Low")
        self.assertEqual(todo["tags"], ["personal"])

        # Verify created_at is between before and after
        self.assertGreaterEqual(todo["created_at"], before_creation)
        self.assertLessEqual(todo["created_at"], after_creation)

    def test_create_todo_backward_compatible(self):
        """Should work with Phase I signature (no priority/tags parameters)."""
        from models import create_todo

        # Call without Phase II parameters (backward compatibility)
        todo = create_todo(1, "Buy groceries", "Milk")

        # Should still create with defaults
        self.assertEqual(todo["priority"], "Medium")
        self.assertEqual(todo["tags"], [])
        self.assertIn("created_at", todo)


if __name__ == "__main__":
    unittest.main()
