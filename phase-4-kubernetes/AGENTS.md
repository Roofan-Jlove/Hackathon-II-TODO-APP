# AI Agent Behavior Rules - Spec-Driven Development

This document defines **mandatory behavior rules** for all AI agents (Claude Code, GitHub Copilot, ChatGPT, etc.) working on this project.

**CRITICAL:** This project uses **Spec-Driven Development (SDD)**. No agent is allowed to write code until the specification is complete and approved.

---

## 1. PURPOSE

### Spec-Driven Development Philosophy

This project follows **Spec-Driven Development (SDD)**, a disciplined approach where:

- **Specifications come first** - Code is never written before specs
- **Specs are the source of truth** - All decisions must be documented
- **No improvisation** - Agents cannot invent requirements or architecture
- **Quality by design** - Prevent bugs by thinking before coding

### The Spec-Kit Lifecycle

All AI agents **MUST** follow this lifecycle:

```
1. Constitution (WHY)    → Principles & Constraints
2. Specify (WHAT)        → Requirements & Acceptance Criteria
3. Plan (HOW)            → Architecture & Design
4. Tasks (BREAKDOWN)     → Atomic Work Units
5. Implement (CODE)      → Execution
```

**Golden Rule:** No spec = No code. Every line of code must trace back to a specification.

---

## 2. HOW AGENTS MUST WORK

### Strict Rules for All AI Agents

#### Rule 1: No Code Without Task ID
```
❌ FORBIDDEN: Writing code without a Task ID
✅ REQUIRED: Every code block must reference a Task ID

Example:
# [Task]: T-001
# [From]: speckit.specify §2.1, speckit.plan §3.4
def create_todo(title: str, description: str):
    ...
```

#### Rule 2: No Architecture Changes Without Plan Update
```
❌ FORBIDDEN: "Let me add a caching layer..."
✅ REQUIRED: "This requires updating speckit.plan §4.2 to add a caching component"
```

#### Rule 3: No Features Without Requirements
```
❌ FORBIDDEN: "I'll add email notifications for completed tasks"
✅ REQUIRED: "Email notifications are not in speckit.specify. Should I propose adding them?"
```

#### Rule 4: Constitution Defines Constraints
```
❌ FORBIDDEN: Switching tech stack without justification
✅ REQUIRED: Follow stack defined in speckit.constitution
```

#### Rule 5: Every Code File Must Link to Specs
```python
"""
Todo CRUD Operations

[Task]: T-003
[Spec]: speckit.specify §3.1 - Todo Management
[Plan]: speckit.plan §2.3 - Storage Layer
[AC]: User can create, read, update, delete todos
"""
```

### What to Do When Specs Are Missing

If an agent cannot find the required specification:

1. **STOP immediately** - Do not proceed with implementation
2. **Identify what's missing** - Which spec file needs updating?
3. **Request clarification** - Ask the user to update the spec
4. **Never improvise** - Do not invent requirements or design

**Example:**
```
Agent: "I need to implement user authentication, but I cannot find:
- speckit.specify §X - Authentication requirements (WHAT)
- speckit.plan §Y - Auth architecture (HOW)
- speckit.tasks - Task breakdown for auth

Please provide these specifications before I proceed."
```

---

## 3. SPEC-KIT WORKFLOW (Source of Truth)

### Stage 1: Constitution (WHY - Principles & Constraints)

**File:** `.specify/memory/constitution.md` or `speckit.constitution`

**Purpose:** Defines project non-negotiables and foundational principles

**Contains:**
- Architecture values (e.g., "Functional programming preferred")
- Security rules (e.g., "All inputs must be validated")
- Tech stack constraints (e.g., "Python 3.13+, FastAPI, Next.js 14+")
- Performance expectations (e.g., "API responses < 200ms")
- Allowed patterns (e.g., "No classes in backend storage layer")
- Coding standards (e.g., "TypeScript strict mode required")

**Agent Behavior:**
- Read constitution at start of every session
- Never violate constitutional principles
- Suggest updates if constraints conflict with requirements

**Example:**
```markdown
# Constitution

## Architecture Principles
- Functional programming for backend storage layer (no classes)
- RESTful API design with proper HTTP methods
- Separation of concerns (models, storage, routers)

## Security Rules
- All user inputs must be validated
- Passwords must be hashed with bcrypt
- SQL injection prevention via SQLModel ORM
```

---

### Stage 2: Specify (WHAT - Requirements)

**File:** `specs/features/[feature].md` or `speckit.specify`

**Purpose:** Defines WHAT the system must do (business requirements)

**Contains:**
- User stories and journeys
- Functional requirements
- Acceptance criteria
- Domain rules and business logic
- Business constraints
- Edge cases and error conditions

**Agent Behavior:**
- Never infer missing requirements
- Ask for clarification if acceptance criteria are unclear
- Do not add features not specified here
- Reference specific sections when implementing

**Example:**
```markdown
# Feature Specification: Todo CRUD

## User Story
As a user, I want to create, read, update, and delete todos so I can manage my tasks.

## Acceptance Criteria
- AC1: User can create a todo with title (required) and description (optional)
- AC2: Title must be 1-200 characters
- AC3: Description must be 0-1000 characters
- AC4: User can list all todos with ID, title, description, status
- AC5: User can update todo title and description
- AC6: User can delete todo by ID
- AC7: IDs are never reused

## Edge Cases
- Empty title returns error: "Error: Title cannot be empty."
- Title > 200 chars returns error: "Error: Title exceeds 200 character limit."
```

---

### Stage 3: Plan (HOW - Architecture)

**File:** `specs/[feature]/plan.md` or `speckit.plan`

**Purpose:** Defines HOW the system will be built (technical design)

**Contains:**
- Component breakdown
- API endpoint specifications
- Database schema and relationships
- Service boundaries
- System responsibilities
- High-level sequencing (which components call which)
- File structure and module organization

**Agent Behavior:**
- Follow the plan exactly - no creative reinterpretation
- Do not add components not in the plan
- Suggest plan updates if better approach found (but get approval first)
- Reference specific plan sections in code

**Example:**
```markdown
# Implementation Plan: Todo CRUD

## Component Breakdown

### Backend Components
1. **models.py** - Data validation functions
   - validate_title(title: str) -> (bool, str)
   - validate_description(desc: str) -> (bool, str)

2. **storage.py** - CRUD operations
   - add_todo(title, description) -> (bool, id, message)
   - get_all_todos() -> list[dict]
   - update_todo(id, title, description) -> (bool, message)
   - delete_todo(id) -> (bool, message)

3. **routers/todos.py** - API endpoints
   - POST /api/todos - Create todo
   - GET /api/todos - List todos
   - PUT /api/todos/{id} - Update todo
   - DELETE /api/todos/{id} - Delete todo

## API Specifications

### POST /api/todos
Request:
{
  "title": string (1-200 chars, required),
  "description": string (0-1000 chars, optional)
}

Response (201):
{
  "id": int,
  "title": string,
  "description": string,
  "message": "Todo created successfully"
}
```

