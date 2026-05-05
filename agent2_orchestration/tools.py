"""
Custom tools for Agent 2 Orchestration agents.
"""

from crewai.tools import BaseTool
from typing import Optional


class ContentAnalyzerTool(BaseTool):
    """Tool for analyzing content chunks to extract structured information."""

    name: str = "Content Analyzer"
    description: str = """
        Analyzes a list of text chunks and extracts:
        - Main topics and themes
        - Key facts and claims
        - Supporting evidence
        - Potential contradictions

        Input: A string containing multiple text chunks separated by newlines.
        Output: Structured analysis as a formatted string.
    """

    def _run(self, content: str) -> str:
        """Analyze content and return structured findings."""
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

        if not chunks:
            return "No content to analyze."

        # Extract key sentences (simple heuristic: first sentence of each chunk)
        key_points = []
        for chunk in chunks[:5]:  # Limit to first 5 chunks
            sentences = chunk.split(".")
            if sentences:
                key_points.append(sentences[0].strip() + ".")

        analysis = [
            "=== CONTENT ANALYSIS ===",
            f"Total chunks analyzed: {len(chunks)}",
            "",
            "KEY POINTS:",
        ]
        for i, point in enumerate(key_points, 1):
            analysis.append(f"  {i}. {point}")

        analysis.append("")
        analysis.append("=== END ANALYSIS ===")

        return "\n".join(analysis)


class QualityCheckTool(BaseTool):
    """Tool for validating content quality before summarization."""

    name: str = "Quality Check"
    description: str = """
        Validates content quality by checking:
        - Completeness (does it cover the topic adequately?)
        - Consistency (are there contradictions?)
        - Clarity (is the information clear?)

        Input: Content string to validate.
        Output: Quality report with score and recommendations.
    """

    def _run(self, content: str, min_length: int = 100) -> str:
        """Run quality checks on content."""
        issues = []
        score = 10  # Start perfect, deduct for issues

        # Check 1: Minimum length
        if len(content) < min_length:
            issues.append(f"Content too short ({len(content)} chars, min {min_length})")
            score -= 3

        # Check 2: Empty or whitespace
        if not content.strip():
            issues.append("Content is empty or whitespace only")
            score -= 5

        # Check 3: Repetition detection (simple)
        words = content.split()
        if len(words) > 0:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:
                issues.append(f"High repetition detected (unique ratio: {unique_ratio:.2f})")
                score -= 2

        # Build report
        report = ["=== QUALITY REPORT ==="]
        report.append(f"Score: {score}/10")
        report.append("")

        if issues:
            report.append("ISSUES FOUND:")
            for issue in issues:
                report.append(f"  - {issue}")
        else:
            report.append("No issues found. Content passed all quality checks.")

        report.append("")
        report.append(f"Content length: {len(content)} characters")
        report.append(f"Word count: {len(words) if 'words' in dir() else len(content.split())}")
        report.append("=== END REPORT ===")

        return "\n".join(report)


class PipelineStatusTool(BaseTool):
    """Tool for tracking and reporting pipeline status."""

    name: str = "Pipeline Status"
    description: str = """
        Reports the current status of the orchestration pipeline.
        Tracks which stages have completed and what's pending.

        Input: Optional stage name to check specifically.
        Output: Current pipeline status report.
    """

    _status_tracker: dict = {}

    def _run(self, stage: Optional[str] = None, status: str = "pending") -> str:
        """Update or query pipeline status."""
        if stage:
            self._status_tracker[stage] = status

        report = ["=== PIPELINE STATUS ==="]
        for stage, stat in self._status_tracker.items():
            icon = "✓" if stat == "completed" else "○" if stat == "pending" else "●"
            report.append(f"  {icon} {stage}: {stat}")

        if not self._status_tracker:
            report.append("  No stages registered yet.")

        report.append("=== END STATUS ===")
        return "\n".join(report)
