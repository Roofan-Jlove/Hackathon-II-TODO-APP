# Feature Specification: Enhanced CLI Todo Application (3 Levels)

**Feature Branch**: `002-cli-todo-app-enhanced`
**Created**: 2025-12-29
**Status**: Planning
**Extends**: `001-cli-todo-app` (Basic Level - COMPLETE)

## Overview

**Purpose**: Extend the CLI Todo Manager from basic CRUD operations to an intermediate and advanced task management system with priorities, categories, search, filtering, sorting, recurring tasks, and due dates.

**Intended Users**: Individual users and professionals who need comprehensive task management through a command-line interface with organizational features and intelligent automation.

**Execution Environment**: Python 3.13+ console application managed with UV, running on standard terminal/command prompt.

**Technology Stack**:
- **UV**: Modern Python package and project manager (mandatory)
- **Python 3.13+**: Latest Python with modern features
- **datetime**: For due dates and time management
- **dateutil** or **schedule**: For recurring tasks (advanced level)

---

## Three-Level Architecture

### 🟢 Basic Level (COMPLETE ✅)
**Status**: Fully implemented and tested (93/93 tests passing)

Core essentials - foundation for any MVP:
1. ✅ **Add Task** – Create new todo items (User Story 1)
2. ✅ **Delete Task** – Remove tasks from the list (User Story 4)
3. ✅ **Update Task** – Modify existing task details (User Story 3)
4. ✅ **View Task List** – Display all tasks (User Story 1)
5. ✅ **Mark as Complete** – Toggle task completion status (User Story 2)

### 🟡 Intermediate Level (Phase II)
**Status**: To Be Implemented

Organization & usability features:
1. **Priorities** – Assign priority levels (High/Medium/Low)
2. **Tags/Categories** – Label tasks (work/personal/shopping/health)
3. **Search & Filter** – Find tasks by keyword, status, priority, or tag
4. **Sort Tasks** – Reorder by due date, priority, creation date, or alphabetically

### 🔴 Advanced Level (Phase III)
**Status**: Future Enhancement

Intelligent automation features:
1. **Recurring Tasks** – Auto-reschedule repeating tasks (daily/weekly/monthly)
2. **Due Dates & Reminders** – Set deadlines with date/time; display overdue warnings

---

## User Stories - Intermediate Level (Phase II)

### User Story 5 - Task Priorities (Priority: P5)

**As a user**, I want to assign priority levels to my tasks so that I can focus on what's most important.

**Why this priority**: Critical for task organization and productivity - helps users focus on high-impact work.

**Independent Test**: Create 3 todos with different priorities (High, Medium, Low), list todos to verify priorities are displayed, filter by High priority to verify only high-priority tasks appear.

**Acceptance Scenarios**:

1. **Given** user is adding a new todo, **When** user selects priority "High", **Then** todo is created with High priority and displays with priority indicator
2. **Given** existing todo with Medium priority, **When** user updates priority to High, **Then** priority changes to High and listing reflects this
3. **Given** todos exist with different priorities, **When** user requests list view, **Then** system displays priority for each todo (H/M/L indicator or color)

**Priority Options**:
- **High** (H) - Urgent, critical tasks
- **Medium** (M) - Standard priority (default)
- **Low** (L) - Nice-to-have, can wait

---

### User Story 6 - Tags and Categories (Priority: P6)

**As a user**, I want to organize my tasks with tags/categories so that I can group related tasks together.

**Why this priority**: Enables better organization for users with diverse task types (work/personal/projects).

**Independent Test**: Create todos with different tags (work, personal, shopping), add multiple tags to one todo, filter by tag to verify only tagged tasks appear.

**Acceptance Scenarios**:

1. **Given** user is adding a new todo, **When** user adds tags "work, urgent", **Then** todo is created with both tags
2. **Given** existing todo without tags, **When** user adds tag "personal", **Then** tag is added and listing reflects this
3. **Given** todos with different tags, **When** user filters by tag "work", **Then** system displays only todos tagged with "work"

