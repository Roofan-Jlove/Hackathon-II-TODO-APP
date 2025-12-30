# Tasks: CLI Todo Application (Phase I)

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are INCLUDED per constitution's non-negotiable testability requirement (Principle III)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization with UV and basic structure

- [ ] T001 Initialize UV project with pyproject.toml configuration
- [ ] T002 Create virtual environment with UV (`uv venv`)
- [ ] T003 Create project directory structure (src/, tests/unit/, tests/integration/, tests/contract/)
- [ ] T004 Create empty module files: src/models.py, src/storage.py, src/cli.py, src/main.py
- [ ] T005 [P] Create empty test files: tests/unit/test_models.py, tests/unit/test_storage.py, tests/unit/test_cli.py
- [ ] T006 [P] Create empty test files: tests/integration/test_workflows.py, tests/contract/test_cli_interface.py
- [ ] T007 Verify UV setup with `uv run python --version` (should show Python 3.13+)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Setup global storage state in src/storage.py (todos list, next_id counter)
- [ ] T009 [P] Implement base validation helpers in src/models.py (validate_id function)
- [ ] T010 [P] Implement menu display function in src/cli.py (display_menu per CLI contract)
- [ ] T011 [P] Implement menu choice input function in src/cli.py (get_menu_choice with validation)
- [ ] T012 Implement main loop structure in src/main.py (while True loop with menu dispatch)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items and view all existing todos in a formatted list

**Independent Test**: Launch app, add 2-3 todos with different titles/descriptions, list them, verify they appear with unique sequential IDs and status indicators

### Tests for User Story 1 (Write FIRST, ensure they FAIL before implementation)

- [ ] T010 [P] [US1] Contract test for Add Todo operation in tests/contract/test_cli_interface.py (verify exact prompts, success message format, error messages)
- [ ] T011 [P] [US1] Contract test for List Todos operation in tests/contract/test_cli_interface.py (verify table format, empty list message)
- [ ] T012 [P] [US1] Integration test for User Story 1 acceptance scenarios in tests/integration/test_workflows.py (all 3 scenarios from spec.md)
- [ ] T013 [P] [US1] Unit test for validate_title in tests/unit/test_models.py (empty, too long, valid cases)
- [ ] T014 [P] [US1] Unit test for validate_description in tests/unit/test_models.py (too long, empty, valid cases)

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement validate_title function in src/models.py (return tuple: bool, error_message)
- [ ] T016 [P] [US1] Implement validate_description function in src/models.py (return tuple: bool, error_message)
- [ ] T017 [P] [US1] Implement create_todo function in src/models.py (return dict with id, title, description, completed)
- [ ] T018 [US1] Unit test for add_todo in tests/unit/test_storage.py (capacity check, validation, ID assignment, success cases)
- [ ] T019 [US1] Implement add_todo function in src/storage.py (validate, check capacity, assign ID, append to list)
- [ ] T020 [P] [US1] Unit test for get_all_todos in tests/unit/test_storage.py (empty list, sorted by ID)
- [ ] T021 [P] [US1] Implement get_all_todos function in src/storage.py (return sorted list by ID ascending)
- [ ] T022 [US1] Unit test for display_todos in tests/unit/test_cli.py (capture stdout, verify table format)
- [ ] T023 [US1] Implement display_todos function in src/cli.py (formatted table per CLI contract)
- [ ] T024 [US1] Implement get_user_input helper in src/cli.py (prompt and return user input)
- [ ] T025 [US1] Implement handle_add function in src/cli.py (prompt for title/description, call storage, display result)
- [ ] T026 [US1] Implement handle_list function in src/cli.py (call storage, display todos)
- [ ] T027 [US1] Wire up menu choices 1 (Add) and 2 (List) in src/main.py main loop

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add and view todos independently

---

## Phase 4: User Story 2 - Mark Completion Status (Priority: P2)

**Goal**: Enable users to toggle todo completion status (mark complete or incomplete)

**Independent Test**: Create 2 todos, mark one complete, list todos to verify status changes to [X], mark it incomplete again to verify toggle back to [ ]

### Tests for User Story 2

- [ ] T028 [P] [US2] Contract test for Mark Complete operation in tests/contract/test_cli_interface.py (verify prompts, success message, error messages)
- [ ] T029 [P] [US2] Contract test for Mark Incomplete operation in tests/contract/test_cli_interface.py (verify prompts, success message, idempotent behavior)
- [ ] T030 [P] [US2] Integration test for User Story 2 acceptance scenarios in tests/integration/test_workflows.py (all 3 scenarios from spec.md)

