"""
Phase III: OpenAI Agent Integration

This module implements the TodoAgent class for AI-powered task management through natural
language conversations.

ARCHITECTURE:
- Uses AsyncOpenAI client for async API calls
- Integrates with MCP tools for task operations
- Supports multi-turn conversations (max 5 iterations)
- Stateless: All conversation state stored in database
- User isolation: user_id passed to all MCP tools

WORKFLOW:
1. Receive conversation messages from chat endpoint
2. Add system prompt to message array
3. Call OpenAI API with tools (MCP tools)
4. Process tool calls (if any)
5. Execute MCP tools with user_id
6. Add tool results to message array
7. Continue until final response or max iterations
8. Return final assistant response

Author: Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

from typing import List, Dict, Any, Optional
import os

# TODO: Import OpenAI client in AI-BACK-009
# from openai import AsyncOpenAI

# TODO: Import MCP tools in AI-BACK-009
# from app.mcp.server import (
#     add_task, list_tasks, update_task, complete_task, delete_task
# )


# System prompt for TODO assistant
TODO_ASSISTANT_SYSTEM_PROMPT = """
You are a helpful TODO task assistant. You help users manage their tasks through natural language conversations.

Available MCP Tools:
1. add_task(user_id, title, description, priority, tags, due_date) - Create new task
   - Use when user wants to add/create a task
   - Extract details from user's message (title, priority, due date, tags)

2. list_tasks(user_id, status, priority, tags, limit) - Retrieve tasks with filters
   - Use when user wants to see/view/list their tasks
   - Apply filters based on user's request (completed, pending, high priority, etc.)

3. update_task(user_id, task_id, title, description, status, priority) - Update existing task
   - Use when user wants to change/modify a task
   - Only update fields mentioned by user

4. complete_task(user_id, task_id) - Mark task as completed
   - Use when user wants to finish/complete/mark done a task

5. delete_task(user_id, task_id) - Delete task permanently
   - Use when user wants to remove/delete a task
   - Confirm before deleting

Personality:
- Friendly and helpful
- Concise and action-oriented
- Professional but not robotic
- Encouraging for task completion

Response Format:
- Confirm what was done
- Show relevant details
- Offer next steps (optional)
- Use emojis sparingly (✅ ❌ 🎯 📅)

Example Interactions:
User: "Create a task for client presentation tomorrow"
You: "I'll create that for you. ✅

Created: "Client presentation"
- Priority: Medium
- Due: Tomorrow
- Status: Ready

Would you like to set this as high priority or add any notes?"

User: "Show me my high priority tasks"
You: "Here are your high priority tasks: 🎯

1. Client presentation - Due tomorrow
2. Finish Q4 report - Due in 3 days

Both are pending. Want to complete any of these?"
"""


class TodoAgent:
    """
    OpenAI agent for todo task management.

    This class will be fully implemented in AI-BACK-009: Implement OpenAI Agent Class.

    Features:
    - Async OpenAI API integration
    - Multi-turn tool calling (max 5 iterations)
    - MCP tool integration
    - Error handling for API failures
    - Token usage tracking
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TodoAgent with OpenAI API key.

        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)

        Raises:
            ValueError: If API key not provided and not in environment
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable."
            )

        # TODO: Initialize AsyncOpenAI client in AI-BACK-009
        self.client = None
        self.model = "gpt-4o"
        self.tools = []
        self.tool_functions = {}

    async def run(
        self,
        messages: List[Dict[str, str]],
        user_id: int,
        max_iterations: int = 5
    ) -> str:
        """
        Run agent with conversation messages and tool calling.

        This method will be fully implemented in AI-BACK-009.

        Args:
            messages: Conversation message history
            user_id: User ID for tool calls
            max_iterations: Maximum tool calling iterations (default: 5)

        Returns:
            Final assistant response text

        Raises:
            Exception: If OpenAI API call fails
        """
        raise NotImplementedError(
            "TodoAgent.run() will be implemented in AI-BACK-009"
        )


# Singleton instance
_agent_instance: Optional[TodoAgent] = None


def get_agent() -> TodoAgent:
    """
    Get singleton TodoAgent instance.

    This function will be implemented in AI-BACK-009.

    Returns:
        TodoAgent instance

    Raises:
        ValueError: If OPENAI_API_KEY not set
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TodoAgent()
    return _agent_instance


# Export agent getter
__all__ = ["get_agent", "TodoAgent", "TODO_ASSISTANT_SYSTEM_PROMPT"]
