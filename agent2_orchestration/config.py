"""
Configuration for Agent 2 Orchestration

All settings loaded from .env or defined as constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class AgentConfig:
    """Centralized configuration for all agents."""

    # LLM Configuration - Gemini 2.5 Flash-Lite
    # For CrewAI with Google Gemini, use 'google/' prefix
    # Available model: gemini-2.5-flash-lite (confirmed from API)
    LLM_MODEL = "google/gemini-2.5-flash-lite"
    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 2048

    # Agent settings
    VERBOSE = True
    ALLOW_DELEGATION = True

    # Pipeline settings
    MAX_ITERATIONS = 10
    RETRY_LIMIT = 3

    # Memory settings
    MEMORY_ENABLED = True
    MEMORY_COLLECTION = "orchestration_memory"

    @classmethod
    def get_llm_config(cls) -> dict:
        """Return LLM configuration dict for CrewAI."""
        return {
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
            "verbose": cls.VERBOSE,
        }
