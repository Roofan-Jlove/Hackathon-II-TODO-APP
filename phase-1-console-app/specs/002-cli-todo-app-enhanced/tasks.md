# Tasks: Enhanced CLI Todo Application - Phase II (Intermediate Level)

**Input**: Design documents from `/specs/002-cli-todo-app-enhanced/`
**Prerequisites**: plan.md (required), spec.md (required), Phase I complete (001-cli-todo-app)
**Extends**: Phase I - All basic functionality MUST remain working

**Tests**: Tests are INCLUDED per constitution's non-negotiable testability requirement (Principle III)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each intermediate feature.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US5=Priority, US6=Tags, US7=Search/Filter, US8=Sort)
- Include exact file paths in descriptions
- Task IDs continue from Phase I (starting at T100+)

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (same as Phase I)
- Paths assume single project structure per plan.md

---

## Phase 2.0: Data Model Migration (Foundation for Intermediate Features)

**Purpose**: Extend Phase I data model with priority, tags, and timestamps while maintaining backward compatibility

**⚠️ CRITICAL**: This phase MUST be complete before ANY Phase II user story work begins

**Dependencies**: Phase I complete (all 93 tests passing)

- [ ] T100 Add priority field to todo dict in src/models.py create_todo() (default: "Medium")
- [ ] T101 Add tags field to todo dict in src/models.py create_todo() (default: empty list [])
- [ ] T102 Add created_at field to todo dict in src/models.py create_todo() (default: datetime.now())
- [ ] T103 [P] Write unit test for create_todo with new fields in tests/unit/test_models.py
- [ ] T104 [P] Implement migrate_todo_to_phase2() function in src/storage.py (adds new fields to existing todos)
- [ ] T105 [P] Write unit test for migrate_todo_to_phase2 in tests/unit/test_storage.py (verify backward compatibility)
- [ ] T106 Add migration call at application startup in src/main.py (before menu loop)
- [ ] T107 Verify all 93 Phase I tests still pass after migration (backward compatibility checkpoint)

**Checkpoint**: Enhanced data model ready - Phase II user stories can now begin

---

## Phase 2.1: User Story 5 - Task Priorities (Priority: P5)

**Goal**: Enable users to assign and update priority levels (High/Medium/Low) for task organization

**Independent Test**: Create 3 todos with different priorities (High, Medium, Low), list todos to verify priorities are displayed, update a priority, filter by High priority

**Dependencies**: Phase 2.0 complete

### Tests for User Story 5 (Write FIRST, ensure they FAIL before implementation)

- [ ] T110 [P] [US5] Unit test for validate_priority in tests/unit/test_models.py (test: "High", "Medium", "Low", case-insensitive, invalid values)
- [ ] T111 [P] [US5] Unit test for set_priority in tests/unit/test_storage.py (test: valid priority update, invalid ID, invalid priority)
- [ ] T112 [P] [US5] Integration test for US5 scenario 1 in tests/integration/test_workflows.py (add todo with High priority, verify in list)
- [ ] T113 [P] [US5] Integration test for US5 scenario 2 in tests/integration/test_workflows.py (update priority from Medium to High)
- [ ] T114 [P] [US5] Integration test for US5 scenario 3 in tests/integration/test_workflows.py (list todos, verify priority indicators)
- [ ] T115 [P] [US5] Contract test for priority prompts in tests/contract/test_cli_interface.py (verify exact prompts and success messages)

### Implementation for User Story 5

- [ ] T116 [P] [US5] Implement validate_priority() in src/models.py (return tuple: bool, error_message, accepts High/Medium/Low case-insensitive)
- [ ] T117 [US5] Implement set_priority() in src/storage.py (validate ID, validate priority, update todo, return success)
- [ ] T118 [US5] Update add_todo() in src/storage.py to accept optional priority parameter (default: "Medium")
- [ ] T119 [US5] Update update_todo() in src/storage.py to accept optional new_priority parameter
- [ ] T120 [US5] Update display_todos() in src/cli.py to show Priority column (format: H | M | L)
- [ ] T121 [US5] Implement handle_set_priority() in src/cli.py (prompt for ID, prompt for priority, call storage, display result)
- [ ] T122 [US5] Update handle_add() in src/cli.py to optionally prompt for priority during todo creation
- [ ] T123 [US5] Wire up menu choice #6 (Set Priority) in src/main.py main loop
- [ ] T124 [US5] Run all tests for User Story 5 - verify 100% pass

**Checkpoint**: Priority feature complete - users can assign and update task priorities

---

## Phase 2.2: User Story 6 - Tags and Categories (Priority: P6)

