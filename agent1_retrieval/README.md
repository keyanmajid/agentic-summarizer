# Agent 1 — Data & Retrieval Module

## What this module does
Takes a topic/query → searches the web → fetches pages → chunks text →
embeds with Gemini → stores in ChromaDB → returns the most relevant chunks.

---

## How to use it (Person 2, this is for you)

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Make sure .env exists in the root folder with:
```
GEMINI_API_KEY=your_key_here
```

### 3. Import and call this one function:
```python
from agent1_retrieval.retriever import retrieve

chunks = retrieve("climate change effects", top_k=5)
print(chunks)  # returns a list of strings
```

---

## Input
| Parameter | Type | Default | Description |
|---|---|---|---|
| query | str | required | The topic to search for |
| top_k | int | 5 | Number of chunks to return |

## Output
A list of strings. Each string is a relevant text chunk.

```python
[
  "Solar energy reduces electricity bills significantly...",
  "Installing solar panels increases home value by...",
  ...
]
```

---

## Files
| File | Job |
|---|---|
| searcher.py | Searches DuckDuckGo |
| fetcher.py | Fetches full page content from URLs |
| chunker.py | Splits text into 500 char chunks |
| embedder.py | Embeds chunks with Gemini + stores in ChromaDB |
| retriever.py | Main function — ties everything together |

---

## AI Prompt for Person 2
> Copy and paste this entire prompt to your AI at the start of your first message.

```
I am working on a Multi-Agent Research Summarizer project as Person 2
(Orchestration & Logic). Here is the full context:

## Project Overview
User enters a topic → Agent 1 searches web & retrieves relevant chunks →
Agent 2 orchestrates the pipeline → Agent 3 summarizes and displays the report.

## Tech Stack
- Language: Python
- LLM: Gemini 2.5 Flash-Lite (free tier)
- Agent Framework: CrewAI + LangChain
- Vector DB: ChromaDB (local)
- Embeddings: Gemini Embeddings API (models/gemini-embedding-001)
- Search: DuckDuckGo (ddgs Python library)
- UI: Streamlit (Person 3 builds this)
- All APIs are free — only one API key needed: GEMINI_API_KEY

## Folder Structure
/agentic-summarizer
  ├── agent1_retrieval/      ← Person 1 (DONE)
  ├── agent2_orchestration/  ← My folder (Person 2)
  ├── agent3_summarizer/     ← Person 3 (not started)
  ├── shared/
  ├── app.py
  ├── .env                   ← contains GEMINI_API_KEY
  └── requirements.txt

## What Person 1 (Agent 1) has already built
All files are inside agent1_retrieval/:

- searcher.py  → searches DuckDuckGo using ddgs library
- fetcher.py   → visits each URL and returns full page text using requests + BeautifulSoup
- chunker.py   → splits pages into 500 char chunks using langchain_text_splitters
- embedder.py  → embeds chunks using Gemini API (models/gemini-embedding-001)
                 and stores in ChromaDB locally
- retriever.py → the MAIN function that ties everything together

## How to call Agent 1 (the only function Person 2 needs):
from agent1_retrieval.retriever import retrieve

chunks = retrieve("any topic here", top_k=5)
# returns: list of strings (most relevant text chunks)

## What Person 3 (Agent 3) will build (not done yet):
from agent3_summarizer.summarizer import summarize

report = summarize(chunks, "any topic here")
# returns: a structured report string (intro, findings, conclusion)

## My job as Person 2:
1. Define agent roles and system prompts
2. Build orchestration flow using CrewAI
3. Wire retrieve() and summarize() together
4. Add memory so agents remember earlier steps
5. Handle errors and retries

## Important notes:
- Use google-genai library (NOT google-generativeai, it is deprecated)
- Gemini free tier: 15 requests/minute, 1000 requests/day
- Add time.sleep(1) between LLM calls to avoid rate limits
- .env is in the root folder, not inside agent2_orchestration/
- Load it with: load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

Help me build my agent2_orchestration module step by step,
one file at a time, so I can understand what is happening and find errors easily.
```