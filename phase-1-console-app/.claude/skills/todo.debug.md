---
description: Debug and fix issues in the TODO app with root cause analysis and spec-compliant solutions
---

## User Input

```text
$ARGUMENTS
```

## Instruction

You are debugging an issue in the TODO app. Follow systematic debugging process:

1. **Issue Reproduction**:
   - Understand the reported problem
   - Identify steps to reproduce
   - Gather relevant context (logs, error messages, input data)

2. **Root Cause Analysis**:
   - Trace execution flow
   - Identify where actual behavior diverges from expected
   - Determine underlying cause (not just symptoms)
   - Check if issue relates to spec ambiguity

3. **Solution Design**:
   - Propose fix that addresses root cause
   - Ensure solution complies with existing specs
   - Consider impact on other features
   - Identify if spec needs update

4. **Implementation**:
   - Apply minimal fix (no unnecessary refactoring)
   - Add tests to prevent regression
   - Validate fix resolves the issue
   - Verify no new issues introduced

5. **Documentation**:
   - Document root cause and solution
   - Update specs if needed
   - Create PHR for debugging session

Use todo-main-agent to coordinate debugging workflow and delegate to specialized agents as needed.
