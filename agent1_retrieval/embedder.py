from google import genai
import chromadb
import os
from dotenv import load_dotenv
import time

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Initialize client - let it use default API version
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chroma_client = chromadb.PersistentClient(path="./chroma_store")

# ✅ CORRECT model name from your debug output
EMBEDDING_MODEL = "models/gemini-embedding-001"

def get_embedding(text: str) -> list[float]:
    """Generate embedding for a single text"""
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

def store_chunks(chunks: list[str], collection_name: str = "research") -> None:
    """Store chunks with embeddings in ChromaDB"""
    # Delete existing collection if it exists
    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass

    # Create new collection
    collection = chroma_client.create_collection(name=collection_name)
    print(f"Embedding and storing {len(chunks)} chunks using model {EMBEDDING_MODEL}...")

    # Store chunks with embeddings
    for i, chunk in enumerate(chunks):
        try:
            embedding = get_embedding(chunk)
            collection.add(
                ids=[f"chunk_{i}"],
                embeddings=[embedding],
                documents=[chunk]
            )
            time.sleep(0.5)  # avoid hitting Gemini rate limits
            if (i + 1) % 10 == 0:
                print(f"  Stored {i+1}/{len(chunks)} chunks")
        except Exception as e:
            print(f"Error processing chunk {i}: {e}")
            continue

    print(f"Done. All {len(chunks)} chunks stored in ChromaDB.")

def retrieve_chunks(query: str, top_k: int = 5, collection_name: str = "research") -> list[str]:
    """Retrieve relevant chunks for a query"""
    collection = chroma_client.get_collection(name=collection_name)
    
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]

# Test the embedding functionality
if __name__ == "__main__":
    # Test a single embedding first
    print("Testing single embedding...")
    test_text = "This is a test sentence."
    try:
        embedding = get_embedding(test_text)
        print(f"✓ Success! Embedding dimension: {len(embedding)}")
        
        # Continue with full storage
        sample_chunks = [
            "Climate change is causing sea levels to rise globally.",
            "Renewable energy sources include solar, wind, and hydro power.",
            "Greenhouse gases trap heat in the atmosphere causing warming.",
            "Electric vehicles reduce carbon emissions from transportation.",
            "Deforestation contributes significantly to carbon dioxide levels.",
        ]
        
        store_chunks(sample_chunks)
        
        query = "what causes global warming?"
        top_chunks = retrieve_chunks(query, top_k=3)
        
        print(f"\nTop chunks for: '{query}'")
        for i, chunk in enumerate(top_chunks):
            print(f"\n{i+1}. {chunk}")
            
    except Exception as e:
        print(f"✗ Error: {e}")