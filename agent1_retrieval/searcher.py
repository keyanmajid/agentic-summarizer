from ddgs import DDGS

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search DuckDuckGo for a query.
    Returns a list of results, each with a title, url, and snippet.
    """
    results = []

    with DDGS() as ddgs:
        for result in ddgs.text(query, max_results=max_results):
            results.append({
                "title":   result.get("title", ""),
                "url":     result.get("href", ""),
                "snippet": result.get("body", "")
            })

    return results


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    results = search_web("benefits of solar energy", max_results=3)

    for i, r in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"  Title   : {r['title']}")
        print(f"  URL     : {r['url']}")
        print(f"  Snippet : {r['snippet'][:100]}...")