---

### Stage 4: Tasks (BREAKDOWN - Atomic Work Units)

**File:** `specs/[feature]/tasks.md` or `speckit.tasks`

**Purpose:** Breaks down plan into implementable atomic tasks

**Each Task Must Contain:**
- **Task ID** - Unique identifier (e.g., T-001, T-002)
- **Clear description** - One sentence summary
- **Preconditions** - What must exist before starting
- **Expected outputs** - What artifacts will be created/modified
- **Artifacts to modify** - Specific files to change
- **Links to specs** - References to Specify and Plan sections
- **Acceptance criteria** - How to verify completion

**Agent Behavior:**
- Only implement tasks that are defined
- Reference Task ID in all code
- Do not skip preconditions
- Verify acceptance criteria before marking complete

**Example:**
```markdown
# Tasks: Todo CRUD

## T-001: Create Todo Validation Functions
**Description:** Implement title and description validation in models.py
**Preconditions:** None
**Artifacts:** backend/app/models.py
**Spec Reference:** speckit.specify §2.1, speckit.plan §1.1
**Acceptance Criteria:**
- validate_title() returns (True, "") for valid titles
- validate_title() returns (False, error) for empty or long titles
- validate_description() returns (True, "") for valid descriptions
- validate_description() returns (False, error) for long descriptions

## T-002: Implement Todo Storage Operations
**Description:** Create CRUD functions in storage.py
**Preconditions:** T-001 complete
**Artifacts:** backend/app/storage.py
**Spec Reference:** speckit.specify §2.1, speckit.plan §1.2
**Acceptance Criteria:**
- add_todo() creates todo and returns ID
- get_all_todos() returns all todos
- update_todo() updates existing todo
- delete_todo() removes todo by ID
```

---

### Stage 5: Implement (CODE - Execute)

**Purpose:** Write code that implements the tasks

**Agents Can Now Write Code, But Must:**
- Reference Task IDs in every file
- Follow the Plan exactly
- Not invent new features or components
- Stop if anything is underspecified
- Validate against acceptance criteria

**Code Template:**
```python
"""
Module: Todo Storage Operations

[Task]: T-002
[Spec]: speckit.specify §2.1 - Todo Management
[Plan]: speckit.plan §1.2 - Storage Layer
[AC]: CRUD operations for todos with validation
"""

def add_todo(title: str, description: str | None) -> tuple[bool, int | None, str]:
    """
    Create a new todo item.

    [Task]: T-002
    [Spec]: speckit.specify §2.1 AC1-AC3

    Args:
        title: Todo title (1-200 chars, required)
        description: Todo description (0-1000 chars, optional)

    Returns:
        (success: bool, todo_id: int | None, message: str)
    """
    # Implementation follows plan §1.2
    ...
```

**Golden Rule:** No task = No code.

---

## 4. AGENT BEHAVIOR IN THIS PROJECT

### When Generating Code

**ALWAYS include these references:**

```python
"""
[Task]: T-003
[From]: speckit.specify §2.1, speckit.plan §3.4
"""
```

### When Proposing Architecture Changes

**STOP and request spec update:**

```
Agent: "The current plan uses in-memory storage, but the requirement
for persistence suggests we need a database.

Required update: speckit.plan §1.2 - Change storage from in-memory to PostgreSQL

Please approve this architectural change before I proceed."
```

### When Proposing New Features

**STOP and request requirements update:**

```
Agent: "I notice we could add email notifications when todos are completed.
However, this is not in the current specification.

Required update: speckit.specify - Add new user story for email notifications

Should I propose this feature, or should we focus on current requirements?"
```

### When Encountering Ambiguity

**STOP and request clarification:**

```
Agent: "The specification says 'users can filter todos' but doesn't specify:
- Filter by what fields? (status, priority, tags?)
- Can multiple filters be combined?
- What's the default filter state?

Please update speckit.specify §3.2 with these details before I implement filtering."
```

---

## 5. AGENT FAILURE MODES (What Agents MUST Avoid)

### ❌ FORBIDDEN: Freestyle Code
```python
# WRONG - No task reference, no spec link
def send_email(user_id, message):
    # Agent invented this feature
    ...
```

### ❌ FORBIDDEN: Architecture Improvisation
```
Agent: "I'll add Redis caching to improve performance"
Problem: Caching not in speckit.plan
```

### ❌ FORBIDDEN: Generating Missing Requirements
```
Agent: "Since the spec doesn't say, I'll assume users want dark mode"
Problem: Requirements must come from speckit.specify, not agent assumptions
```

### ❌ FORBIDDEN: Self-Created Tasks
```
Agent: "I'll break this down into 5 tasks..."
Problem: Tasks must be defined in speckit.tasks first
```

### ❌ FORBIDDEN: Stack Changes Without Justification
```
Agent: "I'll use MongoDB instead of PostgreSQL"
Problem: Stack defined in speckit.constitution
```

### ❌ FORBIDDEN: Undocumented Endpoints
```python
# WRONG - Endpoint not in speckit.plan
@router.post("/api/todos/bulk-delete")
def bulk_delete_todos():
    ...
```

### ❌ FORBIDDEN: Ignoring Acceptance Criteria
```
Agent implements feature but skips edge cases defined in speckit.specify
```

### ❌ FORBIDDEN: Creative Implementations
```
Agent: "The spec says 'validate title length' so I'll add spell-checking too"
Problem: Only implement what's specified
```

---

## 6. SPEC HIERARCHY (Conflict Resolution)

When specs conflict, follow this hierarchy (highest to lowest):

```
1. Constitution      (WHY - Foundational principles)
2. Specify          (WHAT - Requirements)
3. Plan             (HOW - Architecture)
4. Tasks            (BREAKDOWN - Work units)
```

**Example:**
- Constitution says: "No classes allowed"
- Plan says: "Use OOP design pattern"
- **Resolution:** Constitution wins - agent must request plan update

---

## 7. DEVELOPER-AGENT ALIGNMENT

### Collaboration Principles

**Humans and agents collaborate, but the spec is the single source of truth.**

#### Before Every Session
1. Agent reads `.specify/memory/constitution.md`
2. Agent reviews relevant `specs/features/[feature].md`
3. Agent checks `specs/[feature]/plan.md`
4. Agent identifies next task in `specs/[feature]/tasks.md`

#### During Implementation
1. Agent references Task ID in every code block
2. Agent follows plan exactly
3. Agent asks questions if anything is unclear
4. Agent validates against acceptance criteria

