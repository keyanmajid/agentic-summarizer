"""
Agent 3 Summarizer Module

Provides the summarization interface for the agentic summarizer pipeline.
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class SummarizerAgent:
    """
    Summarization agent that processes analyzed content from Agent 2.

    Uses Gemini 2.5 Flash-Lite for efficient, high-quality summarization.
    """

    # LLM Configuration
    MODEL = "gemini-2.5-flash-lite-preview-06-17"
    API_KEY_ENV = "GEMINI_API_KEY"

    def __init__(self, verbose: bool = True):
        """
        Initialize the summarizer agent.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.api_key = os.getenv(self.API_KEY_ENV)

        if not self.api_key:
            raise ValueError(f"API key not found. Set {self.API_KEY_ENV} in .env file.")

        # Initialize Gemini client
        self._client = None

    @property
    def client(self):
        """Lazy-load the Gemini client."""
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def summarize(
        self,
        content: str,
        style: str = "concise",
        max_length: int = 500,
        format: str = "paragraph",
    ) -> str:
        """
        Generate a summary of the provided content.

        Args:
            content: The analyzed content from Agent 2
            style: Summary style - "concise", "detailed", or "bullet"
            max_length: Maximum length in words
            format: Output format - "paragraph" or "markdown"

        Returns:
            Generated summary string
        """
        if self.verbose:
            print(f"[Summarizer] Processing {len(content)} chars...")
            print(f"[Summarizer] Style: {style}, Max length: {max_length} words")

        # Build the prompt based on style
        prompt = self._build_prompt(content, style, max_length, format)

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )

            summary = response.text.strip()

            if self.verbose:
                print(f"[Summarizer] Generated {len(summary)} char summary")

            return summary

        except Exception as e:
            print(f"[Summarizer] Error: {e}")
            raise

    def _build_prompt(
        self, content: str, style: str, max_length: int, format: str
    ) -> str:
        """Build the summarization prompt."""

        style_instructions = {
            "concise": "Provide a concise, focused summary highlighting only the most essential points.",
            "detailed": "Provide a comprehensive summary that covers all key points with supporting details.",
            "bullet": "Provide a bulleted list of key points, each as a complete sentence.",
            "executive": "Provide an executive summary suitable for decision-makers, highlighting implications and key takeaways.",
        }

        format_instructions = {
            "paragraph": "Write in clear, flowing paragraphs.",
            "markdown": "Use markdown formatting with headers, bullet points, and bold text for emphasis.",
        }

        prompt = f"""You are an expert summarizer. Your task is to create a high-quality summary of the following content.

STYLE: {style_instructions.get(style, style_instructions['concise'])}
FORMAT: {format_instructions.get(format, format_instructions['paragraph'])}
MAX LENGTH: Approximately {max_length} words

CONTENT TO SUMMARIZE:
{content}

---
Generate the summary now. Focus on:
1. Capturing the main ideas accurately
2. Maintaining factual integrity
3. Using clear, professional language
4. Preserving any key data points or statistics

SUMMARY:"""

        return prompt

    def summarize_with_context(
        self,
        analyzed_content: str,
        original_query: str,
        style: str = "concise",
    ) -> str:
        """
        Generate a summary that specifically addresses the original query.

        Args:
            analyzed_content: Processed content from Agent 2
            original_query: The user's original question/topic
            style: Summary style

        Returns:
            Query-focused summary
        """
        if self.verbose:
            print(f"[Summarizer] Creating query-focused summary for: '{original_query}'")

        prompt = f"""You are an expert summarizer. Create a summary that directly addresses the query below.

ORIGINAL QUERY: {original_query}

ANALYZED CONTENT:
{analyzed_content}

---
Provide a {style} summary that:
1. Directly answers or addresses the original query
2. Uses evidence from the analyzed content
3. Is well-organized and easy to read
4. Highlights the most relevant information first

SUMMARY:"""

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )
            return response.text.strip()

        except Exception as e:
            print(f"[Summarizer] Error: {e}")
            raise


class SummarizationPipeline:
    """
    High-level pipeline interface for Agent 3.

    Provides a simple interface for end-to-end summarization.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the summarization pipeline.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.summarizer = SummarizerAgent(verbose=verbose)

    def run(
        self,
        analyzed_content: str,
        original_query: Optional[str] = None,
        style: str = "concise",
        max_length: int = 500,
    ) -> dict:
        """
        Run the summarization pipeline.

        Args:
            analyzed_content: Content analyzed by Agent 2
            original_query: Optional original query for context
            style: Summary style
            max_length: Maximum length in words

        Returns:
            Dictionary with summary and metadata
        """
        print("=" * 60)
        print("AGENT 3: SUMMARIZATION PIPELINE")
        print("=" * 60)

        try:
            if original_query:
                summary = self.summarizer.summarize_with_context(
                    analyzed_content=analyzed_content,
                    original_query=original_query,
                    style=style,
                )
            else:
                summary = self.summarizer.summarize(
                    content=analyzed_content,
                    style=style,
                    max_length=max_length,
                )

            result = {
                "success": True,
                "summary": summary,
                "style": style,
                "length": len(summary),
                "metadata": {
                    "input_length": len(analyzed_content),
                    "model": SummarizerAgent.MODEL,
                },
            }

            print(f"\n{'='*60}")
            print("SUMMARY")
            print("=" * 60)
            print(summary)
            print("=" * 60)

            return result

        except Exception as e:
            print(f"[Pipeline Error] {e}")
            return {
                "success": False,
                "summary": "",
                "style": style,
                "length": 0,
                "metadata": {"error": str(e)},
            }


# Convenience function
def summarize(
    content: str,
    query: Optional[str] = None,
    style: str = "concise",
    verbose: bool = True,
) -> str:
    """
    Quick summarization function.

    Args:
        content: Content to summarize
        query: Optional original query
        style: Summary style
        verbose: Enable verbose output

    Returns:
        Summary string
    """
    pipeline = SummarizationPipeline(verbose=verbose)
    result = pipeline.run(
        analyzed_content=content,
        original_query=query,
        style=style,
    )
    return result.get("summary", "") if result.get("success") else ""


# Test function
def test_summarizer():
    """Test the summarizer with sample content."""
    sample_content = """
    Climate change is causing significant global impacts. Rising temperatures
    have led to more frequent extreme weather events including hurricanes,
    droughts, and floods. Scientists overwhelmingly agree that human activities,
    particularly the burning of fossil fuels, are the primary driver of current
    climate change. Greenhouse gases like carbon dioxide and methane trap heat
    in the atmosphere, creating a warming effect. Renewable energy sources such
    as solar and wind power are growing rapidly and becoming cost-competitive
    with fossil fuels. Electric vehicles are increasingly adopted worldwide.
    International agreements like the Paris Accord aim to limit global warming
    to 1.5 degrees Celsius above pre-industrial levels. Adaptation measures are
    being implemented to handle unavoidable climate impacts.
    """

    print("Testing Summarizer Agent...")
    print("=" * 60)

    try:
        pipeline = SummarizationPipeline(verbose=True)
        result = pipeline.run(
            analyzed_content=sample_content,
            original_query="What are the main points about climate change?",
            style="concise",
        )

        if result["success"]:
            print("\n✓ Summarization successful!")
            print(f"\nSummary:\n{result['summary']}")
            return True
        else:
            print("\n✗ Summarization failed")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_summarizer()
    sys.exit(0 if success else 1)
