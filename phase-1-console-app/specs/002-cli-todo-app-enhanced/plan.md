# Implementation Plan: Enhanced CLI Todo Application - Phase II (Intermediate Level)

**Branch**: `002-cli-todo-app-enhanced` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Extends**: Phase I (001-cli-todo-app) - Basic Level COMPLETE ✅
**Input**: Enhanced feature specification from `specs/002-cli-todo-app-enhanced/spec.md`

## Summary

Extend the Phase I CLI Todo Manager with intermediate-level organizational features: task priorities (High/Medium/Low), tags/categories for grouping, comprehensive search and filtering capabilities, and flexible sorting options. Maintains functional programming approach, in-memory storage, and 100% test coverage. Adds 4 new user stories (US5-US8) while preserving all existing functionality. Implements backward-compatible data model migration from Phase I.

## Technical Context

**Language/Version**: Python 3.13+ (unchanged from Phase I)
**Project Manager**: UV (unchanged from Phase I)
**Primary Dependencies**: Python standard library only (unchanged from Phase I)
**Storage**: Enhanced in-memory list of dictionaries with additional fields
**Testing**: unittest with expanded test suite (93 existing + ~50 new tests)
**Performance Goals**:
- Search: <100ms for 1000 todos
- Filter: <50ms for 1000 todos
- Sort: <200ms for 1000 todos
**Migration Strategy**: Backward-compatible field additions with defaults
**Scale/Scope**: Single-user, single-session, up to 1000 todos with rich metadata

## Constitution Check

*GATE: Must pass before implementation. Validates against project constitution.*

### ✅ I. Explicitness Over Implicitness

**Status**: PASS

**Evidence**:
- All new behaviors specified with exact formats (priority: H/M/L, tags: [work] [urgent])
- Default values explicit (priority: "Medium", tags: empty list)
- Search/filter/sort behaviors documented with examples
- No implicit tag processing or priority ordering assumptions

### ✅ II. Separation of Concerns

**Status**: PASS

**Evidence**:
- New validation functions in models.py (validate_priority, validate_tags)
- Storage operations remain in storage.py (filter_todos, sort_todos, search_todos)
- CLI display logic in cli.py (format_with_priority, format_with_tags)
- No cross-layer contamination

### ✅ III. Testability as First-Class Requirement

**Status**: PASS

**Evidence**:
- Each user story (US5-US8) has 3+ acceptance scenarios
- Unit tests for each new function (validate_priority, filter_by_tag, sort_by_priority)
- Integration tests for combined features (filter + sort, search + priority)
- Contract tests for new CLI prompts and output formats

### ✅ IV. Minimal Viable Scope

**Status**: PASS

**Evidence**:
- Only 4 new user stories (priorities, tags, search/filter, sort)
- No advanced features (recurring tasks, due dates) in Phase II
- Simple data structures (priority: string, tags: list of strings)
- No external libraries (regex for search, built-in sort for sorting)

### ✅ V. Error Transparency

**Status**: PASS

**Evidence**:
- Invalid priority error: "Error: Priority must be High, Medium, or Low."
- Tag format error: "Error: Tags must be comma-separated words."
- Search with no results: "No todos found matching 'keyword'."
- Invalid sort option: "Error: Sort option must be 1-4."

---

## Architecture Decisions

### AD-001: Priority Representation

**Decision**: Store priority as string enum ("High", "Medium", "Low") rather than integer (1-3)

**Rationale**:
- **Readability**: String is self-documenting in code and storage
- **Display**: No conversion needed for CLI output
- **Validation**: Simple string comparison vs range checking
- **Extensibility**: Easy to add "Urgent" or "Critical" later without reindexing

**Trade-offs**:
- ❌ Slightly more memory (4-6 bytes vs 1 byte per todo)
- ✅ No magic numbers or lookup tables
- ✅ Case-insensitive matching possible ("high" == "High")

**Alternatives Considered**:
1. Integer (1=Low, 2=Medium, 3=High) - rejected due to magic numbers
2. Enum class - rejected to maintain functional programming approach (no classes)

**Migration Impact**: Add `"priority": "Medium"` to all existing todos (default)

---