#### After Implementation
1. Agent verifies acceptance criteria met
2. Agent documents what was built
3. Agent suggests next task from speckit.tasks
4. Agent updates specs if requirements evolved (with approval)

### Agent-Human Communication

**When Agent Needs Guidance:**
```
"I'm ready to implement [Feature], but I need:
- speckit.specify: Define acceptance criteria for [specific behavior]
- speckit.plan: Clarify how [component X] interacts with [component Y]
- speckit.tasks: Break down the work into atomic tasks

Please provide these before I proceed with implementation."
```

**When Agent Finds Inconsistency:**
```
"I found a conflict:
- speckit.specify §2.1 says: [requirement A]
- speckit.plan §3.4 says: [different approach B]

Please resolve this conflict before I implement."
```

**When Agent Completes Work:**
```
"Task T-003 completed:
✅ All acceptance criteria met
✅ Code references Task ID and specs
✅ Tests passing
✅ No spec violations

Ready for next task: T-004 [description]"
```

---

## 8. QUALITY CHECKLIST FOR AGENTS

Before submitting any code, agents must verify:

- [ ] Task ID referenced in code comments
- [ ] Links to speckit.specify and speckit.plan included
- [ ] No features added beyond specification
- [ ] No architecture changes without plan update
- [ ] All acceptance criteria met
- [ ] Edge cases handled per spec
- [ ] Error messages match spec format
- [ ] No tech stack deviations from constitution
- [ ] Tests written and passing
- [ ] Documentation updated if needed

---

## 9. AGENT SPECIALIZATION (Phase 2 Web App)

### Available Specialized Agents

This project uses specialized agents for different tasks. Each agent has specific responsibilities but **all must follow spec-driven development**.

#### 1. **spec-writer**
- **Purpose:** Create and update specifications
- **Files:** `specs/features/*.md`, `specs/api/*.md`, `specs/database/*.md`
- **Constraints:** Must follow SpecKit Plus templates

#### 2. **fastapi-developer**
- **Purpose:** Implement backend API endpoints
- **Files:** `backend/app/*.py`
- **Constraints:** Must reference specs, use SQLModel, follow FastAPI patterns

#### 3. **nextjs-developer**
- **Purpose:** Implement frontend components and pages
- **Files:** `frontend/src/**/*.tsx`
- **Constraints:** Must use TypeScript, Tailwind CSS, Next.js App Router

#### 4. **auth-specialist**
- **Purpose:** Implement authentication and authorization
- **Files:** `backend/app/auth.py`, `frontend/src/lib/auth.ts`
- **Constraints:** Must use Better Auth, secure patterns

#### 5. **fullstack-architect**
- **Purpose:** Design system architecture and integration
- **Files:** `specs/*/plan.md`
- **Constraints:** Must ensure frontend-backend consistency

**All agents must:**
- Follow the Spec-Kit lifecycle
- Reference Task IDs
- Never improvise features
- Stop if specs are missing

---

## 10. ENFORCEMENT

### How This Document is Enforced

1. **Agent Prompts:** All agents receive this document in their context
2. **Code Review:** Human reviews check for spec references
3. **Quality Gates:** CI/CD validates Task IDs in code
4. **Constitution Check:** Automated checks for principle violations

### What Happens When Agents Violate Rules

1. **Code without Task ID** → Rejected, must add reference
2. **Feature not in spec** → Stopped, must update spec first
3. **Architecture deviation** → Rejected, must update plan
4. **Missing acceptance criteria** → Cannot proceed, must define criteria

---

## 11. PHASE III: AI CHATBOT DEVELOPMENT RULES

### Purpose of Phase III Rules

Phase III adds conversational AI capabilities using OpenAI Agents SDK and Model Context Protocol (MCP) tools. **Stateless architecture is critical** - the chatbot must store all state in the database, never in memory.

**Agents working on Phase III MUST follow these additional rules.**

---

### 1. CHATBOT SPEC-DRIVEN REQUIREMENTS

**Rule:** All chatbot features must be specified before implementation.

#### Required Specifications Before Coding:

**In speckit.specify:**
- ✅ User journey for AI chat interactions
- ✅ MCP tool signatures (all 5 tools with parameters)
- ✅ Natural language understanding requirements
- ✅ AI agent behavior standards
- ✅ Conversation persistence requirements
- ✅ Database schema (conversations, messages tables)

**In speckit.plan:**
- ✅ OpenAI Agent class architecture
- ✅ MCP tools implementation patterns
- ✅ Stateless conversation flow diagrams
- ✅ POST /api/chat/message endpoint design
- ✅ System prompt definition
- ✅ Tool calling orchestration logic

**In speckit.tasks:**
- ✅ Task breakdown for each MCP tool
- ✅ Task for OpenAI Agent implementation
- ✅ Task for conversation persistence
- ✅ Task for chat endpoint
- ✅ Task for frontend chat UI

#### Agent Behavior:

```
❌ FORBIDDEN:
Agent: "I'll implement the chat endpoint..."

✅ REQUIRED:
Agent: "I need to read:
- speckit.specify §5.9 - Conversational Task Creation (Feature 9)
- speckit.plan §4.7 - Chat Message Endpoint
- speckit.tasks T-051 - Implement POST /api/chat/message

All specs found. Proceeding with implementation referencing T-051."
```

---

### 2. STATELESS ARCHITECTURE ENFORCEMENT

**CRITICAL:** The chatbot MUST be stateless. All conversation state MUST be in the database.

#### Stateless Architecture Rules:

**✅ REQUIRED Patterns:**

```python
# CORRECT - Fetch from database every request
@router.post("/api/chat/message")
async def send_chat_message(request: ChatMessageRequest, db: AsyncSession):
    # ALWAYS fetch conversation from database
    conversation = await get_or_create_conversation(db, user_id, request.conversation_id)

    # ALWAYS fetch message history from database
    messages = await get_conversation_messages(db, conversation.id, limit=20)

    # Process with AI agent
    response = await agent.run(messages, user_id)

    # ALWAYS store response in database
    await store_message(db, conversation.id, "assistant", response)

    return response
```

**❌ FORBIDDEN Patterns:**

```python
# WRONG - In-memory state (NEVER DO THIS)
conversation_cache = {}  # ❌ Global state

@router.post("/api/chat/message")
async def send_chat_message(request: ChatMessageRequest):
    # ❌ Storing in memory
    if request.conversation_id not in conversation_cache:
        conversation_cache[request.conversation_id] = []

    # ❌ Using cached state
    history = conversation_cache[request.conversation_id]

    # This breaks stateless architecture!
```

