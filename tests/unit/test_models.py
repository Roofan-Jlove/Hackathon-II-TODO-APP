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


class TestValidatePriority(unittest.TestCase):
    """Test cases for validate_priority function (Phase II - User Story 5)."""

    def test_valid_priority_high(self):
        """'High' should be accepted and normalized."""
        from models import validate_priority

        valid, normalized, error = validate_priority("High")

        self.assertTrue(valid)
        self.assertEqual(normalized, "High")
        self.assertEqual(error, "")

    def test_valid_priority_medium(self):
        """'Medium' should be accepted and normalized."""
        from models import validate_priority

        valid, normalized, error = validate_priority("Medium")

        self.assertTrue(valid)
        self.assertEqual(normalized, "Medium")
        self.assertEqual(error, "")

    def test_valid_priority_low(self):
        """'Low' should be accepted and normalized."""
        from models import validate_priority

        valid, normalized, error = validate_priority("Low")

        self.assertTrue(valid)
        self.assertEqual(normalized, "Low")
        self.assertEqual(error, "")

    def test_case_insensitive_high(self):
        """'high', 'HIGH', 'HiGh' should all be normalized to 'High'."""
        from models import validate_priority

        for variant in ["high", "HIGH", "HiGh", "hIgH"]:
            valid, normalized, error = validate_priority(variant)
            self.assertTrue(valid, f"'{variant}' should be valid")
            self.assertEqual(normalized, "High", f"'{variant}' should normalize to 'High'")
            self.assertEqual(error, "")

    def test_case_insensitive_medium(self):
        """'medium', 'MEDIUM', 'MeDiUm' should all be normalized to 'Medium'."""
        from models import validate_priority

        for variant in ["medium", "MEDIUM", "MeDiUm"]:
            valid, normalized, error = validate_priority(variant)
            self.assertTrue(valid)
            self.assertEqual(normalized, "Medium")
            self.assertEqual(error, "")

    def test_case_insensitive_low(self):
        """'low', 'LOW', 'LoW' should all be normalized to 'Low'."""
        from models import validate_priority

        for variant in ["low", "LOW", "LoW"]:
            valid, normalized, error = validate_priority(variant)
            self.assertTrue(valid)
            self.assertEqual(normalized, "Low")
            self.assertEqual(error, "")

    def test_invalid_priority_returns_error(self):
        """Invalid priority values should return error."""
        from models import validate_priority

        for invalid in ["urgent", "critical", "normal", "", "123", None]:
            valid, normalized, error = validate_priority(invalid)
            self.assertFalse(valid, f"'{invalid}' should be invalid")
            self.assertIsNone(normalized, f"'{invalid}' should return None")
            self.assertEqual(error, "Error: Priority must be High, Medium, or Low.")

    def test_whitespace_priority_normalized(self):
        """Priority with leading/trailing whitespace should be normalized."""
        from models import validate_priority

        valid, normalized, error = validate_priority("  High  ")

        self.assertTrue(valid)
        self.assertEqual(normalized, "High")
        self.assertEqual(error, "")