### AD-002: Tags Storage Format

**Decision**: Store tags as list of lowercase strings `["work", "urgent"]` rather than comma-separated string

**Rationale**:
- **Search Efficiency**: Direct membership check (`"work" in todo["tags"]`) vs string parsing
- **Multiple Tags**: Natural Python list operations (add, remove, iterate)
- **Case Handling**: Store lowercase, search case-insensitive
- **Validation**: Easy to validate each tag individually

**Trade-offs**:
- ✅ O(n) search for tag (acceptable for <10 tags per todo)
- ✅ Simple display: `", ".join(tags)` → "work, urgent"
- ❌ Slightly more complex input parsing (split on comma)

**Alternatives Considered**:
1. Comma-separated string "work,urgent" - rejected due to search complexity
2. Set of strings - rejected due to JSON serialization issues (future persistence)
3. Dictionary {tag: True} - over-engineering for simple membership check

**Migration Impact**: Add `"tags": []` to all existing todos (empty list default)

---

### AD-003: Created Timestamp for Sorting

**Decision**: Add `created_at` datetime field automatically set on todo creation

**Rationale**:
- **Sort by Date**: Enable "newest first" and "oldest first" sorting
- **Audit Trail**: Useful for understanding task history
- **Future Features**: Foundation for analytics, task aging reports
- **Low Cost**: Minimal memory overhead (8 bytes per todo)

**Trade-offs**:
- ✅ Automatic assignment in `add_todo()` (no user input needed)
- ✅ Immutable after creation (no update logic needed)
- ❌ Requires datetime import (still standard library)

**Alternatives Considered**:
1. Sequential creation counter - rejected due to lack of real-world meaning
2. Manual timestamp entry - rejected due to UX complexity
3. No timestamps - rejected due to inability to sort by creation

**Migration Impact**: Add `"created_at": datetime.now()` to all existing todos during migration

---

### AD-004: Search Implementation Strategy

**Decision**: Case-insensitive substring search in both title and description using Python's `in` operator

**Rationale**:
- **Simplicity**: No regex compilation overhead
- **User Expectations**: "grocery" matches "Buy Groceries" and "grocery shopping"
- **Performance**: O(n*m) acceptable for n=1000 todos, m=avg 50 chars
- **No Dependencies**: Pure Python string operations

**Trade-offs**:
- ✅ Simple implementation: `keyword.lower() in title.lower()`
- ✅ Meets NFR-I-001: <100ms for 1000 todos
- ❌ No advanced features (wildcards, regex, fuzzy matching)

**Alternatives Considered**:
1. Regex search - rejected due to user complexity and error potential
2. Fuzzy matching (Levenshtein distance) - over-engineering for MVP
3. Full-text indexing - over-engineering for in-memory <1000 items

**Implementation**: New function `search_todos(keyword: str) -> list[dict]`

---

### AD-005: Filter Combination Logic

**Decision**: Use AND logic for multiple filters (priority AND tag AND status)

**Rationale**:
- **Narrowing Results**: Users expect filters to narrow, not expand results
- **Predictability**: AND is more intuitive than OR for filtering
- **Performance**: Early termination possible (fail-fast on first non-match)
- **Common Use Case**: "Show me High priority work tasks that are incomplete"

**Trade-offs**:
- ✅ Meets user expectations (standard filter behavior)
- ✅ Simple implementation: chain of `if` conditions
- ❌ OR logic not supported (could be Phase III feature)

**Alternatives Considered**:
1. OR logic - rejected due to result explosion (100 work tasks + 200 incomplete = 300 results)
2. User-selectable AND/OR - deferred to Phase III (adds UI complexity)
3. No combination - rejected due to limited utility

**Implementation**: Single `filter_todos()` function with optional parameters

---

### AD-006: Sort Implementation Strategy

**Decision**: Implement sorting via Python's built-in `sorted()` with custom key functions

**Rationale**:
- **Performance**: Python's Timsort is O(n log n), optimized for partially sorted data
- **Simplicity**: One-liner for each sort type: `sorted(todos, key=lambda t: t["priority_order"])`
- **Stability**: Timsort preserves order for equal elements (good for secondary sorting)
- **No Dependencies**: Built-in Python functionality