**Tag Features**:
- Multiple tags per todo (comma-separated)
- Common tags: work, personal, shopping, health, family, urgent
- Case-insensitive tag matching
- Display tags in square brackets: `[work] [urgent]`

---

### User Story 7 - Search and Filter (Priority: P7)

**As a user**, I want to search for tasks by keyword and filter by various criteria so that I can quickly find specific tasks.

**Why this priority**: Essential for productivity with large task lists - reduces time spent scrolling.

**Independent Test**: Create 10 todos with varied titles, descriptions, priorities, and tags. Search for keyword in title, filter by incomplete status, filter by High priority, verify each filter returns correct subset.

**Acceptance Scenarios**:

1. **Given** 10 todos exist, **When** user searches for keyword "grocery", **Then** system displays only todos containing "grocery" in title or description
2. **Given** todos with different statuses, **When** user filters by "incomplete", **Then** system displays only incomplete todos
3. **Given** todos with different priorities and tags, **When** user filters by "High priority" AND "work tag", **Then** system displays only High-priority work todos

**Filter Criteria**:
- **By Status**: Complete, Incomplete, All
- **By Priority**: High, Medium, Low, All
- **By Tag**: Any specific tag
- **By Keyword**: Search in title and description
- **Combined Filters**: Multiple criteria (AND logic)

---

### User Story 8 - Sort Tasks (Priority: P8)

**As a user**, I want to sort my task list by different criteria so that I can view tasks in the most relevant order.

**Why this priority**: Improves usability and helps users focus on the right tasks at the right time.

**Independent Test**: Create 5 todos with different priorities, creation dates, and titles. Sort alphabetically to verify A-Z order, sort by priority to verify High-Medium-Low order, sort by creation date to verify newest-first.

**Acceptance Scenarios**:

1. **Given** todos with different titles, **When** user sorts alphabetically, **Then** todos appear in A-Z order by title
2. **Given** todos with different priorities, **When** user sorts by priority, **Then** todos appear High > Medium > Low
3. **Given** todos created at different times, **When** user sorts by creation date, **Then** todos appear newest-first or oldest-first

**Sort Options**:
- **Alphabetically**: A-Z by title
- **By Priority**: High → Medium → Low
- **By Creation Date**: Newest first or Oldest first
- **By Status**: Incomplete first, then Complete
- **By Due Date**: Upcoming first (when advanced level implemented)

---

## User Stories - Advanced Level (Phase III)

### User Story 9 - Recurring Tasks (Priority: P9)

**As a user**, I want to create recurring tasks that automatically reschedule so that I don't have to manually re-add regular tasks.

**Why this priority**: Powerful automation for repetitive workflows - saves time and ensures consistency.

**Independent Test**: Create recurring task "Weekly team meeting" with weekly recurrence, mark it complete, verify new instance is auto-created for next week with same details.

**Acceptance Scenarios**:

1. **Given** user creates a task, **When** user sets recurrence to "Daily", **Then** task is marked as recurring and displays recurrence indicator
2. **Given** recurring task with weekly schedule, **When** user marks it complete, **Then** system auto-creates next instance scheduled for next week
3. **Given** user wants to stop recurrence, **When** user removes recurrence from task, **Then** task becomes one-time only

**Recurrence Patterns**:
- **Daily**: Every day at same time
- **Weekly**: Every 7 days (e.g., every Monday)
- **Monthly**: Same day each month (e.g., 1st of month)
- **Weekdays**: Monday-Friday only
- **Custom**: Every N days/weeks/months

**Behavior**:
- When marked complete, auto-create next instance
- Next instance inherits title, description, priority, tags
- Original instance remains in history
- Display recurrence: `🔁 Every Monday`

---

### User Story 10 - Due Dates and Reminders (Priority: P10)

**As a user**, I want to set due dates for my tasks and see overdue warnings so that I never miss important deadlines.

**Why this priority**: Critical for deadline-driven work - prevents missed deadlines and improves accountability.

**Independent Test**: Create task with due date tomorrow, create task with due date yesterday, list tasks to verify overdue task is highlighted, verify upcoming tasks show days remaining.

**Acceptance Scenarios**:

