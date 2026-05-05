"""
Test script for Agent 2 Orchestration pipeline.

Run this to verify the orchestration module works before connecting to Agent 1 and Agent 3.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent2_orchestration.orchestrator import OrchestrationPipeline, run_orchestration
from agent2_orchestration.agents import create_agents
from agent2_orchestration.config import AgentConfig


def test_agent_creation():
    """Test that agents are created successfully."""
    print("=" * 60)
    print("TEST 1: Agent Creation")
    print("=" * 60)

    try:
        agents = create_agents(verbose=True)
        print(f"[PASS] Created {len(agents)} agents:")
        for agent in agents:
            print(f"  - {agent.role[:50]}...")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to create agents: {e}")
        return False


def test_config():
    """Test configuration loading."""
    print("\n" + "=" * 60)
    print("TEST 2: Configuration")
    print("=" * 60)

    print(f"LLM Model: {AgentConfig.LLM_MODEL}")
    print(f"Temperature: {AgentConfig.LLM_TEMPERATURE}")
    print(f"Verbose: {AgentConfig.VERBOSE}")
    print(f"Memory Enabled: {AgentConfig.MEMORY_ENABLED}")
    print("[PASS] Configuration loaded")
    return True


def test_pipeline_with_sample_content():
    """Test the full pipeline with sample content."""
    print("\n" + "=" * 60)
    print("TEST 3: Full Pipeline Run")
    print("=" * 60)

    sample_content = """
Climate change is causing significant impacts globally.
Rising temperatures have led to more frequent extreme weather events.
Scientists agree that human activities are the primary cause.
Greenhouse gas emissions from fossil fuels trap heat in the atmosphere.
Renewable energy sources like solar and wind are growing rapidly.
Electric vehicles are becoming more affordable and popular.
Governments worldwide are implementing carbon reduction policies.
The Paris Agreement aims to limit warming to 1.5 degrees Celsius.
Adaptation strategies are needed for unavoidable climate impacts.
Sea level rise threatens coastal communities worldwide.
"""

    try:
        pipeline = OrchestrationPipeline(verbose=True)
        result = pipeline.run(sample_content)

        print("\n--- Pipeline Result ---")
        print(f"Success: {result['success']}")
        print(f"Quality Score: {result['quality_score']}")
        print(f"Notes: {result['notes']}")
        print(f"Output length: {len(result['analyzed_content'])} chars")

        if result['success']:
            print("[PASS] Pipeline completed successfully")
            return True
        else:
            print("[FAIL] Pipeline failed")
            return False

    except Exception as e:
        print(f"[FAIL] Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_memory():
    """Test memory functionality."""
    print("\n" + "=" * 60)
    print("TEST 4: Memory System")
    print("=" * 60)

    from agent2_orchestration.memory import get_memory, reset_memory

    try:
        reset_memory()
        memory = get_memory()

        memory.add_context("test_key", "test_value")
        value = memory.get_context("test_key")
        assert value == "test_value", f"Expected 'test_value', got {value}"

        memory.add_to_history("TestAgent", "test_action", "test_result")
        history = memory.get_history()
        assert len(history) == 1, f"Expected 1 history entry, got {len(history)}"

        print(f"Memory summary: {memory.get_summary()}")
        print("[PASS] Memory system working")
        return True

    except Exception as e:
        print(f"[FAIL] Memory error: {e}")
        return False


def test_tools():
    """Test custom tools."""
    print("\n" + "=" * 60)
    print("TEST 5: Custom Tools")
    print("=" * 60)

    from agent2_orchestration.tools import ContentAnalyzerTool, QualityCheckTool

    try:
        # Test Content Analyzer
        analyzer = ContentAnalyzerTool()
        result = analyzer._run("Sample content chunk.\n\nAnother chunk here.")
        assert "CONTENT ANALYSIS" in result
        print("[PASS] ContentAnalyzerTool working")

        # Test Quality Check
        checker = QualityCheckTool()
        result = checker._run("This is some test content to validate.")
        assert "QUALITY REPORT" in result
        print("[PASS] QualityCheckTool working")

        return True

    except Exception as e:
        print(f"[FAIL] Tool error: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 60)
    print("AGENT 2 ORCHESTRATION - TEST SUITE")
    print("=" * 60)
    print(f"LLM Model: {AgentConfig.LLM_MODEL}")
    print(f"Verbose: {AgentConfig.VERBOSE}")
    print("=" * 60)

    tests = [
        ("Config", test_config),
        ("Agent Creation", test_agent_creation),
        ("Memory", test_memory),
        ("Tools", test_tools),
        ("Full Pipeline", test_pipeline_with_sample_content),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n[FAIL] {name} crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "[PASS] PASS" if result else "[FAIL] FAIL"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
