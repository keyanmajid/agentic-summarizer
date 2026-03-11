from ddgs import DDGS
import time

def search_web(query: str, max_results: int = 5, retries: int = 3) -> list[dict]:
    """
    Search DuckDuckGo for a query.
    Retries up to 3 times if DuckDuckGo blocks the request.
    """
    for attempt in range(retries):
        try:
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title":   result.get("title", ""),
                        "url":     result.get("href", ""),
                        "snippet": result.get("body", "")
                    })
            return results

        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    print("  Search failed after all retries.")
    return []


if __name__ == "__main__":
    results = search_web("benefits of solar energy", max_results=3)
    for i, r in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"  Title   : {r['title']}")
        print(f"  URL     : {r['url']}")
        print(f"  Snippet : {r['snippet'][:100]}...")