**Goal**: Enable users to organize tasks with tags/categories for grouping related items

**Independent Test**: Create todos with different tags (work, personal), add multiple tags to one todo, list todos to verify tags are displayed, filter by tag

**Dependencies**: Phase 2.0 complete (can run in parallel with Phase 2.1)

### Tests for User Story 6 (Write FIRST)

- [ ] T130 [P] [US6] Unit test for validate_tags in tests/unit/test_models.py (test: comma-separated parsing, empty tags, whitespace handling, case normalization)
- [ ] T131 [P] [US6] Unit test for add_tag in tests/unit/test_storage.py (test: add to empty list, add duplicate, invalid ID)
- [ ] T132 [P] [US6] Unit test for remove_tag in tests/unit/test_storage.py (test: remove existing, remove non-existent, invalid ID)
- [ ] T133 [P] [US6] Integration test for US6 scenario 1 in tests/integration/test_workflows.py (add todo with multiple tags "work, urgent")
- [ ] T134 [P] [US6] Integration test for US6 scenario 2 in tests/integration/test_workflows.py (add tag to existing todo)
- [ ] T135 [P] [US6] Integration test for US6 scenario 3 in tests/integration/test_workflows.py (filter by tag, verify only matching todos)
- [ ] T136 [P] [US6] Contract test for tag prompts in tests/contract/test_cli_interface.py (verify tag format, display format [tag1] [tag2])

### Implementation for User Story 6

- [ ] T137 [P] [US6] Implement validate_tags() in src/models.py (parse comma-separated string, return tuple: bool, list[str], error_message)
- [ ] T138 [US6] Implement add_tag() in src/storage.py (validate ID, append tag to list if not duplicate, return success)
- [ ] T139 [US6] Implement remove_tag() in src/storage.py (validate ID, remove tag if exists, return success)
- [ ] T140 [US6] Update add_todo() in src/storage.py to accept optional tags parameter
- [ ] T141 [US6] Update display_todos() in src/cli.py to show Tags column (format: [work] [urgent])
- [ ] T142 [US6] Implement handle_manage_tags() in src/cli.py (prompt for ID, show current tags, allow add/remove)
- [ ] T143 [US6] Update handle_add() in src/cli.py to optionally prompt for tags during creation
- [ ] T144 [US6] Wire up menu choice #7 (Manage Tags) in src/main.py main loop
- [ ] T145 [US6] Run all tests for User Story 6 - verify 100% pass

**Checkpoint**: Tags feature complete - users can organize tasks with categories

---

## Phase 2.3: User Story 7 - Search and Filter (Priority: P7)

**Goal**: Enable users to find specific tasks quickly using keyword search and multi-criteria filtering

**Independent Test**: Create 10 todos with varied content, search for keyword, filter by status, filter by priority+tag combination, verify correct results

**Dependencies**: Phase 2.0, 2.1 (priority), and 2.2 (tags) complete

### Tests for User Story 7 (Write FIRST)

- [ ] T150 [P] [US7] Unit test for search_todos in tests/unit/test_storage.py (test: case-insensitive, search title, search description, no matches)
- [ ] T151 [P] [US7] Unit test for filter_todos in tests/unit/test_storage.py (test: filter by status, by priority, by tag, combined filters AND logic)
- [ ] T152 [P] [US7] Integration test for US7 scenario 1 in tests/integration/test_workflows.py (search by keyword in title)
- [ ] T153 [P] [US7] Integration test for US7 scenario 2 in tests/integration/test_workflows.py (filter by incomplete status)
- [ ] T154 [P] [US7] Integration test for US7 scenario 3 in tests/integration/test_workflows.py (combined filter: High priority AND work tag)
- [ ] T155 [P] [US7] Contract test for search/filter prompts in tests/contract/test_cli_interface.py (verify prompts, no results message)
- [ ] T156 [P] [US7] Performance test for search in tests/unit/test_storage.py (1000 todos, assert <100ms)
- [ ] T157 [P] [US7] Performance test for filter in tests/unit/test_storage.py (1000 todos, assert <50ms)

### Implementation for User Story 7

- [ ] T158 [P] [US7] Implement search_todos() in src/storage.py (case-insensitive substring search in title and description)
- [ ] T159 [P] [US7] Implement filter_todos() in src/storage.py (accept optional status, priority, tag; AND logic for multiple filters)
- [ ] T160 [US7] Implement handle_search() in src/cli.py (prompt for keyword, call search_todos, display results or "No todos found")
- [ ] T161 [US7] Implement handle_filter() in src/cli.py (prompt for filter criteria, call filter_todos, display results)
- [ ] T162 [US7] Wire up menu choice #8 (Search) in src/main.py main loop
- [ ] T163 [US7] Wire up menu choice #9 (Filter) in src/main.py main loop
- [ ] T164 [US7] Run all tests for User Story 7 - verify 100% pass including performance tests