**Trade-offs**:
- ✅ Meets NFR-I-003: <200ms for 1000 todos
- ✅ Easy to add new sort options
- ❌ Creates new list (O(n) memory), but acceptable for n=1000

**Priority Sort Order**: Define mapping: `{"High": 1, "Medium": 2, "Low": 3}` for numeric comparison

**Alternatives Considered**:
1. Manual bubble/insertion sort - rejected due to poor performance
2. In-place sorting - rejected due to potential side effects on shared list
3. Database-style ORDER BY - over-engineering for in-memory list

**Implementation**: New function `sort_todos(todos, sort_by: str) -> list[dict]`

---

## Data Model Changes

### Enhanced Todo Structure

```python
# Phase I (Existing)
{
    "id": int,              # Unique identifier
    "title": str,           # Task title (required, max 200)
    "description": str,     # Task details (optional, max 1000)
    "completed": bool,      # Completion status
}

# Phase II (New Fields Added)
{
    "id": int,              # Unchanged
    "title": str,           # Unchanged
    "description": str,     # Unchanged
    "completed": bool,      # Unchanged

    # NEW FIELDS
    "priority": str,        # "High", "Medium", "Low" (default: "Medium")
    "tags": list[str],      # ["work", "urgent"] (default: [])
    "created_at": datetime, # Auto-assigned timestamp (default: datetime.now())
}
```

### Migration Strategy

**Backward Compatibility**: All new fields have defaults, existing code continues to work

**Migration Function**:
```python
def migrate_todo_to_phase2(todo: dict) -> dict:
    """Add Phase II fields to Phase I todo with defaults."""
    if "priority" not in todo:
        todo["priority"] = "Medium"
    if "tags" not in todo:
        todo["tags"] = []
    if "created_at" not in todo:
        todo["created_at"] = datetime.now()
    return todo
```

**Migration Timing**: On application startup, run migration on all existing todos

---

## Module Structure

### models.py (Validation)

**Existing Functions**: (unchanged)
- `validate_title(title: str) -> tuple[bool, str]`
- `validate_description(description: str | None) -> tuple[bool, str]`
- `validate_id(todo_id: any) -> tuple[bool, int | None, str]`
- `create_todo(id, title, description) -> dict`

**New Functions**:
```python
def validate_priority(priority: str | None) -> tuple[bool, str]:
    """Validate priority is High, Medium, or Low (case-insensitive)."""

def validate_tags(tags_input: str) -> tuple[bool, list[str], str]:
    """Parse and validate comma-separated tags, returns (valid, tags_list, error)."""

def create_todo_with_metadata(id, title, description, priority="Medium", tags=None) -> dict:
    """Create todo with Phase II metadata (priority, tags, created_at)."""
```

### storage.py (Data Operations)

**Existing Functions**: (unchanged)
- `add_todo(title, description) -> tuple[bool, int | None, str]`
- `get_all_todos() -> list[dict]`
- `get_todo_by_id(id) -> dict | None`
- `update_todo(id, new_title, new_description) -> tuple[bool, str]`
- `delete_todo(id) -> tuple[bool, str]`
- `mark_complete(id) -> tuple[bool, str]`
- `mark_incomplete(id) -> tuple[bool, str]`

**Enhanced Functions**:
```python
# Update add_todo to include priority and tags
def add_todo(title, description, priority="Medium", tags=None) -> tuple[bool, int | None, str]:
    """Enhanced with priority and tags parameters."""

# Update update_todo to handle priority and tags
def update_todo(id, new_title=None, new_description=None, new_priority=None, new_tags=None) -> tuple[bool, str]:
    """Enhanced with priority and tags update capability."""
```

**New Functions**:
```python
def search_todos(keyword: str) -> list[dict]:
    """Search todos by keyword in title or description."""

def filter_todos(status=None, priority=None, tag=None) -> list[dict]:
    """Filter todos by status, priority, and/or tag (AND logic)."""

def sort_todos(todos: list[dict], sort_by: str) -> list[dict]:
    """Sort todos by: 'alpha', 'priority', 'date', 'status'."""

def set_priority(id, priority: str) -> tuple[bool, str]:
    """Update priority for existing todo."""

def add_tag(id, tag: str) -> tuple[bool, str]:
    """Add tag to existing todo's tag list."""

def remove_tag(id, tag: str) -> tuple[bool, str]:
    """Remove tag from existing todo's tag list."""
```

