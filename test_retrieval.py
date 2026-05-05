"""
Test script to verify Agent 1 Retrieval module is working correctly.
Run this before Person 3 connects their module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent1_retrieval'))

from retriever import retrieve

def test_retrieval():
    """Test the full retrieval pipeline."""
    print("=" * 60)
    print("TESTING AGENT 1 RETRIEVAL MODULE")
    print("=" * 60)

    test_queries = [
        "benefits of solar energy",
        "climate change causes",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: '{query}'")
        print(f"{'='*60}")

        try:
            results = retrieve(query, top_k=3)

            if results:
                print(f"\nSUCCESS: Retrieved {len(results)} chunks")
                for i, chunk in enumerate(results[:2], 1):
                    print(f"\n--- Chunk {i} (preview) ---")
                    print(f"{chunk[:200]}..." if len(chunk) > 200 else chunk)
            else:
                print("WARNING: No results returned")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_retrieval()