```python
# WRONG - Session-based state (NEVER DO THIS)
from fastapi import Session

sessions = {}  # ❌ Server-side sessions

@router.post("/api/chat/message")
async def send_chat_message(request: ChatMessageRequest, session: Session):
    # ❌ Storing conversation in session
    if "conversation" not in session:
        session["conversation"] = []

    # This breaks horizontal scaling!
```

#### Agent Behavior:

**If agent creates stateful code → STOP and revise:**

```
Agent reviews own code and finds:
conversations = {}  # Global dictionary

Agent MUST:
1. ❌ DELETE the stateful implementation
2. ✅ REWRITE using database-backed pattern
3. ✅ VERIFY all state stored in PostgreSQL
4. ✅ TEST server restart scenario (conversation persists)
```

#### Stateless Validation Checklist:

Before submitting any chat-related code, agent must verify:

- [ ] NO global variables for conversation state
- [ ] NO in-memory caches for messages
- [ ] NO server-side sessions
- [ ] ALL conversation data fetched from database
- [ ] ALL messages stored in database immediately
- [ ] Conversation survives server restart
- [ ] Multiple server instances can handle same conversation

---

### 3. MCP TOOL DEVELOPMENT RULES

**CRITICAL:** MCP tools are the AI agent's interface to the database. **Every tool MUST filter by user_id.**

#### MCP Tool Requirements:

**✅ REQUIRED Pattern:**

```python
async def mcp_add_task(
    user_id: int,        # ✅ ALWAYS first parameter
    title: str,          # Required
    description: str = None,
    priority: str = "medium"
) -> Dict[str, Any]:
    """
    Create a new task. Use when user wants to add a task.

    [Task]: T-052
    [Spec]: speckit.specify §5.9 Feature 9 - Conversational Task Creation
    """
    async with get_db_session() as db:
        task = Task(
            user_id=user_id,  # ✅ CRITICAL: Filter by user
            title=title,
            description=description,
            priority=priority
        )
        db.add(task)
        await db.commit()

        return {
            "success": True,
            "data": {"id": task.id, "title": task.title}
        }


async def mcp_list_tasks(
    user_id: int,            # ✅ ALWAYS first parameter
    status: str = None,
    limit: int = 20
) -> Dict[str, Any]:
    """List user's tasks with optional filters."""
    async with get_db_session() as db:
        query = select(Task).where(
            Task.user_id == user_id  # ✅ CRITICAL: User isolation
        )

        if status == "pending":
            query = query.where(Task.completed == False)

        result = await db.execute(query.limit(limit))
        tasks = result.scalars().all()

        return {
            "success": True,
            "data": {"tasks": [...], "count": len(tasks)}
        }
```

**❌ FORBIDDEN Pattern:**

```python
# WRONG - Missing user_id parameter
async def mcp_add_task(title: str, description: str = None):  # ❌ No user_id!
    task = Task(title=title, description=description)  # ❌ No user isolation!
    # This allows cross-user data leakage!


# WRONG - Not filtering by user_id
async def mcp_list_tasks(user_id: int, status: str = None):
    query = select(Task)  # ❌ No WHERE user_id filter!
    # Returns ALL users' tasks - major security breach!
```

#### MCP Tool Checklist:

Every MCP tool implementation MUST:

- [ ] Accept `user_id: int` as **first parameter**
- [ ] Include `user_id` in ALL database queries (`WHERE user_id = ?`)
- [ ] Be stateless (no global variables)
- [ ] Return structured JSON (`Dict[str, Any]`)
- [ ] Have type hints on all parameters
- [ ] Have clear docstring explaining when to use
- [ ] Handle errors gracefully (return `{"success": False, "error": "..."}`)
- [ ] Reference Task ID in docstring

#### Agent Behavior:

**If agent creates MCP tool without user_id filtering → REJECT:**

```
Agent implements:
async def mcp_list_tasks(status: str = None):  # ❌ No user_id!
    ...

Agent MUST:
1. ❌ STOP implementation immediately
2. ✅ ADD user_id as first parameter
3. ✅ ADD WHERE clause filtering by user_id
4. ✅ VERIFY no cross-user data leakage
5. ✅ TEST with different user_ids
```

---

### 4. OPENAI AGENT INTEGRATION RULES

**Rule:** OpenAI Agent must be integrated according to specifications, not invented patterns.

#### Required Before Implementation:

**In speckit.plan:**
- ✅ OpenAI Agent class structure defined
- ✅ Tool registration pattern specified
- ✅ System prompt defined
- ✅ Multi-turn conversation handling specified
- ✅ Tool calling orchestration logic documented

#### OpenAI Agent Requirements:

**✅ REQUIRED Pattern:**

```python
class OpenAIAgent:
    """
    OpenAI agent with MCP tool calling support.

    [Task]: T-053
    [Spec]: speckit.plan §4.7 - OpenAI Agent Processing
    """

    def __init__(
        self,
        client: AsyncOpenAI,
        system_prompt: str,
        tools: List[Dict[str, Any]]
    ):
        self.client = client
        self.system_prompt = system_prompt
        self.tools = tools
        self.model = "gpt-4o"  # From spec

    async def run(
        self,
        messages: List[Dict[str, str]],
        user_id: int,  # ✅ CRITICAL: Always pass user_id
        max_iterations: int = 5
    ) -> Tuple[str, List[Dict]]:
        """
        Run agent with multi-turn tool calling.

        [Spec]: speckit.plan §4.7 - Multi-turn conversations (max 5 iterations)
        """
        tool_calls_log = []

        for iteration in range(max_iterations):
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools
            )

            message = response.choices[0].message

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_args = json.loads(tool_call.function.arguments)

                    # ✅ CRITICAL: Inject user_id for security
                    tool_args["user_id"] = user_id

                    # Execute MCP tool
                    tool_result = await execute_mcp_tool(
                        tool_call.function.name,
                        tool_args
                    )

                    tool_calls_log.append({...})
                    messages.append({"role": "tool", ...})

                continue  # Continue loop
            else:
                return message.content, tool_calls_log

        # Max iterations reached
        return "I had trouble processing that. Can you simplify?", tool_calls_log
```

#### System Prompt Requirements:

**System prompt MUST be defined in speckit.plan before implementation:**

```python
TODO_ASSISTANT_SYSTEM_PROMPT = """You are a personal TODO assistant...

[Task]: T-054
[Spec]: speckit.plan §4.7 - System Prompt Requirements

Available Tools:
- add_task(user_id, title, ...): Create a new task
- list_tasks(user_id, ...): List tasks
- ... (all 5 tools documented)

Personality:
- Friendly and helpful
- Concise and action-oriented
...

[From]: speckit.plan §6 - AI Agent Behavior Specification
"""
```

#### Agent Behavior:

**If system prompt not in specs → STOP:**

