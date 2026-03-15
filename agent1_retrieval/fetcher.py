import requests
from bs4 import BeautifulSoup
import time

def fetch_page_content(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text

    except Exception as e:
        print(f"  Failed to fetch {url}: {e}")
        return ""


def fetch_all(urls: list[str]) -> list[str]:
    pages = []

    for url in urls:
        print(f"  Fetching: {url}")
        content = fetch_page_content(url)
        if content:
            pages.append(content)
        time.sleep(0.5)

    print(f"\nSuccessfully fetched {len(pages)}/{len(urls)} pages.")
    return pages


if __name__ == "__main__":
    from searcher import search_web

    results = search_web("benefits of solar energy", max_results=3)
    urls = [r["url"] for r in results]
    pages = fetch_all(urls)

    for i, page in enumerate(pages):
        print(f"\n--- Page {i+1} preview ---")
        print(page[:300])