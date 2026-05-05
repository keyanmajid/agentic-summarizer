"""
Main orchestration pipeline for Agent 2.

Coordinates the flow of information between agents and Agent 3.
"""

import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Task, Crew, Process
from .config import AgentConfig
from .agents import create_agents, get_agent_by_role
from .memory import get_memory, reset_memory
from .prompts import PIPELINE_INTRO, HANDOFF_TO_SUMMARIZER


class OrchestrationPipeline:
    """
    Main pipeline class for Agent 2 orchestration.

    Coordinates the multi-agent analysis workflow and hands off to Agent 3.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the orchestration pipeline.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.agents = create_agents(verbose=verbose)
        self.memory = get_memory()
        self._crew: Optional[Crew] = None

    def _build_crew(self, content: str) -> Crew:
        """Build the CrewAI crew with tasks."""
        researcher = get_agent_by_role(self.agents, "Research")
        orchestrator = get_agent_by_role(self.agents, "Coordinator")
        quality_controller = get_agent_by_role(self.agents, "Quality")

        if not all([researcher, orchestrator, quality_controller]):
            raise RuntimeError("Failed to create all required agents")

        # =========================================================================
        # TASK 1: Research Analysis
        # =========================================================================
        research_task = Task(
            name="research_analysis",
            description=f"""
Analyze the provided content chunks:
1. Identify the main topic and up to 3 subtopics
2. Extract 5-10 key facts or claims
3. Note any contradictions or gaps
4. Organize findings by theme

Content to analyze:
{content}
""",
            expected_output="""
A structured analysis containing:
- Main topic identification
- List of key facts/claims
- Any noted contradictions or gaps
- Thematic organization of findings
""",
            agent=researcher,
        )

        # =========================================================================
        # TASK 2: Quality Validation
        # =========================================================================
        quality_task = Task(
            name="quality_validation",
            description="""
Review the research analysis for quality:
1. Verify completeness - are all key aspects covered?
2. Check for factual consistency
3. Identify any missing context
4. Provide a quality score (1-10) with justification
""",
            expected_output="""
A quality report containing:
- Completeness assessment
- Consistency check results
- Missing context (if any)
- Quality score (1-10) with justification
""",
            agent=quality_controller,
            context=[research_task],
        )

        # =========================================================================
        # TASK 3: Orchestration & Handoff Prep
        # =========================================================================
        orchestration_task = Task(
            name="orchestration_handoff",
            description="""
Prepare the analyzed content for handoff to summarization:
1. Review the research analysis and quality report
2. Determine if quality is sufficient (score >= 7)
3. If not sufficient, request re-analysis
4. If sufficient, prepare final handoff package
""",
            expected_output="""
Either:
A) If quality is insufficient: A request for re-analysis with specific improvements needed.
B) If quality is sufficient: A handoff package containing the finalized content ready for summarization.
""",
            agent=orchestrator,
            context=[research_task, quality_task],
        )

        # Create the crew
        crew = Crew(
            agents=self.agents,
            tasks=[research_task, quality_task, orchestration_task],
            process=Process.sequential,
            verbose=self.verbose,
        )

        return crew

    def run(self, content: str) -> dict:
        """
        Run the full orchestration pipeline.

        Args:
            content: Raw content chunks from Agent 1 (newline-separated)

        Returns:
            Dictionary with:
            - success: bool indicating if pipeline completed
            - analyzed_content: str of analyzed content for Agent 3
            - quality_score: int 1-10
            - notes: any relevant notes from the pipeline
        """
        print(PIPELINE_INTRO)

        # Reset memory for fresh run
        reset_memory()
        self.memory.add_context("input_length", len(content))

        # Build crew fresh for each run
        self._crew = self._build_crew(content)

        try:
            # Run the pipeline
            result = self._crew.kickoff()

            # Store result in memory
            self.memory.add_context("pipeline_status", "completed")
            self.memory.add_context("output", str(result)[:1000])

            # Parse result for handoff
            output = {
                "success": True,
                "analyzed_content": str(result),
                "quality_score": 8,  # Default if not specified
                "notes": "Pipeline completed successfully",
                "memory_summary": self.memory.get_summary(),
            }

            print(HANDOFF_TO_SUMMARIZER)
            return output

        except Exception as e:
            self.memory.add_context("pipeline_status", "failed")
            print(f"[Pipeline Error] {e}")
            return {
                "success": False,
                "analyzed_content": "",
                "quality_score": 0,
                "notes": f"Pipeline failed: {str(e)}",
            }

    def run_incremental(
        self, content: str, stage: str = "full"
    ) -> dict:
        """
        Run a specific stage of the pipeline (for debugging/testing).

        Args:
            content: Input content
            stage: Which stage to run ("research", "quality", "orchestration", "full")

        Returns:
            Stage-specific output dictionary
        """
        if stage == "full":
            return self.run(content)

        # For incremental runs, we'd need to modify task dependencies
        # This is a simplified version for testing
        print(f"[Pipeline] Running incremental stage: {stage}")
        return self.run(content)


# Convenience function for direct pipeline access
def run_orchestration(content: str, verbose: bool = True) -> dict:
    """
    Run the orchestration pipeline with the given content.

    Args:
        content: Raw content from Agent 1
        verbose: Enable verbose output

    Returns:
        Pipeline result dictionary
    """
    pipeline = OrchestrationPipeline(verbose=verbose)
    return pipeline.run(content)
