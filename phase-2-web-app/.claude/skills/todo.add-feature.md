---
description: Add a new feature to the TODO app with full spec-driven workflow (spec → plan → tasks → implement)
---

## User Input

```text
$ARGUMENTS
```

## Instruction

You are coordinating the addition of a new feature to the TODO app. Follow the complete Spec-Driven Development workflow:

1. **Specification Phase**: Create a detailed spec in `specs/<feature-name>/spec.md` that includes:
   - Feature scope and boundaries
   - User interaction model
   - Data structures and invariants
   - Error conditions and handling
   - Acceptance criteria

2. **Planning Phase**: Create architectural plan in `specs/<feature-name>/plan.md`:
   - Design decisions and rationale
   - Interface contracts
   - Non-functional requirements
   - Risk analysis
   - Suggest ADR if architecturally significant

3. **Task Breakdown**: Generate `specs/<feature-name>/tasks.md`:
   - Dependency-ordered tasks
   - Test cases for each task
   - Clear acceptance criteria

4. **Implementation**: Coordinate implementation following tasks.md

5. **Documentation**: Create PHR in `history/prompts/<feature-name>/`

Engage the todo-main-agent to orchestrate this workflow and delegate to specialized sub-agents as needed.