class TestValidateTags(unittest.TestCase):
    """Test cases for validate_tags function (Phase II - User Story 6)."""

    def test_valid_single_tag(self):
        """Single tag should be accepted and normalized to lowercase."""
        from models import validate_tags

        valid, normalized, error = validate_tags("work")

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work"])
        self.assertEqual(error, "")

    def test_valid_multiple_tags_comma_separated(self):
        """Multiple comma-separated tags should be parsed and normalized."""
        from models import validate_tags

        valid, normalized, error = validate_tags("work, urgent, important")

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work", "urgent", "important"])
        self.assertEqual(error, "")

    def test_tags_normalized_to_lowercase(self):
        """Tags should be normalized to lowercase for case-insensitive matching."""
        from models import validate_tags

        valid, normalized, error = validate_tags("Work, URGENT, Personal")

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work", "urgent", "personal"])
        self.assertEqual(error, "")

    def test_whitespace_trimmed_from_tags(self):
        """Leading/trailing whitespace should be trimmed from each tag."""
        from models import validate_tags

        valid, normalized, error = validate_tags("  work  ,  urgent  ,  personal  ")

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work", "urgent", "personal"])
        self.assertEqual(error, "")

    def test_empty_string_returns_empty_list(self):
        """Empty string should return empty list (valid - optional field)."""
        from models import validate_tags

        valid, normalized, error = validate_tags("")

        self.assertTrue(valid)
        self.assertEqual(normalized, [])
        self.assertEqual(error, "")

    def test_none_returns_empty_list(self):
        """None should return empty list (valid - optional field)."""
        from models import validate_tags

        valid, normalized, error = validate_tags(None)

        self.assertTrue(valid)
        self.assertEqual(normalized, [])
        self.assertEqual(error, "")

    def test_duplicate_tags_removed(self):
        """Duplicate tags should be removed (case-insensitive)."""
        from models import validate_tags

        valid, normalized, error = validate_tags("work, Work, WORK, urgent")

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work", "urgent"])
        self.assertEqual(error, "")

    def test_tag_too_long_returns_error(self):
        """Tags longer than 20 characters should return error."""
        from models import validate_tags

        long_tag = "a" * 21
        valid, normalized, error = validate_tags(long_tag)

        self.assertFalse(valid)
        self.assertIsNone(normalized)
        self.assertEqual(error, "Error: Each tag must be 1-20 characters.")

    def test_empty_tag_after_split_ignored(self):
        """Empty tags after splitting (e.g., 'work,,urgent') should be ignored."""
        from models import validate_tags

        valid, normalized, error = validate_tags("work,,urgent,  ,personal")

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work", "urgent", "personal"])
        self.assertEqual(error, "")

    def test_list_of_tags_accepted(self):
        """List of tags should be accepted directly."""
        from models import validate_tags

        valid, normalized, error = validate_tags(["Work", "Urgent"])

        self.assertTrue(valid)
        self.assertEqual(normalized, ["work", "urgent"])
        self.assertEqual(error, "")


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


class TestValidateRecurrencePattern(unittest.TestCase):
    """Test cases for validate_recurrence_pattern function (Phase III - User Story 9)."""

    def test_valid_pattern_daily(self):
        """'Daily' should be accepted and normalized."""
        from models import validate_recurrence_pattern
        valid, normalized, error = validate_recurrence_pattern("Daily")
        self.assertTrue(valid)
        self.assertEqual(normalized, "Daily")
        self.assertEqual(error, "")

    def test_valid_pattern_weekly(self):
        """'Weekly' should be accepted and normalized."""
        from models import validate_recurrence_pattern
        valid, normalized, error = validate_recurrence_pattern("Weekly")
        self.assertTrue(valid)
        self.assertEqual(normalized, "Weekly")
        self.assertEqual(error, "")

    def test_valid_pattern_monthly(self):
        """'Monthly' should be accepted and normalized."""
        from models import validate_recurrence_pattern
        valid, normalized, error = validate_recurrence_pattern("Monthly")
        self.assertTrue(valid)
        self.assertEqual(normalized, "Monthly")
        self.assertEqual(error, "")

    def test_pattern_none_returns_none(self):
        """'None' should return None (no recurrence)."""
        from models import validate_recurrence_pattern
        valid, normalized, error = validate_recurrence_pattern("None")
        self.assertTrue(valid)
        self.assertIsNone(normalized)
        self.assertEqual(error, "")

    def test_case_insensitive_patterns(self):
        """Should accept patterns in any case and normalize."""
        from models import validate_recurrence_pattern

        patterns = ["daily", "DAILY", "DaiLy", "weekly", "WEEKLY", "monthly", "MONTHLY"]
        expected = ["Daily", "Daily", "Daily", "Weekly", "Weekly", "Monthly", "Monthly"]

        for pattern, expect in zip(patterns, expected):
            valid, normalized, error = validate_recurrence_pattern(pattern)
            self.assertTrue(valid, f"'{pattern}' should be valid")
            self.assertEqual(normalized, expect)

    def test_invalid_pattern_returns_error(self):
        """Invalid patterns should return error."""
        from models import validate_recurrence_pattern

        for invalid in ["yearly", "hourly", "biweekly", "custom", "123"]:
            valid, normalized, error = validate_recurrence_pattern(invalid)
            self.assertFalse(valid)
            self.assertIsNone(normalized)
            self.assertEqual(error, "Error: Recurrence pattern must be None, Daily, Weekly, or Monthly.")

    def test_empty_string_returns_none(self):
        """Empty string should return None (no recurrence)."""
        from models import validate_recurrence_pattern
        valid, normalized, error = validate_recurrence_pattern("")
        self.assertTrue(valid)
        self.assertIsNone(normalized)
        self.assertEqual(error, "")

    def test_none_input_returns_none(self):
        """None input should return None (no recurrence)."""
        from models import validate_recurrence_pattern
        valid, normalized, error = validate_recurrence_pattern(None)
        self.assertTrue(valid)
        self.assertIsNone(normalized)
        self.assertEqual(error, "")