**Checkpoint**: Search and filter complete - users can find tasks quickly

---

## Phase 2.4: User Story 8 - Sort Tasks (Priority: P8)

**Goal**: Enable users to reorder task list by different criteria (alphabetically, by priority, by date, by status)

**Independent Test**: Create 5 todos with different priorities, creation times, and titles; test each sort option, verify correct order

**Dependencies**: Phase 2.0 and 2.1 (priority) complete

### Tests for User Story 8 (Write FIRST)

- [ ] T170 [P] [US8] Unit test for sort_todos in tests/unit/test_storage.py (test: sort alphabetically A-Z)
- [ ] T171 [P] [US8] Unit test for sort_todos priority in tests/unit/test_storage.py (test: sort High > Medium > Low)
- [ ] T172 [P] [US8] Unit test for sort_todos date in tests/unit/test_storage.py (test: sort by created_at newest/oldest)
- [ ] T173 [P] [US8] Unit test for sort_todos status in tests/unit/test_storage.py (test: incomplete first, then complete)
- [ ] T174 [P] [US8] Integration test for US8 scenario 1 in tests/integration/test_workflows.py (sort alphabetically, verify A-Z order)
- [ ] T175 [P] [US8] Integration test for US8 scenario 2 in tests/integration/test_workflows.py (sort by priority, verify H-M-L order)
- [ ] T176 [P] [US8] Integration test for US8 scenario 3 in tests/integration/test_workflows.py (sort by creation date, verify newest-first)
- [ ] T177 [P] [US8] Contract test for sort prompts in tests/contract/test_cli_interface.py (verify sort menu, invalid option error)
- [ ] T178 [P] [US8] Performance test for sort in tests/unit/test_storage.py (1000 todos, assert <200ms)

### Implementation for User Story 8

- [ ] T179 [P] [US8] Implement sort_todos() in src/storage.py (accept sort_by parameter: "alpha", "priority", "date", "status")
- [ ] T180 [P] [US8] Create priority order mapping in src/storage.py ({"High": 1, "Medium": 2, "Low": 3} for numeric sort)
- [ ] T181 [US8] Implement handle_sort() in src/cli.py (display sort options menu, get choice, call sort_todos, display sorted list)
- [ ] T182 [US8] Wire up menu choice #10 (Sort Tasks) in src/main.py main loop
- [ ] T183 [US8] Run all tests for User Story 8 - verify 100% pass including performance tests

**Checkpoint**: Sort feature complete - users can reorder tasks by multiple criteria

---

## Phase 2.5: Integration, Testing & Polish

**Purpose**: Ensure all Phase II features work together, pass all tests, meet performance requirements

**Dependencies**: Phases 2.1, 2.2, 2.3, and 2.4 complete

- [ ] T190 Run complete Phase I test suite (93 tests) - verify 100% still pass (backward compatibility)
- [ ] T191 Run complete Phase II test suite (new ~50 tests) - verify 100% pass
- [ ] T192 Run full test suite (Phase I + Phase II = ~143 tests) - verify 100% pass
- [ ] T193 [P] Performance validation: Run all performance tests (search/filter/sort with 1000 todos)
- [ ] T194 [P] Create test report showing test counts per category (unit/integration/contract)
- [ ] T195 Update CLAUDE.md with Phase II features and instructions
- [ ] T196 Update README.md with Phase II feature descriptions and examples
- [ ] T197 [P] Add examples to QUICKSTART.md showing priority, tags, search, filter, sort usage
- [ ] T198 Verify menu structure matches spec (13 options, clear categorization)
- [ ] T199 Manual smoke test: Run app, test all 13 menu options, verify no crashes
- [ ] T200 Final code review: Check all docstrings updated, error messages match spec

**Checkpoint**: Phase II complete and production-ready

---

## Phase 2.6: Documentation & Release Preparation

**Purpose**: Finalize documentation and prepare for deployment/submission

**Dependencies**: Phase 2.5 complete

- [ ] T205 Create migration guide from Phase I to Phase II for existing users
- [ ] T206 [P] Document all new error messages in contracts/cli-interface.md (if exists)
- [ ] T207 [P] Update data-model.md with new fields (priority, tags, created_at)
- [ ] T208 Create example usage scenarios document showing combined features (filter+sort, search+tag)
- [ ] T209 Git commit: "Complete Phase II - Intermediate Level Features" with comprehensive commit message
- [ ] T210 Git push to GitHub on feature branch (002-cli-todo-app-enhanced)
- [ ] T211 Create pull request comparing Phase II to Phase I (console-app branch)
- [ ] T212 Final validation: Clone fresh repository, run tests, verify everything works

