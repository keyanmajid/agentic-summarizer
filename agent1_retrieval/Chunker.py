from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_texts(pages: list[str], chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    Takes a list of raw page text strings and splits them into smaller chunks.

    chunk_size    = max characters per chunk (500 is a good default)
    chunk_overlap = how many characters overlap between chunks
                    (overlap helps avoid losing context at chunk boundaries)

    Returns a flat list of all chunks across all pages.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]  # tries to split on these in order
    )

    all_chunks = []
    for page in pages:
        chunks = splitter.split_text(page)
        all_chunks.extend(chunks)

    # Remove empty or very short chunks (less than 50 chars, not useful)
    all_chunks = [c.strip() for c in all_chunks if len(c.strip()) > 50]

    print(f"Created {len(all_chunks)} chunks from {len(pages)} pages.")
    return all_chunks


# ── Quick test ────────────────────────────────────────────────
if __name__ == "__main__":
    sample_pages = [
        "Climate change is a long-term shift in global temperatures and weather patterns. "
        "While natural factors have influenced climate in the past, since the 1800s human activities "
        "have been the main driver of climate change. Burning fossil fuels like coal, oil and gas "
        "generates greenhouse gas emissions that act like a blanket wrapped around the Earth, "
        "trapping the sun's heat and raising temperatures. Examples of greenhouse gas emissions "
        "include carbon dioxide and methane. These come from using petrol to drive a car or coal "
        "to heat a building. Clearing land and forests can also release carbon dioxide. Agriculture, "
        "oil and gas operations are major sources of methane emissions."
    ]

    chunks = chunk_texts(sample_pages)
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:\n{chunk}")