### cli.py (User Interface)

**Existing Functions**: (unchanged)
- `display_menu() -> None`
- `get_menu_choice() -> str`
- `display_todos(todos) -> None`
- `handle_add() -> None`
- `handle_list() -> None`
- `handle_update() -> None`
- `handle_delete() -> None`
- `handle_mark_complete() -> None`
- `handle_mark_incomplete() -> None`

**Enhanced Functions**:
```python
def display_todos(todos: list[dict]) -> None:
    """Enhanced to show priority and tags in table."""
    # New columns: Priority | Tags
    # Format: H | [work] [urgent]
```

**New Functions**:
```python
def handle_set_priority() -> None:
    """Prompt for ID and new priority, call storage.set_priority()."""

def handle_manage_tags() -> None:
    """Prompt for ID, show current tags, allow add/remove."""

def handle_search() -> None:
    """Prompt for keyword, display matching todos."""

def handle_filter() -> None:
    """Prompt for filter criteria (status/priority/tag), display filtered todos."""

def handle_sort() -> None:
    """Prompt for sort option, display sorted todos."""
```

### main.py (Menu Loop)

**Changes**:
- Expand menu from 7 options to 13 options
- Add handlers for options 6-12 (new features)
- Maintain same loop structure

**New Menu**:
```
1-5: Basic operations (unchanged)
6: Set Priority
7: Manage Tags
8: Search
9: Filter
10: Sort
11-12: Reserved for Advanced features
13: Exit
```

---

## Testing Strategy

### Test Coverage Expansion

**Phase I**: 93 tests (42 unit + 12 integration + 39 contract) ✅

**Phase II Target**: ~143 tests (92 unit + 28 integration + 53 contract)

**New Unit Tests** (~50 tests):
- models.py: validate_priority (5 tests), validate_tags (8 tests)
- storage.py: search_todos (6 tests), filter_todos (10 tests), sort_todos (8 tests), set_priority (5 tests), add_tag (4 tests), remove_tag (4 tests)

**New Integration Tests** (~16 tests):
- US5: Priority scenarios (4 tests)
- US6: Tag scenarios (4 tests)
- US7: Search/filter scenarios (4 tests)
- US8: Sort scenarios (4 tests)

**New Contract Tests** (~14 tests):
- Priority prompts and messages (4 tests)
- Tag prompts and messages (3 tests)
- Search/filter prompts (4 tests)
- Sort prompts (3 tests)

### Performance Testing

**Search Performance Test**:
```python
def test_search_performance_1000_todos():
    # Create 1000 todos
    # Measure search time
    # Assert < 100ms
```

**Filter Performance Test**:
```python
def test_filter_performance_1000_todos():
    # Create 1000 todos with varied metadata
    # Measure filter time
    # Assert < 50ms
```

**Sort Performance Test**:
```python
def test_sort_performance_1000_todos():
    # Create 1000 todos
    # Measure sort time
    # Assert < 200ms
```

---

## Implementation Phases

### Phase 2.0: Data Model Migration (Foundation)
**Dependencies**: None (can start immediately)

- Add priority, tags, created_at fields to todo structure
- Implement migrate_todo_to_phase2() function
- Write migration tests
- Update create_todo() to include new fields
- **Deliverable**: Enhanced data model with backward compatibility

### Phase 2.1: User Story 5 - Priorities
**Dependencies**: Phase 2.0 complete

- Implement validate_priority() in models.py
- Implement set_priority() in storage.py
- Enhance add_todo() to accept priority parameter
- Enhance update_todo() to update priority
- Update display_todos() to show priority column
- Implement handle_set_priority() in cli.py
- Add menu option #6
- **Deliverable**: Full priority support with tests

### Phase 2.2: User Story 6 - Tags
**Dependencies**: Phase 2.0 complete (can run parallel with 2.1)