### Implementation for User Story 2

- [ ] T031 [P] [US2] Unit test for get_todo_by_id in tests/unit/test_storage.py (found, not found, invalid ID cases)
- [ ] T032 [P] [US2] Implement get_todo_by_id function in src/storage.py (return todo dict or None)
- [ ] T033 [US2] Unit test for mark_complete in tests/unit/test_storage.py (ID validation, status toggle, idempotent behavior)
- [ ] T034 [US2] Implement mark_complete function in src/storage.py (validate ID, toggle completed field, return success/error)
- [ ] T035 [US2] Implement handle_mark_complete function in src/cli.py (get ID, call storage, display result)
- [ ] T036 [US2] Implement handle_mark_incomplete function in src/cli.py (get ID, call storage mark_complete with False, display result)
- [ ] T037 [US2] Wire up menu choices 5 (Mark Complete) and 6 (Mark Incomplete) in src/main.py main loop

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo Content (Priority: P3)

**Goal**: Enable users to edit the title and/or description of existing todos

**Independent Test**: Create a todo, update its title, list to verify change, update description independently to verify both fields can be modified

### Tests for User Story 3

- [ ] T038 [P] [US3] Contract test for Update Todo operation in tests/contract/test_cli_interface.py (verify prompts, blank to skip behavior, error messages)
- [ ] T039 [P] [US3] Integration test for User Story 3 acceptance scenarios in tests/integration/test_workflows.py (all 3 scenarios from spec.md)

### Implementation for User Story 3

- [ ] T040 [US3] Unit test for update_todo in tests/unit/test_storage.py (ID validation, title/description update, keep current if blank)
- [ ] T041 [US3] Implement update_todo function in src/storage.py (validate ID, update title/description if provided, preserve if None)
- [ ] T042 [US3] Implement handle_update function in src/cli.py (get ID, prompt for new title/description, call storage, display result)
- [ ] T043 [US3] Wire up menu choice 3 (Update) in src/main.py main loop

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Todos (Priority: P4)

**Goal**: Enable users to remove todos they no longer need

**Independent Test**: Create 3 todos, delete the middle one by ID, list remaining todos to verify only 2 remain and IDs are preserved

### Tests for User Story 4

- [ ] T044 [P] [US4] Contract test for Delete Todo operation in tests/contract/test_cli_interface.py (verify prompts, success message, error messages)
- [ ] T045 [P] [US4] Integration test for User Story 4 acceptance scenarios in tests/integration/test_workflows.py (all 3 scenarios from spec.md)

### Implementation for User Story 4

- [ ] T046 [US4] Unit test for delete_todo in tests/unit/test_storage.py (ID validation, removal, ID preservation for remaining todos)
- [ ] T047 [US4] Implement delete_todo function in src/storage.py (validate ID, remove from list, IDs never reused)
- [ ] T048 [US4] Implement handle_delete function in src/cli.py (get ID, call storage, display result)
- [ ] T049 [US4] Wire up menu choice 4 (Delete) in src/main.py main loop

**Checkpoint**: All user stories (1-4) should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and finalize the application

- [ ] T050 [P] Implement menu choice 7 (Exit) in src/main.py (print goodbye message, break loop)
- [ ] T051 [P] Implement invalid menu choice handling in src/main.py (error message per CLI contract)
- [ ] T052 Add comprehensive docstrings to all functions in src/models.py following PEP 8
- [ ] T053 Add comprehensive docstrings to all functions in src/storage.py following PEP 8
- [ ] T054 Add comprehensive docstrings to all functions in src/cli.py following PEP 8
- [ ] T055 Add module-level docstrings and main entry point check in src/main.py
- [ ] T056 Run all unit tests and verify 100% pass: python -m unittest discover tests/unit -v
- [ ] T057 Run all integration tests and verify 100% pass: python -m unittest discover tests/integration -v
- [ ] T058 Run all contract tests and verify 100% pass: python -m unittest discover tests/contract -v
- [ ] T059 Manual validation against quickstart.md success criteria checklist
- [ ] T060 Final smoke test: Run application and execute all 7 menu operations successfully

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Reuses get_todo_by_id but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Reuses get_todo_by_id but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Reuses get_todo_by_id but independently testable

### Within Each User Story

