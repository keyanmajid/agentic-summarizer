"""
Memory management for Agent 2 Orchestration.

Provides short-term context retention between agent interactions.
"""

import os
from typing import Optional
from datetime import datetime

from .config import AgentConfig


class OrchestrationMemory:
    """
    Manages short-term memory for the orchestration pipeline.

    Stores conversation history, intermediate results, and context
    that agents need to share between tasks.
    """

    def __init__(self, collection_name: Optional[str] = None):
        """
        Initialize orchestration memory.

        Args:
            collection_name: Name for the memory collection
        """
        self.collection_name = collection_name or AgentConfig.MEMORY_COLLECTION
        self._context: dict[str, any] = {}
        self._history: list[dict] = []
        self._created_at = datetime.now()

    def add_context(self, key: str, value: any) -> None:
        """
        Add a piece of context to memory.

        Args:
            key: Context key
            value: Context value (any JSON-serializable type)
        """
        self._context[key] = value
        self._log_event("add_context", key)

    def get_context(self, key: str, default: any = None) -> any:
        """
        Retrieve context by key.

        Args:
            key: Context key
            default: Default value if key not found

        Returns:
            Context value or default
        """
        return self._context.get(key, default)

    def get_all_context(self) -> dict:
        """Return all stored context."""
        return self._context.copy()

    def clear_context(self, key: Optional[str] = None) -> None:
        """
        Clear context.

        Args:
            key: If provided, clear only this key. Otherwise clear all.
        """
        if key:
            self._context.pop(key, None)
        else:
            self._context.clear()

    def add_to_history(
        self,
        agent_role: str,
        action: str,
        result: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """
        Add an event to the history log.

        Args:
            agent_role: Role of the agent that performed the action
            action: Description of the action
            result: Result of the action
            metadata: Optional additional metadata
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "agent_role": agent_role,
            "action": action,
            "result": result[:500] if len(result) > 500 else result,  # Truncate long results
            "metadata": metadata or {},
        }
        self._history.append(event)
        self._log_event("add_to_history", f"{agent_role}: {action}")

    def get_history(
        self, limit: int = 10, agent_role: Optional[str] = None
    ) -> list[dict]:
        """
        Retrieve history entries.

        Args:
            limit: Maximum number of entries to return
            agent_role: If provided, filter to this agent only

        Returns:
            List of history entries
        """
        filtered = self._history
        if agent_role:
            filtered = [h for h in filtered if h["agent_role"] == agent_role]
        return filtered[-limit:]

    def clear_history(self) -> None:
        """Clear all history."""
        self._history.clear()

    def get_summary(self) -> dict:
        """
        Get a summary of the current memory state.

        Returns:
            Dictionary with memory statistics
        """
        return {
            "collection_name": self.collection_name,
            "context_keys": list(self._context.keys()),
            "context_count": len(self._context),
            "history_count": len(self._history),
            "created_at": self._created_at.isoformat(),
        }

    def export_for_agent(self) -> str:
        """
        Export memory contents in a format suitable for agent context.

        Returns:
            Formatted string of memory contents
        """
        lines = ["=== ORCHESTRATION MEMORY ==="]

        if self._context:
            lines.append("CONTEXT:")
            for key, value in self._context.items():
                lines.append(f"  {key}: {value}")

        if self._history:
            lines.append("")
            lines.append("RECENT HISTORY:")
            for event in self._history[-5:]:
                lines.append(
                    f"  [{event['timestamp']}] {event['agent_role']}: {event['action']}"
                )

        lines.append("=== END MEMORY ===")
        return "\n".join(lines)

    def _log_event(self, event_type: str, details: str) -> None:
        """Internal logging for debugging."""
        if AgentConfig.VERBOSE:
            print(f"[Memory] {event_type}: {details}")


# Global memory instance (lazy initialized)
_memory_instance: Optional[OrchestrationMemory] = None


def get_memory() -> OrchestrationMemory:
    """Get or create the global memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = OrchestrationMemory()
    return _memory_instance


def reset_memory() -> None:
    """Reset the global memory instance."""
    global _memory_instance
    _memory_instance = OrchestrationMemory()
