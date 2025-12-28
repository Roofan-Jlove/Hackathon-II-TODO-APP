# CLI Interface Contract: Todo Manager

**Feature**: 001-cli-todo-app
**Date**: 2025-12-28
**Purpose**: Define the contract between user and application for all CLI interactions

## Menu Interface

### Main Menu Display

**Contract**: Application MUST display this exact menu after startup and after each operation completes

```
Welcome to Todo Manager
-----------------------
1. Add Todo
2. List All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo Complete
6. Mark Todo Incomplete
7. Exit

Enter choice [1-7]: _
```

**Inputs**: User enters a single character ('1' through '7')
**Outputs**: Menu disappears, operation executes, menu redisplays (except for Exit)

### Input Validation

**Invalid Choice Contract**:
- **Input**: Any value not in {'1', '2', '3', '4', '5', '6', '7'}
- **Output**: `"Error: Invalid choice. Please enter 1-7."`
- **Behavior**: Menu redisplays immediately

## Operation 1: Add Todo

### Input Sequence

**Step 1 - Title Input**:
```
Enter title: _
```
- User inputs title text and presses Enter
- Validation: See "Add Todo Validation" below

**Step 2 - Description Input**:
```
Enter description (optional, press Enter to skip): _
```
- User inputs description text OR presses Enter without text
- If Enter without text: description = empty string
- Validation: See "Add Todo Validation" below

### Output

**Success Case**:
```
Todo added successfully! (ID: N)
```
Where N is the assigned ID (positive integer)

**Error Cases**:

| Condition | Output Message |
|-----------|----------------|
| Title is empty | `Error: Title cannot be empty.` |
| Title > 200 characters | `Error: Title exceeds 200 character limit.` |
| Description > 1000 characters | `Error: Description exceeds 1000 character limit.` |
| Already 1000 todos exist | `Error: Maximum 1000 todos reached.` |

### Add Todo Validation

1. Check title not empty
2. Check title length ≤ 200
3. Check description length ≤ 1000 (if provided)
4. Check total todo count < 1000
5. If all pass: Create todo, assign ID, return success
6. If any fail: Return appropriate error message, do not create todo

## Operation 2: List All Todos

### Input

No additional input required (menu choice '2' is sufficient)

### Output

**Empty List Case**:
```
No todos found.
```

**Populated List Case**:
```
ID | Status | Title           | Description
---|--------|-----------------|------------------
1  | [ ]    | Buy groceries   | Milk, eggs, bread
2  | [X]    | Call dentist    | Schedule checkup
3  | [ ]    | Write report    |
```

**Format Contract**:
- Header row with column names separated by ` | `
- Separator row with `---|--------|-----------------|------------------`
- Data rows with fields aligned under headers
- Status: `[ ]` for incomplete (completed=false), `[X]` for complete (completed=true)
- Empty description shown as blank (no placeholder text)
- Todos ordered by ID ascending
- All todos in memory displayed (no pagination for Phase I)

## Operation 3: Update Todo

### Input Sequence

**Step 1 - ID Input**:
```
Enter todo ID: _
```
- User inputs ID number
- Validation: Must be positive integer, must exist in list

**Step 2 - Title Input**:
```
Enter new title (leave blank to keep current): _
```
- User inputs new title OR presses Enter to skip
- If Enter without text: title unchanged
- If text provided: validate as per Add Todo rules

**Step 3 - Description Input**:
```
Enter new description (leave blank to keep current): _
```
- User inputs new description OR presses Enter to skip
- If Enter without text: description unchanged
- If text provided: validate length ≤ 1000

### Output

**Success Case**:
```
Todo ID N updated successfully!
```

**Error Cases**:

| Condition | Output Message |
|-----------|----------------|
| ID not found | `Error: Todo with ID N not found.` |
| ID not a number | `Error: ID must be a positive integer.` |
| New title empty | `Error: Title cannot be empty.` |
| New title > 200 characters | `Error: Title exceeds 200 character limit.` |
| New description > 1000 characters | `Error: Description exceeds 1000 character limit.` |

## Operation 4: Delete Todo

### Input Sequence

**Step 1 - ID Input**:
```
Enter todo ID to delete: _
```
- User inputs ID number
- Validation: Must be positive integer, must exist in list

### Output

**Success Case**:
```
Todo ID N deleted successfully!
```

**Error Cases**:

| Condition | Output Message |
|-----------|----------------|
| ID not found | `Error: Todo with ID N not found.` |
| ID not a number | `Error: ID must be a positive integer.` |

## Operation 5: Mark Todo Complete

### Input Sequence

**Step 1 - ID Input**:
```
Enter todo ID: _
```
- User inputs ID number
- Validation: Must be positive integer, must exist in list

### Output

**Success Case**:
```
Todo ID N marked as complete!
```

**Error Cases**:

| Condition | Output Message |
|-----------|----------------|
| ID not found | `Error: Todo with ID N not found.` |
| ID not a number | `Error: ID must be a positive integer.` |

**Note**: Marking an already-complete todo as complete is allowed (idempotent operation) and shows success message.

## Operation 6: Mark Todo Incomplete

### Input Sequence

**Step 1 - ID Input**:
```
Enter todo ID: _
```
- User inputs ID number
- Validation: Must be positive integer, must exist in list

### Output

**Success Case**:
```
Todo ID N marked as incomplete!
```

**Error Cases**:

| Condition | Output Message |
|-----------|----------------|
| ID not found | `Error: Todo with ID N not found.` |
| ID not a number | `Error: ID must be a positive integer.` |

**Note**: Marking an already-incomplete todo as incomplete is allowed (idempotent operation) and shows success message.

## Operation 7: Exit

### Input

No additional input required (menu choice '7' is sufficient)

### Output

```
Goodbye! All todos will be lost.
```

**Behavior**: Application terminates, all data in memory is lost

## Error Handling Contract

### General Principles

1. **No Application Crashes**: All errors result in user-friendly messages, not stack traces
2. **Operation Continues**: After displaying error, menu redisplays (no application exit)
3. **Exact Messages**: Error messages match the specified strings exactly
4. **Immediate Feedback**: Errors detected before any state changes occur
5. **Clear Indication**: Error messages start with "Error: " prefix

### Error Message Format

All error messages follow this pattern:
```
Error: [Clear description of the problem]
```

### Input Type Validation

For ID inputs expecting integers:
- Non-numeric input (e.g., "abc", "1.5"): `"Error: ID must be a positive integer."`
- Negative or zero: `"Error: ID must be a positive integer."`
- Valid integer but non-existent: `"Error: Todo with ID N not found."`

## Performance Contract

**Response Time**: All operations MUST complete in under 1 second for todo lists up to 1000 items

**Capacity**: Application MUST support up to 1000 todos without degradation

## I/O Contract

**Input Source**: Standard input (stdin) only
**Output Destination**: Standard output (stdout) only
**Character Encoding**: UTF-8
**Line Endings**: Platform-native (LF on Unix, CRLF on Windows - Python handles automatically)

## Determinism Contract

**Identical Inputs → Identical Outputs**: Given the same sequence of menu choices and user inputs, the application MUST produce identical outputs every time

**Sequential IDs**: ID assignment is strictly sequential (1, 2, 3, ...) and never reused

**Predictable Ordering**: List display is always ordered by ID ascending