**Checkpoint**: Phase II ready for release/submission

---

## Dependency Graph

### Critical Path (Cannot Be Parallelized)

```
Phase I Complete (93 tests passing)
  ↓
Phase 2.0: Data Model Migration (T100-T107)
  ↓
[Can parallelize US5 and US6]
  ↓
Phase 2.3: Search/Filter (needs US5 and US6 for filtering)
  ↓
Phase 2.5: Integration & Polish
  ↓
Phase 2.6: Documentation & Release
```

### Parallel Execution Opportunities

**After Phase 2.0 Complete**:
- Phase 2.1 (US5: Priority) and Phase 2.2 (US6: Tags) can run in parallel
- Phase 2.4 (US8: Sort) can start as soon as Phase 2.1 complete

**Testing**:
- All test files within same user story can be written in parallel (marked with [P])
- Unit tests, integration tests, and contract tests are independent

---

## Test Coverage Summary

### Phase I (Existing)
- Unit tests: 42
- Integration tests: 12
- Contract tests: 39
- **Total**: 93 tests ✅

### Phase II (New)
- Unit tests: ~50 (validation, storage operations, performance)
- Integration tests: ~16 (4 per user story × 4 stories)
- Contract tests: ~14 (prompts and messages for new features)
- **Total**: ~80 new tests

### Combined (Phase I + Phase II)
- **Grand Total**: ~173 tests
- **Target**: 100% pass rate
- **Performance**: All performance tests under specified thresholds

---

## Implementation Strategy

### TDD Workflow (MUST FOLLOW)

For each user story:

1. **RED**: Write tests first (T110-T115, T130-T136, etc.)
   - Run tests → verify they FAIL
   - Commit: "Add failing tests for US5" (or US6, US7, US8)

2. **GREEN**: Implement minimal code to pass tests (T116-T124, T137-T145, etc.)
   - Implement one function at a time
   - Run tests after each function → verify they PASS
   - Commit: "Implement validate_priority" (incremental commits)

3. **REFACTOR**: Clean up code, improve efficiency
   - Run all tests → verify still PASS
   - Commit: "Refactor priority validation logic"

4. **CHECKPOINT**: Run full suite before moving to next user story
   - All Phase I tests still pass (backward compatibility)
   - All new tests for current user story pass
   - Commit: "Complete User Story 5 - Priorities"

### Recommended Order

1. **Phase 2.0** (Foundation) - MUST be first
2. **Phase 2.1** (Priorities) - Start after 2.0
3. **Phase 2.2** (Tags) - Start after 2.0 (parallel with 2.1)
4. **Phase 2.4** (Sort) - Start after 2.1 complete (needs priority)
5. **Phase 2.3** (Search/Filter) - Start after 2.1 AND 2.2 complete
6. **Phase 2.5** (Integration) - After all user stories
7. **Phase 2.6** (Documentation) - Final step

---

## Success Criteria Checklist

Before marking Phase II complete, verify:

- [ ] ✅ All 93 Phase I tests still pass (backward compatibility)
- [ ] ✅ All ~80 Phase II tests pass (new features)
- [ ] ✅ Total test count: ~173 tests, 100% pass rate
- [ ] ✅ Search performance: <100ms for 1000 todos
- [ ] ✅ Filter performance: <50ms for 1000 todos
- [ ] ✅ Sort performance: <200ms for 1000 todos
- [ ] ✅ Priority display shows H/M/L in list view
- [ ] ✅ Tags display shows [tag1] [tag2] format
- [ ] ✅ Search finds keywords in title OR description
- [ ] ✅ Filters combine with AND logic
- [ ] ✅ Sort maintains stable order for equal elements
- [ ] ✅ All 13 menu options work correctly
- [ ] ✅ No crashes or unhandled exceptions
- [ ] ✅ Documentation updated (CLAUDE.md, README.md)
- [ ] ✅ Code committed and pushed to GitHub

---

**Task Count**: 113 tasks total (T100-T212)
**Estimated Effort**: 12-18 hours
**Parallel Opportunities**: ~40% of tasks can run in parallel (marked with [P])
**Critical Path**: ~10-12 hours (sequential tasks only)

**Created**: 2025-12-29
**Author**: Claude Code
**Status**: Ready for Implementation
**Next**: Begin with Phase 2.0 (Data Model Migration)
