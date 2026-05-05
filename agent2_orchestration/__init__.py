"""
Agent 2 Orchestration Module

Handles CrewAI agent orchestration for the agentic summarizer pipeline.
"""

from .orchestrator import OrchestrationPipeline
from .agents import create_agents
from .config import AgentConfig

__all__ = ["OrchestrationPipeline", "create_agents", "AgentConfig"]