- Implement validate_tags() in models.py
- Implement add_tag() and remove_tag() in storage.py
- Enhance add_todo() to accept tags parameter
- Update display_todos() to show tags column
- Implement handle_manage_tags() in cli.py
- Add menu option #7
- **Deliverable**: Full tag management with tests

### Phase 2.3: User Story 7 - Search & Filter
**Dependencies**: Phase 2.1 and 2.2 complete (needs priority and tags)

- Implement search_todos() in storage.py
- Implement filter_todos() in storage.py
- Implement handle_search() in cli.py
- Implement handle_filter() in cli.py
- Add menu options #8 and #9
- **Deliverable**: Search and filter capabilities with tests

### Phase 2.4: User Story 8 - Sorting
**Dependencies**: Phase 2.1 complete (needs priority for priority sorting)

- Implement sort_todos() in storage.py
- Implement handle_sort() in cli.py
- Update display logic to show sort order indicator
- Add menu option #10
- **Deliverable**: Multi-criteria sorting with tests

### Phase 2.5: Integration & Polish
**Dependencies**: All previous phases complete

- Run full test suite (target: 143/143 passing)
- Performance testing (search/filter/sort < thresholds)
- Update CLAUDE.md with Phase II instructions
- Update README.md with new features
- Documentation review
- **Deliverable**: Production-ready Phase II

---

## Risk Analysis

### R1: Performance Degradation with 1000 Todos

**Risk**: Search/filter/sort may be slow with large datasets

**Likelihood**: Medium
**Impact**: High (violates NFR-I-001 to NFR-I-003)

**Mitigation**:
- Early performance testing with 1000-item dataset
- Profile search/filter/sort with Python's cProfile
- Optimize hot paths if needed (e.g., cache lowercase titles for search)

**Contingency**: If performance targets missed, reduce capacity limit to 500 todos

---

### R2: Data Model Breaking Changes

**Risk**: Migration function fails or corrupts existing todos

**Likelihood**: Low
**Impact**: Critical (data loss)

**Mitigation**:
- Comprehensive migration tests before touching real data
- Non-destructive migration (adds fields, never removes)
- Validation after migration (check all todos have new fields)

**Contingency**: Rollback capability - keep Phase I code as fallback

---

### R3: Test Suite Maintenance Burden

**Risk**: 143 tests difficult to maintain, slow to run

**Likelihood**: Medium
**Impact**: Medium (slower development velocity)

**Mitigation**:
- Modular test structure (unit/integration/contract separation)
- Fast unit tests (<1ms each)
- Longer integration/performance tests in separate suite

**Contingency**: Implement test parallelization with pytest-xdist (Phase III)

---

## Success Criteria

**SC-P2-001**: All 93 Phase I tests continue to pass (backward compatibility)
**SC-P2-002**: 50+ new tests added with 100% pass rate
**SC-P2-003**: Search completes in <100ms for 1000 todos
**SC-P2-004**: Filter completes in <50ms for 1000 todos
**SC-P2-005**: Sort completes in <200ms for 1000 todos
**SC-P2-006**: Priority display shows H/M/L indicator in list view
**SC-P2-007**: Tags display shows [tag1] [tag2] format in list view
**SC-P2-008**: Search finds todos with keyword in title OR description
**SC-P2-009**: Filters combine with AND logic (all criteria must match)
**SC-P2-010**: Sort maintains stable order for equal elements

---

## Dependencies

**External**: None (Python standard library only)
**Internal**: Phase I (001-cli-todo-app) MUST be complete

---

## Timeline Estimate

**Phase 2.0**: 1-2 hours (data model + migration)
**Phase 2.1**: 2-3 hours (priorities)
**Phase 2.2**: 2-3 hours (tags)
**Phase 2.3**: 3-4 hours (search & filter)
**Phase 2.4**: 2-3 hours (sorting)
**Phase 2.5**: 2-3 hours (integration & polish)

**Total Estimated**: 12-18 hours of development time

---

**Created**: 2025-12-29
**Author**: Claude Code + Human Collaboration
**Status**: Ready for Task Breakdown (tasks.md)
**Next**: Create tasks.md with detailed implementation tasks