1. **Given** user creates a task, **When** user sets due date to "2025-12-31 14:00", **Then** task displays due date in list view
2. **Given** task with due date in the past, **When** user lists tasks, **Then** overdue task is highlighted/marked with warning indicator
3. **Given** task due today, **When** user lists tasks, **Then** task shows "DUE TODAY" indicator
4. **Given** task due in 3 days, **When** user lists tasks, **Then** task shows "3 days left"

**Due Date Features**:
- **Date Entry**: YYYY-MM-DD format or relative (tomorrow, next week, +3d)
- **Time Entry**: HH:MM (24-hour) or omit for all-day task
- **Visual Indicators**:
  - 🔴 OVERDUE (past due date)
  - 🟡 DUE TODAY
  - 🟢 UPCOMING (due in 1-7 days)
  - ⚪ FUTURE (due in >7 days)

**Display Format**:
```
ID | Status | Priority | Title              | Due Date      | Tags
---|--------|----------|--------------------|--------------|---------
1  | [ ]    | H        | Submit report      | 🔴 Yesterday | [work]
2  | [ ]    | M        | Buy groceries      | 🟡 Today     | [personal]
3  | [ ]    | L        | Read book chapter  | 🟢 3 days    | [personal]
```

---

## Requirements - Intermediate Level

### Functional Requirements

**Priorities (FR-I-001 to FR-I-003)**:
- **FR-I-001**: System MUST support three priority levels: High, Medium (default), Low
- **FR-I-002**: System MUST allow users to set priority during creation and update it later
- **FR-I-003**: System MUST display priority indicator (H/M/L) in list view

**Tags/Categories (FR-I-004 to FR-I-006)**:
- **FR-I-004**: System MUST allow multiple comma-separated tags per todo
- **FR-I-005**: System MUST store tags as case-insensitive (work = Work = WORK)
- **FR-I-006**: System MUST display tags in square brackets in list view

**Search & Filter (FR-I-007 to FR-I-010)**:
- **FR-I-007**: System MUST support keyword search in title and description
- **FR-I-008**: System MUST support filtering by status (complete/incomplete)
- **FR-I-009**: System MUST support filtering by priority level
- **FR-I-010**: System MUST support filtering by tag
- **FR-I-011**: System MUST support combining multiple filters (AND logic)

**Sort (FR-I-012 to FR-I-015)**:
- **FR-I-012**: System MUST support sorting alphabetically by title
- **FR-I-013**: System MUST support sorting by priority (High > Medium > Low)
- **FR-I-014**: System MUST support sorting by creation date (newest/oldest first)
- **FR-I-015**: System MUST support sorting by status (incomplete first)

### Non-Functional Requirements (Intermediate)

- **NFR-I-001**: Search operations MUST complete in <100ms for up to 1000 todos
- **NFR-I-002**: Filter operations MUST complete in <50ms for up to 1000 todos
- **NFR-I-003**: Sort operations MUST complete in <200ms for up to 1000 todos
- **NFR-I-004**: Tags MUST support Unicode characters (emoji support)

---

## Requirements - Advanced Level

### Functional Requirements

**Recurring Tasks (FR-A-001 to FR-A-005)**:
- **FR-A-001**: System MUST support daily, weekly, monthly recurrence patterns
- **FR-A-002**: System MUST auto-create next instance when recurring task is completed
- **FR-A-003**: System MUST preserve all attributes (priority, tags, description) in next instance
- **FR-A-004**: System MUST allow users to disable recurrence
- **FR-A-005**: System MUST display recurrence indicator (🔁) in list view

**Due Dates (FR-A-006 to FR-A-011)**:
- **FR-A-006**: System MUST accept due dates in YYYY-MM-DD format
- **FR-A-007**: System MUST accept relative due dates (tomorrow, +3d, next week)
- **FR-A-008**: System MUST support optional time in HH:MM format
- **FR-A-009**: System MUST calculate and display days until due/overdue
- **FR-A-010**: System MUST highlight overdue tasks in red
- **FR-A-011**: System MUST sort by due date (soonest first)

### Non-Functional Requirements (Advanced)