class TestMigrateTodoToPhase3(unittest.TestCase):
    """Test cases for migrate_todo_to_phase3 function (Phase III - User Story 9)."""

    def test_migrate_phase2_todo_adds_recurrence_fields(self):
        """Should add recurrence fields to Phase II todo."""
        from models import migrate_todo_to_phase3
        from datetime import datetime

        phase2_todo = {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs",
            "completed": False,
            "priority": "Medium",
            "tags": [],
            "created_at": datetime.now()
        }

        migrated = migrate_todo_to_phase3(phase2_todo)

        # Should preserve all Phase I and Phase II fields
        self.assertEqual(migrated["id"], 1)
        self.assertEqual(migrated["title"], "Buy groceries")
        self.assertEqual(migrated["description"], "Milk, eggs")
        self.assertEqual(migrated["completed"], False)
        self.assertEqual(migrated["priority"], "Medium")
        self.assertEqual(migrated["tags"], [])

        # Should add Phase III fields with defaults
        self.assertIsNone(migrated["recurrence_pattern"])
        self.assertEqual(migrated["recurrence_interval"], 1)
        self.assertIsNone(migrated["next_occurrence"])

    def test_migrate_already_migrated_todo_is_idempotent(self):
        """Should not modify todo that already has Phase III fields."""
        from models import migrate_todo_to_phase3
        from datetime import datetime

        already_migrated = {
            "id": 2,
            "title": "Take vitamins",
            "description": "Daily vitamins",
            "completed": False,
            "priority": "High",
            "tags": ["health"],
            "created_at": datetime(2025, 1, 1),
            "recurrence_pattern": "Daily",
            "recurrence_interval": 1,
            "next_occurrence": datetime(2025, 1, 2)
        }

        result = migrate_todo_to_phase3(already_migrated)

        # Should preserve ALL fields unchanged
        self.assertEqual(result["recurrence_pattern"], "Daily")
        self.assertEqual(result["recurrence_interval"], 1)
        self.assertEqual(result["next_occurrence"], datetime(2025, 1, 2))


class TestCreateTodoPhase3(unittest.TestCase):
    """Test cases for create_todo function with Phase III fields (recurrence)."""

    def test_create_todo_with_recurrence(self):
        """Should create todo with recurrence pattern."""
        from models import create_todo

        todo = create_todo(1, "Take vitamins", "Daily vitamins", recurrence_pattern="Daily")

        # Verify Phase III fields
        self.assertEqual(todo["recurrence_pattern"], "Daily")
        self.assertEqual(todo["recurrence_interval"], 1)
        self.assertIsNone(todo["next_occurrence"])

    def test_create_todo_without_recurrence(self):
        """Should create todo without recurrence (default)."""
        from models import create_todo

        todo = create_todo(1, "Buy groceries", "Milk")

        # Verify Phase III fields exist with defaults
        self.assertIsNone(todo["recurrence_pattern"])
        self.assertEqual(todo["recurrence_interval"], 1)
        self.assertIsNone(todo["next_occurrence"])

    def test_create_todo_with_custom_interval(self):
        """Should create todo with custom recurrence interval."""
        from models import create_todo

        todo = create_todo(1, "Weekly meeting", "Team sync", recurrence_pattern="Weekly", recurrence_interval=2)

        self.assertEqual(todo["recurrence_pattern"], "Weekly")
        self.assertEqual(todo["recurrence_interval"], 2)


if __name__ == "__main__":
    unittest.main()
