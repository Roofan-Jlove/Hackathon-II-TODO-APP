"""
Phase III: MCP (Model Context Protocol) Server

This module implements stateless MCP tools for AI agent interaction with the TODO application.

CRITICAL REQUIREMENTS:
1. Stateless: Tools MUST NOT maintain state between calls
2. user_id First: EVERY tool MUST accept user_id as first parameter
3. Database Filter: EVERY database query MUST filter by user_id
4. Return JSON: Tools MUST return Dict[str, Any], never arbitrary objects
5. Type Hints: All parameters MUST have type hints
6. Clear Descriptions: Docstrings MUST explain WHEN to use the tool
7. Error Handling: Tools MUST handle errors gracefully and return structured errors

MCP Tools:
1. add_task(user_id, title, description, priority, tags, due_date) - Create new task
2. list_tasks(user_id, status, priority, tags, limit) - Retrieve tasks with filters
3. update_task(user_id, task_id, title, description, status, priority) - Update existing task
4. complete_task(user_id, task_id) - Mark task as completed
5. delete_task(user_id, task_id) - Delete task permanently

Author: Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

# MCP SDK imports
from mcp.server import Server
from mcp.types import Tool

# Database imports
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import async_session_maker

# Model imports (for future tool implementations)
from app.models import Task


# Initialize MCP Server
# This server provides stateless tools for the AI agent to manage TODO tasks
mcp_server = Server(name="todo-assistant")


# Database session context manager for MCP tools
@asynccontextmanager
async def get_db_session():
    """
    Get async database session for MCP tools.

    This context manager provides database access for MCP tools while maintaining
    stateless architecture. Each tool call gets a fresh session.

    Yields:
        AsyncSession: SQLModel async database session

    Example:
        async with get_db_session() as db:
            task = Task(user_id=user_id, title="Example")
            db.add(task)
            await db.commit()
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Tool registration dictionary
# Maps tool names to their handler functions
_tool_handlers: Dict[str, callable] = {}


def tool(name: str, description: str, input_schema: Dict[str, Any]):
    """
    Decorator for registering MCP tools.

    This decorator registers a function as an MCP tool that can be called by the AI agent.

    Args:
        name: Tool name (must match function name)
        description: Clear description of when agent should use this tool
        input_schema: JSON Schema describing tool parameters

    Returns:
        Decorator function that registers the tool

    Example:
        @tool(
            name="add_task",
            description="Create a new TODO task when user wants to add a task",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        )
        async def add_task(user_id: str, title: str, description: str = None):
            ...
    """
    def decorator(func: callable):
        # Register tool with MCP server
        tool_obj = Tool(
            name=name,
            description=description,
            inputSchema=input_schema
        )

        # Store handler function
        _tool_handlers[name] = func

        # Return original function (allows normal calling)
        return func

    return decorator


# Tool implementations will be added in tasks AI-BACK-004 through AI-BACK-006:
# - AI-BACK-004: Implement add_task MCP Tool
# - AI-BACK-005: Implement list_tasks, update_task, complete_task MCP Tools
# - AI-BACK-006: Implement delete_task MCP Tool


# Export server instance and utilities
__all__ = ["mcp_server", "get_db_session", "tool", "_tool_handlers"]