- **NFR-A-001**: Date parsing MUST handle invalid dates gracefully with clear error messages
- **NFR-A-002**: Recurring task generation MUST not create duplicates
- **NFR-A-003**: System MUST handle timezone correctly for due date calculations
- **NFR-A-004**: Overdue calculation MUST run each time list is displayed (real-time)

---

## Updated Data Model

### Enhanced Todo Entity

```python
{
    "id": int,              # Unique identifier (auto-assigned)
    "title": str,           # Task title (required, max 200 chars)
    "description": str,     # Task details (optional, max 1000 chars)
    "completed": bool,      # Completion status (default: False)

    # Intermediate Level Fields
    "priority": str,        # "High", "Medium", "Low" (default: "Medium")
    "tags": list[str],      # List of tags (default: [])
    "created_at": datetime, # Creation timestamp (auto-assigned)

    # Advanced Level Fields
    "due_date": datetime | None,   # Due date/time (optional)
    "recurrence": dict | None,     # Recurrence pattern (optional)
    # Example recurrence: {"pattern": "weekly", "interval": 1}
}
```

---

## Menu Structure - All Levels

### Enhanced Main Menu
```
Welcome to Enhanced Todo Manager
--------------------------------
BASIC OPERATIONS:
  1. Add Todo
  2. List All Todos
  3. Update Todo
  4. Delete Todo
  5. Mark Complete/Incomplete

INTERMEDIATE FEATURES:
  6. Set Priority
  7. Add/Remove Tags
  8. Search & Filter
  9. Sort Tasks

ADVANCED FEATURES:
  10. Set Recurring
  11. Set Due Date
  12. View Overdue Tasks

OTHER:
  13. Exit

Enter choice [1-13]: _
```

---

## Implementation Phases

### Phase I: Basic Level ✅ COMPLETE
- User Stories 1-4
- All CRUD operations
- 93/93 tests passing

### Phase II: Intermediate Level 🚧 IN PROGRESS
- User Stories 5-8
- Priorities and tags
- Search, filter, sort
- Estimated: 50+ new tests

### Phase III: Advanced Level 📋 PLANNED
- User Stories 9-10
- Recurring tasks
- Due dates and reminders
- Estimated: 30+ new tests

---

## Success Criteria - All Levels

### Basic Level (SC-B-001 to SC-B-006) ✅ ALL MET
- All original success criteria met (see 001-cli-todo-app/spec.md)

### Intermediate Level (SC-I-001 to SC-I-005)
- **SC-I-001**: Users can assign and update priority within 2 interactions
- **SC-I-002**: Users can add multiple tags to a task with comma separation
- **SC-I-003**: Search returns results in <100ms for 1000 todos
- **SC-I-004**: Filters can be combined (e.g., High priority + work tag)
- **SC-I-005**: Sort order is immediately visible in list view

### Advanced Level (SC-A-001 to SC-A-004)
- **SC-A-001**: Recurring tasks auto-generate next instance upon completion
- **SC-A-002**: Due dates accept both absolute and relative formats
- **SC-A-003**: Overdue tasks are visually distinct in all views
- **SC-A-004**: Users can set due date within 3 interactions

---

## Migration Path

### From Basic to Intermediate
1. Add priority field to existing todos (default: "Medium")
2. Add tags field to existing todos (default: empty list)
3. Add created_at timestamp to existing todos (use current time)
4. Extend CLI with new menu options
5. Implement search/filter/sort logic
6. Add new tests for intermediate features

### From Intermediate to Advanced
1. Add due_date field to existing todos (default: None)
2. Add recurrence field to existing todos (default: None)
3. Implement recurring task scheduler
4. Implement due date parser and calculator
5. Update display logic for overdue indicators
6. Add new tests for advanced features

---

**Next Steps**:
1. Create plan.md for Phase II implementation
2. Break down tasks.md for User Stories 5-8
3. Design data migration strategy
4. Implement intermediate features with TDD approach
5. Achieve 100% test coverage for new features

---

**Created**: 2025-12-29
**Author**: Enhanced with Claude Code
**Version**: 1.0 (Planning Phase)