```
Agent: "I need to implement the OpenAI agent, but I cannot find:
- speckit.plan §6 - AI Agent Behavior Specification
- System prompt definition

Please add the system prompt to speckit.plan before I proceed."
```

---

### 5. CONVERSATION PERSISTENCE RULES

**Rule:** Every message (user and assistant) MUST be stored in the database immediately.

#### Conversation Persistence Pattern:

**✅ REQUIRED Implementation:**

```python
@router.post("/api/chat/message")
async def send_chat_message(
    request: ChatMessageRequest,
    db: AsyncSession,
    current_user: User
):
    """
    [Task]: T-051
    [Spec]: speckit.specify §5.14 Feature 14 - Conversation Persistence
    [Plan]: speckit.plan §4.7 - Chat Message Endpoint
    """

    # STEP 1: Get or create conversation (from DB)
    conversation = await get_or_create_conversation(
        db, current_user.id, request.conversation_id
    )

    # STEP 2: Fetch conversation history (from DB, last 20 messages)
    messages_history = await get_conversation_messages(
        db, conversation.id, limit=20
    )

    # STEP 3: ✅ Store user message IMMEDIATELY
    await store_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )

    # STEP 4: Process with AI agent
    message_array = build_message_array(messages_history, request.message)
    ai_response, tool_calls = await agent.run(message_array, current_user.id)

    # STEP 5: ✅ Store assistant response IMMEDIATELY
    await store_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response
    )

    # STEP 6: Return response
    return ChatMessageResponse(
        conversation_id=conversation.id,
        response=ai_response
    )
```

#### Database Operations:

**Store message function MUST:**

```python
async def store_message(
    db: AsyncSession,
    conversation_id: int,
    role: str,  # "user" | "assistant" | "system" | "tool"
    content: str
) -> Message:
    """
    Store a message in the database.

    [Task]: T-055
    [Spec]: speckit.specify §5.14 AC1 - Database Persistence
    """
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    # ✅ Update conversation timestamp
    conversation = await db.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()
    await db.commit()

    return message
```

**Fetch messages function MUST:**

```python
async def get_conversation_messages(
    db: AsyncSession,
    conversation_id: int,
    limit: int = 20
) -> List[Message]:
    """
    Fetch last N messages for conversation.

    [Task]: T-055
    [Spec]: speckit.specify §5.14 AC2 - Conversation Retrieval
    """
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())  # Most recent first
        .limit(limit)
    )
    messages = result.scalars().all()
    return list(reversed(messages))  # Return oldest first for AI context
```

#### Agent Behavior:

**Verify persistence after implementation:**

- [ ] User message stored BEFORE AI processing
- [ ] Assistant response stored AFTER AI completion
- [ ] Timestamps recorded for all messages
- [ ] Conversation updated_at timestamp updated
- [ ] Messages linked to conversation via conversation_id
- [ ] Test: Server restart preserves conversation history
- [ ] Test: Page refresh shows full conversation

---

### 6. PROHIBITED PATTERNS IN PHASE III

**Agents MUST NOT create these patterns. If found in code, STOP and revise.**

#### ❌ PROHIBITED: Stateful Chatbot

```python
# WRONG - Global state
conversations = {}  # ❌ FORBIDDEN

@router.post("/api/chat/message")
async def send_chat_message(request):
    if request.conversation_id not in conversations:
        conversations[request.conversation_id] = []

    # ❌ This breaks stateless architecture
```

**Why prohibited:** Breaks horizontal scaling, loses data on server restart.

---

#### ❌ PROHIBITED: MCP Tools Without user_id

```python
# WRONG - No user_id parameter
async def mcp_add_task(title: str):  # ❌ Missing user_id
    task = Task(title=title)
    # ❌ No user isolation - security breach!
```

**Why prohibited:** Cross-user data leakage, major security vulnerability.

---

#### ❌ PROHIBITED: MCP Tools Without Filtering

```python
# WRONG - No WHERE clause
async def mcp_list_tasks(user_id: int):
    query = select(Task)  # ❌ No .where(Task.user_id == user_id)
    # ❌ Returns all users' tasks!
```

**Why prohibited:** Exposes other users' private data.

---

#### ❌ PROHIBITED: Chat Without Persistence

```python
# WRONG - Not storing messages
@router.post("/api/chat/message")
async def send_chat_message(request):
    response = await agent.run([request.message], user_id)

    # ❌ Not storing user message
    # ❌ Not storing assistant response
    # ❌ Conversation lost on server restart

    return response
```

**Why prohibited:** Conversation doesn't persist, violates specs.

---

#### ❌ PROHIBITED: Global Variables in MCP Server

```python
# WRONG - Global state
task_cache = {}  # ❌ FORBIDDEN

async def mcp_list_tasks(user_id: int):
    if user_id in task_cache:
        return task_cache[user_id]  # ❌ Cached state
```

**Why prohibited:** Breaks stateless architecture, stale data.

---

#### ❌ PROHIBITED: Skipping JWT Auth

```python
# WRONG - No authentication
@router.post("/api/chat/message")
async def send_chat_message(request):  # ❌ No current_user dependency
    # ❌ Anyone can access any conversation
```

**Why prohibited:** Security breach, no user isolation.

---

#### ❌ PROHIBITED: Hardcoded System Prompts

```python
# WRONG - Prompt not in specs
class OpenAIAgent:
    def __init__(self):
        self.system_prompt = "You are a helpful assistant"  # ❌ Invented prompt
        # ❌ Not from speckit.plan
```

**Why prohibited:** Behavior not specified, can't be reviewed.

---

### 7. REQUIRED TESTING FOR CHATBOT

**Agents MUST verify these scenarios before marking implementation complete.**

#### Individual MCP Tool Tests:

```python
# Test each tool in isolation
async def test_mcp_add_task():
    """
    [Task]: T-052
    [Spec]: speckit.specify §5.9 AC2 - MCP Tool Integration
    """
    result = await mcp_add_task(
        user_id=1,
        title="Test task",
        priority="high"
    )

    assert result["success"] == True
    assert result["data"]["id"] is not None
    assert result["data"]["title"] == "Test task"


async def test_mcp_list_tasks_user_isolation():
    """
    [Task]: T-056
    [Spec]: speckit.specify §5.14 AC6 - Authorization
    """
    # Create tasks for user 1
    await mcp_add_task(user_id=1, title="User 1 task")

    # Create tasks for user 2
    await mcp_add_task(user_id=2, title="User 2 task")

    # List tasks for user 1
    result = await mcp_list_tasks(user_id=1)

    # ✅ CRITICAL: User 1 should only see their own tasks
    assert len(result["data"]["tasks"]) == 1
    assert result["data"]["tasks"][0]["title"] == "User 1 task"

    # User 1 should NOT see user 2's tasks
    assert "User 2 task" not in [t["title"] for t in result["data"]["tasks"]]
```

