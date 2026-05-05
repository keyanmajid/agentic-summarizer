import sys
import os

# Allow imports from the same folder - must be BEFORE any other imports
agent1_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, agent1_dir)

from searcher import search_web
from fetcher import fetch_all
# Import local chunker module explicitly to avoid conflict with pip package
import importlib.util
chunker_spec = importlib.util.spec_from_file_location("local_chunker", os.path.join(agent1_dir, "Chunker.py"))
local_chunker = importlib.util.module_from_spec(chunker_spec)
chunker_spec.loader.exec_module(local_chunker)
chunk_texts = local_chunker.chunk_texts

from embedder import store_chunks, retrieve_chunks


def retrieve(query: str, top_k: int = 5) -> list[str]:
    """
    ─────────────────────────────────────────────────────
    MAIN FUNCTION — Person 2 calls this.

    Input : a topic/query string
    Output: list of most relevant text chunks

    Pipeline:
      1. Search DuckDuckGo for the query
      2. Fetch full content from each result URL
      3. Split content into chunks
      4. Embed chunks and store in ChromaDB
      5. Return the most relevant chunks
    ─────────────────────────────────────────────────────
    """
    print(f"\n[Agent 1] Starting retrieval for: '{query}'")

    # Step 1: Search
    results = search_web(query, max_results=5)
    if not results:
        print("[Agent 1] No search results found.")
        return []

    # Step 2: Fetch full page content
    urls = [r["url"] for r in results]
    pages = fetch_all(urls)
    if not pages:
        print("[Agent 1] Could not fetch any pages.")
        return []

    # Step 3: Chunk the pages
    chunks = chunk_texts(pages)
    if not chunks:
        print("[Agent 1] No chunks generated.")
        return []

    # Step 4: Embed and store in ChromaDB
    store_chunks(chunks, collection_name="research")

    # Step 5: Retrieve most relevant chunks
    top_chunks = retrieve_chunks(query, top_k=top_k, collection_name="research")

    print(f"[Agent 1] Done. Returning {len(top_chunks)} chunks.\n")
    return top_chunks


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    results = retrieve("benefits of solar energy", top_k=5)

    print("\n=== FINAL OUTPUT ===")
    for i, chunk in enumerate(results):
        print(f"\nChunk {i+1}:\n{chunk}")