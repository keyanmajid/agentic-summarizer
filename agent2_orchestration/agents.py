"""
Agent definitions for Agent 2 Orchestration.

Uses CrewAI with Gemini 2.5 Flash-Lite model.
"""

from crewai import Agent
from .config import AgentConfig
from .prompts import (
    RESEARCHER_ROLE,
    RESEARCHER_GOAL,
    RESEARCHER_BACKSTORY,
    ORCHESTRATOR_ROLE,
    ORCHESTRATOR_GOAL,
    ORCHESTRATOR_BACKSTORY,
    QUALITY_CONTROLLER_ROLE,
    QUALITY_CONTROLLER_GOAL,
    QUALITY_CONTROLLER_BACKSTORY,
)
from .tools import ContentAnalyzerTool, QualityCheckTool, PipelineStatusTool


def create_agents(verbose: bool = True) -> list[Agent]:
    """
    Create and configure all orchestration agents.

    Args:
        verbose: Enable verbose logging for all agents

    Returns:
        List of configured CrewAI Agent instances
    """
    llm_config = AgentConfig.get_llm_config()
    llm_config["verbose"] = verbose

    # Initialize tools
    content_analyzer = ContentAnalyzerTool()
    quality_check = QualityCheckTool()
    pipeline_status = PipelineStatusTool()

    # ==========================================================================
    # RESEARCHER AGENT
    # ==========================================================================
    researcher = Agent(
        role=RESEARCHER_ROLE.strip(),
        goal=RESEARCHER_GOAL.strip(),
        backstory=RESEARCHER_BACKSTORY.strip(),
        tools=[content_analyzer],
        llm=llm_config["model"],
        verbose=verbose,
        allow_delegation=AgentConfig.ALLOW_DELEGATION,
    )

    # ==========================================================================
    # ORCHESTRATOR AGENT
    # ==========================================================================
    orchestrator = Agent(
        role=ORCHESTRATOR_ROLE.strip(),
        goal=ORCHESTRATOR_GOAL.strip(),
        backstory=ORCHESTRATOR_BACKSTORY.strip(),
        tools=[pipeline_status],
        llm=llm_config["model"],
        verbose=verbose,
        allow_delegation=AgentConfig.ALLOW_DELEGATION,
    )

    # ==========================================================================
    # QUALITY CONTROLLER AGENT
    # ==========================================================================
    quality_controller = Agent(
        role=QUALITY_CONTROLLER_ROLE.strip(),
        goal=QUALITY_CONTROLLER_GOAL.strip(),
        backstory=QUALITY_CONTROLLER_BACKSTORY.strip(),
        tools=[quality_check],
        llm=llm_config["model"],
        verbose=verbose,
        allow_delegation=AgentConfig.ALLOW_DELEGATION,
    )

    return [researcher, orchestrator, quality_controller]


def get_agent_by_role(agents: list[Agent], role_keyword: str) -> Agent | None:
    """
    Find an agent by keyword in its role.

    Args:
        agents: List of agents to search
        role_keyword: Keyword to match in agent role

    Returns:
        Matching agent or None
    """
    for agent in agents:
        if role_keyword.lower() in agent.role.lower():
            return agent
    return None