#### Tool Chaining Tests:

```python
async def test_multi_turn_conversation():
    """
    [Task]: T-057
    [Spec]: speckit.specify Journey 4 - Managing Tasks via AI Chatbot
    """
    # User: "Show me my tasks and mark the first one done"

    response = await send_chat_message(
        conversation_id=None,
        message="Show me my tasks and mark the first one done",
        user_id=1
    )

    # Agent should:
    # 1. Call list_tasks(user_id=1)
    # 2. Call complete_task(user_id=1, task_id=first_task_id)

    assert "✅" in response.response
    assert "marked" in response.response.lower()
```

#### Conversation Persistence Tests:

```python
async def test_conversation_persists_across_requests():
    """
    [Task]: T-058
    [Spec]: speckit.specify §5.14 AC3 - Stateless Architecture
    """
    # Request 1: Create task
    response1 = await send_chat_message(
        conversation_id=None,
        message="Add task to buy groceries",
        user_id=1
    )

    conversation_id = response1.conversation_id

    # Request 2: Reference previous task (using context)
    response2 = await send_chat_message(
        conversation_id=conversation_id,
        message="Mark it as done",  # "it" refers to previous task
        user_id=1
    )

    # Agent should understand "it" from conversation history
    assert "✅" in response2.response
    assert "buy groceries" in response2.response.lower()


async def test_conversation_survives_server_restart():
    """
    [Task]: T-059
    [Spec]: speckit.specify §5.14 AC3 - Stateless Architecture
    """
    # Send message
    response = await send_chat_message(
        conversation_id=None,
        message="Add task to finish report",
        user_id=1
    )

    conversation_id = response.conversation_id

    # Simulate server restart (clear all in-memory state)
    # In real code, this would be an actual server restart

    # Fetch conversation history
    messages = await get_conversation_messages(db, conversation_id)

    # ✅ CRITICAL: Conversation must persist
    assert len(messages) >= 2  # User message + assistant response
    assert messages[0].role == "user"
    assert messages[0].content == "Add task to finish report"
    assert messages[1].role == "assistant"
```

#### User Isolation Tests:

```python
async def test_users_cannot_access_other_conversations():
    """
    [Task]: T-060
    [Spec]: speckit.specify §5.14 AC6 - Authorization
    """
    # User 1 creates conversation
    response1 = await send_chat_message(
        conversation_id=None,
        message="Hello",
        user_id=1
    )

    conversation_id = response1.conversation_id

    # User 2 tries to access user 1's conversation
    with pytest.raises(HTTPException) as exc_info:
        await send_chat_message(
            conversation_id=conversation_id,  # User 1's conversation
            message="Hello",
            user_id=2  # ❌ Different user
        )

    # ✅ Should return 403 Forbidden or 404 Not Found
    assert exc_info.value.status_code in [403, 404]
```

#### Agent Behavior Testing Checklist:

Before marking Phase III implementation complete, agent must verify:

- [ ] Each MCP tool tested individually (add, list, update, complete, delete)
- [ ] User isolation tested (user 1 can't access user 2's data)
- [ ] Tool chaining tested (multi-turn conversations work)
- [ ] Conversation persistence tested (survives page refresh)
- [ ] Server restart tested (conversation recovered from DB)
- [ ] Context tracking tested ("it", "that task" references work)
- [ ] Error handling tested (tool failures handled gracefully)
- [ ] JWT auth tested (401 on expired token)
- [ ] Performance tested (< 3 second response time per spec)

---

### Phase III Agent Contract

**By implementing Phase III features, agents agree to:**

1. ✅ **Stateless ALWAYS** - No in-memory conversation state, ever
2. ✅ **user_id ALWAYS first** - Every MCP tool, every database query
3. ✅ **Store EVERYTHING** - User messages, assistant responses, immediately
4. ✅ **Test user isolation** - Verify no cross-user data leakage
5. ✅ **Follow AI specs** - System prompt, tool behavior from speckit.plan
6. ✅ **Test persistence** - Conversation survives server restart
7. ✅ **Reference tasks** - Every line links to Task ID and spec
8. ✅ **STOP if stateful** - Revise immediately if in-memory state created

**Remember:** Phase III stateless architecture is NON-NEGOTIABLE. If an agent creates stateful code, it MUST be rejected and rewritten.

---

## 12. PHASE IV: CONTAINERIZATION & KUBERNETES DEPLOYMENT RULES

### Purpose of Phase IV Rules

Phase IV transitions the application from PaaS deployment (Vercel, Railway) to containerized Kubernetes deployment. **Security, resource management, and operational reliability are critical** - containers must be secure, properly configured, and observable.

**Agents working on Phase IV MUST follow these additional rules.**

---

### 1. DOCKERFILE GENERATION RULES

**Rule:** All Dockerfiles must follow security and optimization best practices.

#### Required Patterns:

**✅ REQUIRED: Multi-Stage Builds**

```dockerfile
# CORRECT - Multi-stage build for optimization
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

**✅ REQUIRED: Official Base Images**

```dockerfile
# CORRECT - Official slim/alpine images
FROM node:20-alpine          # ✅ Alpine for Node.js
FROM python:3.13-slim        # ✅ Slim for Python
FROM nginx:alpine            # ✅ Alpine for Nginx

# WRONG - Non-official or bloated images
FROM ubuntu:latest           # ❌ Too large, not optimized
FROM my-custom-image:latest  # ❌ Not official
```

**✅ REQUIRED: Non-Root User**

```dockerfile
# CORRECT - Run as non-root user
RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 appuser
USER appuser

# WRONG - Running as root
USER root  # ❌ NEVER in production
```

**❌ FORBIDDEN: Secrets in Images**

```dockerfile
# WRONG - Hardcoded secrets
ENV DATABASE_URL=postgresql://user:password@host/db  # ❌ NEVER!
ENV API_KEY=sk-1234567890                            # ❌ NEVER!
COPY .env /app/.env                                  # ❌ NEVER!

# CORRECT - Secrets via runtime injection
ENV DATABASE_URL=""  # ✅ Injected at runtime via K8s Secrets
```

#### Agent Behavior:

**If Dockerfile size > 500MB after build → Optimize:**

```
Agent must:
1. ✅ Use multi-stage builds to separate build and runtime
2. ✅ Use alpine/slim base images
3. ✅ Remove unnecessary files (.git, tests, docs)
4. ✅ Combine RUN commands to reduce layers
5. ✅ Use .dockerignore to exclude large files
```

---

### 2. KUBERNETES MANIFEST RULES

**Rule:** All Kubernetes manifests must be valid, secure, and production-ready.

#### Required Patterns:

**✅ REQUIRED: Resource Requests and Limits**

```yaml
# CORRECT - Always define resources
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: backend
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