1. **Tests FIRST** - Write all tests for the story and ensure they FAIL
2. **Models** - Validation functions (can be parallel)
3. **Storage** - CRUD operations (sequential, depends on models)
4. **CLI** - User interaction handlers (depends on storage)
5. **Main** - Wire up menu choices (depends on CLI handlers)
6. **Verify** - Run tests and ensure they PASS

### Parallel Opportunities

- **Phase 1**: T003 and T004 can run in parallel
- **Phase 2**: T006, T007, T008 can run in parallel after T005
- **User Story 1**:
  - Tests T010-T014 can all run in parallel
  - Models T015-T017 can all run in parallel
  - T020-T021 can run in parallel (after T018-T019 complete)
- **User Story 2**: Tests T028-T030 can run in parallel; T031-T032 can run in parallel
- **User Story 3**: Tests T038-T039 can run in parallel
- **User Story 4**: Tests T044-T045 can run in parallel
- **Phase 7**: T050-T051 can run in parallel; T052-T055 can run in parallel
- **Different user stories** can be worked on in parallel by different developers after Phase 2

---

## Parallel Example: User Story 1

```bash
# Step 1: Launch all tests for User Story 1 together (ensure they FAIL):
Task T010: "Contract test for Add Todo operation in tests/contract/test_cli_interface.py"
Task T011: "Contract test for List Todos operation in tests/contract/test_cli_interface.py"
Task T012: "Integration test for User Story 1 acceptance scenarios in tests/integration/test_workflows.py"
Task T013: "Unit test for validate_title in tests/unit/test_models.py"
Task T014: "Unit test for validate_description in tests/unit/test_models.py"

# Step 2: Launch all model functions for User Story 1 together:
Task T015: "Implement validate_title function in src/models.py"
Task T016: "Implement validate_description function in src/models.py"
Task T017: "Implement create_todo function in src/models.py"

# Step 3: After storage tests, launch parallel storage operations:
Task T020: "Unit test for get_all_todos in tests/unit/test_storage.py"
Task T021: "Implement get_all_todos function in src/storage.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T010-T027)
4. **STOP and VALIDATE**: Run all US1 tests independently
5. Manual test: Add and view todos in the application
6. Result: Working MVP with core todo management

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **Deploy/Demo (MVP!)**
3. Add User Story 2 → Test independently → Deploy/Demo (Status tracking added)
4. Add User Story 3 → Test independently → Deploy/Demo (Editing added)
5. Add User Story 4 → Test independently → Deploy/Demo (Deletion added)
6. Complete Polish → Final validation → Deploy/Demo (Full Phase I complete)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (after Phase 2 completes):

1. **Team completes Setup + Foundational together** (T001-T009)
2. Once Foundational is done, split work:
   - Developer A: User Story 1 (T010-T027)
   - Developer B: User Story 2 (T028-T037) - can start immediately
   - Developer C: User Story 3 (T038-T043) - can start immediately
   - Developer D: User Story 4 (T044-T049) - can start immediately
3. Stories complete and integrate independently
4. Team converges on Phase 7: Polish (T050-T060)

---

## Task Execution Summary

- **Total Tasks**: 60
- **Setup Phase**: 4 tasks
- **Foundational Phase**: 5 tasks (BLOCKS all user stories)
- **User Story 1 (P1)**: 18 tasks (MVP - Core functionality)
- **User Story 2 (P2)**: 10 tasks (Status tracking)
- **User Story 3 (P3)**: 6 tasks (Editing)
- **User Story 4 (P4)**: 6 tasks (Deletion)
- **Polish Phase**: 11 tasks (Finalization)

**Parallelizable Tasks**: 23 tasks marked with [P]

**MVP Scope**: Phases 1-3 only (27 tasks) delivers a working todo app with add/view functionality

**Test Coverage**: 20 test tasks ensuring all requirements are validated

---

## Notes

- All tasks follow strict checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [P] tasks target different files or have no dependencies - safe to parallelize
- [Story] labels enable traceability from task → user story → requirement → constitution principle
- Tests are written FIRST and must FAIL before implementation (TDD approach per constitution)
- Each user story is independently completable and testable (supports incremental delivery)
- Exact error messages from CLI contract must be used in implementation
- All code must follow PEP 8 style guidelines (NFR-014)
- No external dependencies beyond Python 3.8+ standard library (NFR-017)
- IDs are sequential and never reused (NFR-005)
- All validation uses exact messages from contracts/cli-interface.md