# WRONG - No resource definitions
spec:
  containers:
  - name: backend
    # ❌ Missing resources - causes cluster instability!
```

**✅ REQUIRED: Liveness and Readiness Probes**

```yaml
# CORRECT - Always include health probes
containers:
- name: backend
  livenessProbe:
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 30
    periodSeconds: 10
  readinessProbe:
    httpGet:
      path: /ready
      port: 8000
    initialDelaySeconds: 5
    periodSeconds: 5

# WRONG - No health probes
containers:
- name: backend
  # ❌ Missing probes - causes restart loops!
```

**✅ REQUIRED: ConfigMaps for Configuration**

```yaml
# CORRECT - Use ConfigMaps
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
data:
  LOG_LEVEL: "info"
  CORS_ORIGINS: "https://app.example.com"
---
spec:
  containers:
  - name: backend
    envFrom:
    - configMapRef:
        name: backend-config
```

**✅ REQUIRED: Secrets for Sensitive Data**

```yaml
# CORRECT - Use Secrets (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: backend-secrets
type: Opaque
data:
  DATABASE_URL: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0Bob3N0L2Ri
  OPENAI_API_KEY: c2stMTIzNDU2Nzg5MA==
---
spec:
  containers:
  - name: backend
    envFrom:
    - secretRef:
        name: backend-secrets

# WRONG - Secrets in plain text in manifests
env:
- name: DATABASE_URL
  value: "postgresql://user:pass@host/db"  # ❌ NEVER!
```

**✅ REQUIRED: Standard Labels**

```yaml
# CORRECT - Follow Kubernetes labeling best practices
metadata:
  labels:
    app.kubernetes.io/name: todo-backend
    app.kubernetes.io/instance: todo-backend-prod
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: api
    app.kubernetes.io/part-of: todo-app
    app.kubernetes.io/managed-by: helm
```

#### Agent Behavior:

**All manifests MUST pass validation:**

```bash
# Agent must run before committing
kubectl apply --dry-run=client -f manifest.yaml
```

---

### 3. HELM CHART RULES

**Rule:** Helm charts must follow standard structure and be fully parameterized.

#### Required Structure:

```
helm-charts/
├── todo-app/
│   ├── Chart.yaml           # Chart metadata (required)
│   ├── values.yaml          # Default values (required)
│   ├── values-dev.yaml      # Dev environment overrides
│   ├── values-staging.yaml  # Staging environment overrides
│   ├── values-prod.yaml     # Production environment overrides
│   └── templates/
│       ├── _helpers.tpl     # Template helpers
│       ├── deployment.yaml  # Deployment template
│       ├── service.yaml     # Service template
│       ├── configmap.yaml   # ConfigMap template
│       ├── secret.yaml      # Secret template
│       ├── ingress.yaml     # Ingress template
│       └── hpa.yaml         # HorizontalPodAutoscaler
```

**✅ REQUIRED: Parameterized Values**

```yaml
# values.yaml - All configurable values
replicaCount: 2

image:
  repository: todo-backend
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# templates/deployment.yaml - Uses values
spec:
  replicas: {{ .Values.replicaCount }}
  containers:
  - image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    resources:
      {{- toYaml .Values.resources | nindent 12 }}
```

**✅ REQUIRED: Semantic Versioning**

```yaml
# Chart.yaml
apiVersion: v2
name: todo-app
version: 1.0.0        # Chart version (SemVer)
appVersion: "1.0.0"   # Application version
```

#### Agent Behavior:

**If helm install fails → Debug and Fix:**

```bash
# Agent must run these commands
helm lint ./helm-charts/todo-app
helm template ./helm-charts/todo-app --debug
helm install todo-app ./helm-charts/todo-app --dry-run --debug
```

---

### 4. DEPLOYMENT VERIFICATION RULES

**Rule:** Agents MUST verify deployments are healthy before marking tasks complete.

#### Required Verification Steps:

**✅ Step 1: Verify Pods Running**

```bash
# Agent must verify pods reach Running state
kubectl get pods -l app=todo-backend
# Expected: STATUS = Running, READY = 1/1

# If pods not running, check events
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**✅ Step 2: Verify Health Probes Pass**

```bash
# Agent must verify health endpoints respond
kubectl exec <pod-name> -- curl -s http://localhost:8000/health
# Expected: {"status": "healthy"}

kubectl exec <pod-name> -- curl -s http://localhost:8000/ready
# Expected: {"status": "ready"}
```

**✅ Step 3: Verify Services Accessible**

```bash
# Agent must verify service routing
kubectl get svc todo-backend
kubectl port-forward svc/todo-backend 8000:8000

# Test service responds
curl http://localhost:8000/api/health
```

**✅ Step 4: Test End-to-End Application Flow**

```bash
# Agent must verify full application flow
# 1. Frontend loads
# 2. User can register/login
# 3. User can create/list tasks
# 4. AI chatbot responds (Phase III features)
```

#### Agent Behavior:

**If deployment fails → Troubleshoot:**

```
Agent must:
1. ✅ Check pod status: kubectl get pods
2. ✅ Check pod events: kubectl describe pod <name>
3. ✅ Check pod logs: kubectl logs <name>
4. ✅ Check service endpoints: kubectl get endpoints
5. ✅ Check resource quotas: kubectl describe quota
6. ✅ Fix issue and redeploy
7. ✅ Verify fix works
```

---

### 5. AI-OPS TOOL USAGE

**Rule:** When AI-powered Kubernetes tools are available, agents SHOULD use them for enhanced productivity.

#### Docker AI (Gordon)

**When available, use Gordon for:**

```bash
# Dockerfile generation
docker ai "Create a Dockerfile for a FastAPI Python application"

# Image optimization
docker ai "Optimize this Dockerfile for smaller image size"

# Troubleshooting
docker ai "Why is my container failing to start?"
```

#### kubectl-ai

**When available, use kubectl-ai for:**

```bash
# Deployment commands
kubectl-ai "Deploy the todo-backend with 3 replicas"

# Troubleshooting
kubectl-ai "Why are my pods in CrashLoopBackOff?"

# Resource inspection
kubectl-ai "Show me all pods using more than 500Mi memory"
```

#### Kagent

**When available, use Kagent for:**

```bash
# Cluster analysis
kagent analyze cluster

# Resource optimization
kagent optimize deployments

# Cost analysis
kagent cost-report
```

#### Agent Behavior:

```
If AI-Ops tool available:
1. ✅ Use tool for initial generation/analysis
2. ✅ Review and validate output
3. ✅ Ensure output follows AGENTS.md rules
4. ✅ Test before committing

If AI-Ops tool not available:
1. ✅ Use manual kubectl/helm commands
2. ✅ Follow standard Kubernetes practices
3. ✅ Reference official documentation
```

---

### 6. PROHIBITED PATTERNS IN PHASE IV

**Agents MUST NOT create these patterns. If found, STOP and revise.**

#### ❌ PROHIBITED: Hardcoded Secrets in Dockerfiles

```dockerfile
# WRONG - Secrets in Dockerfile
ENV DATABASE_URL=postgresql://user:password@host/db
COPY .env /app/.env
ARG API_KEY=sk-1234567890
```

**Why prohibited:** Secrets exposed in image layers, visible in registry.

---

#### ❌ PROHIBITED: Running Containers as Root

```dockerfile
# WRONG - No USER directive (runs as root)
FROM python:3.13-slim
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
# ❌ Runs as root - security vulnerability!
```

**Why prohibited:** Root access enables container escape attacks.

---

#### ❌ PROHIBITED: Missing Resource Limits

```yaml
# WRONG - No resource limits
spec:
  containers:
  - name: backend
    image: todo-backend:latest
    # ❌ No resources defined - can consume all cluster resources!
```

**Why prohibited:** Causes cluster instability, affects other workloads.

---

#### ❌ PROHIBITED: Missing Health Probes

```yaml
# WRONG - No health probes
spec:
  containers:
  - name: backend
    image: todo-backend:latest
    ports:
    - containerPort: 8000
    # ❌ No liveness/readiness probes - undetected failures!
```

**Why prohibited:** Kubernetes can't detect unhealthy pods, causes cascading failures.

---

#### ❌ PROHIBITED: Imperative kubectl in Production

```bash
# WRONG - Imperative commands
kubectl run backend --image=todo-backend:latest
kubectl expose deployment backend --port=8000
kubectl scale deployment backend --replicas=3
# ❌ Not reproducible, not version controlled!
```

**Why prohibited:** Changes not tracked, can't reproduce environment.

---

#### ❌ PROHIBITED: Development Dependencies in Production

```dockerfile
# WRONG - Dev dependencies in production image
FROM python:3.13-slim
COPY requirements.txt .
RUN pip install -r requirements.txt  # ❌ Includes pytest, black, etc.

# CORRECT - Production only
RUN pip install --no-cache-dir -r requirements-prod.txt
```

**Why prohibited:** Larger image size, potential security vulnerabilities.

---

### 7. REQUIRED TESTING FOR KUBERNETES

**Agents MUST verify these scenarios before marking Phase IV tasks complete.**

#### Docker Image Tests:

```bash
# Test 1: Image builds successfully
docker build -t todo-backend:test .
# Expected: Build completes without errors

# Test 2: Image size is reasonable
docker images todo-backend:test --format "{{.Size}}"
# Expected: < 500MB for backend, < 200MB for frontend

# Test 3: Container runs locally
docker run -d -p 8000:8000 --name test-backend todo-backend:test
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Test 4: Container runs as non-root
docker exec test-backend whoami
# Expected: NOT "root"
```

#### Kubernetes Deployment Tests:

```bash
# Test 1: Pods start successfully
kubectl apply -f manifests/
kubectl wait --for=condition=Ready pod -l app=todo-backend --timeout=120s
# Expected: pod/todo-backend-xxx condition met

# Test 2: Health probes pass
kubectl get pods -l app=todo-backend
# Expected: READY 1/1, STATUS Running

# Test 3: Services accessible
kubectl port-forward svc/todo-backend 8000:8000 &
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Test 4: Logs show no errors
kubectl logs -l app=todo-backend --tail=100
# Expected: No ERROR or CRITICAL logs
```

#### End-to-End Application Tests:

```bash
# Test 1: Frontend loads
curl http://localhost:3000
# Expected: HTML response

# Test 2: API responds
curl http://localhost:8000/api/health
# Expected: {"status": "healthy"}

# Test 3: Authentication works
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'
# Expected: JWT token in response

# Test 4: Full workflow (if AI chatbot enabled)
# - Create user
# - Login
# - Create task via API
# - Create task via chatbot
# - Verify tasks in database
```

#### Agent Testing Checklist:

Before marking Phase IV implementation complete, agent must verify:

- [ ] Docker images build successfully
- [ ] Docker images are optimized (< 500MB backend, < 200MB frontend)
- [ ] Containers run as non-root user
- [ ] No secrets in Docker images
- [ ] Kubernetes manifests pass validation (--dry-run)
- [ ] Pods reach Running state
- [ ] Health probes pass
- [ ] Services are accessible
- [ ] Helm charts lint successfully
- [ ] Helm install works (--dry-run)
- [ ] End-to-end application flow works
- [ ] Logs show no critical errors

---

### Phase IV Agent Contract

**By implementing Phase IV features, agents agree to:**

1. ✅ **Multi-stage builds ALWAYS** - Optimize Docker images
2. ✅ **Non-root users ALWAYS** - Never run containers as root
3. ✅ **No secrets in images** - Use K8s Secrets at runtime
4. ✅ **Resource limits ALWAYS** - Define requests and limits
5. ✅ **Health probes ALWAYS** - Liveness and readiness required
6. ✅ **Declarative YAML only** - No imperative kubectl in production
7. ✅ **Validate before commit** - --dry-run all manifests
8. ✅ **Verify deployments** - Pods running, probes passing
9. ✅ **Test end-to-end** - Full application workflow verified
10. ✅ **Use AI-Ops tools** - When available, for productivity

**Remember:** Phase IV security and reliability practices are NON-NEGOTIABLE. If an agent creates insecure or unreliable configurations, they MUST be rejected and rewritten.

---

## Summary: The Agent Contract

By working on this project, AI agents agree to:

1. ✅ **Read specs first** - Never code without reading relevant specs
2. ✅ **Reference Task IDs** - Every code block links to a task
3. ✅ **Follow the plan** - No creative reinterpretation
4. ✅ **Stop when unclear** - Request clarification, never improvise
5. ✅ **Respect hierarchy** - Constitution > Specify > Plan > Tasks
6. ✅ **Validate completion** - Check acceptance criteria
7. ✅ **Document everything** - Link code to specs
8. ✅ **No freelancing** - Only implement what's specified

**Remember:** In spec-driven development, the agent's job is to **execute the spec perfectly**, not to invent features or architecture.

---

**Project:** Phase II-IV - Full-Stack Web Application with AI Chatbot & Kubernetes Deployment
**Framework:** SpecKit Plus
**Last Updated:** 2026-01-21
**Phase III Critical:** Stateless architecture, user_id filtering, conversation persistence
**Phase IV Critical:** Multi-stage Docker builds, non-root containers, resource limits, health probes
**Compliance:** Mandatory for all AI agents
