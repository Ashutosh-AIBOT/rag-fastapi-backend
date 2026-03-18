import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chromadb")
EMBED_MODEL = "all-MiniLM-L6-v2"

# load once
embedder      = SentenceTransformer(EMBED_MODEL)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection    = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)


def chunk_text(text: str, size: int = 500, overlap: int = 50) -> List[str]:
    words  = text.split()
    chunks = []
    start  = 0
    while start < len(words):
        chunks.append(" ".join(words[start:start + size]))
        start += size - overlap
    return chunks


def add_document(text: str, doc_id: str, metadata: dict = {}) -> dict:
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        collection.upsert(
            ids        = [f"{doc_id}_{i}"],
            documents  = [chunk],
            embeddings = [embedder.encode(chunk).tolist()],
            metadatas  = [{**metadata, "chunk": i, "doc_id": doc_id}]
        )
    return {"chunks_added": len(chunks), "doc_id": doc_id}


def retrieve(query: str, top_k: int = 3) -> List[str]:
    if collection.count() == 0:
        return []
    results = collection.query(
        query_embeddings=[embedder.encode(query).tolist()],
        n_results=min(top_k, collection.count())
    )
    return results["documents"][0] if results["documents"] else []


def build_rag_prompt(query: str, chunks: List[str]) -> str:
    if not chunks:
        return query
    context = "\n\n".join(chunks)
    return f"""Use the context below to answer the question.
If context doesn't help, answer from your own knowledge.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""


def get_stats() -> dict:
    return {
        "total_chunks": collection.count(),
        "embed_model" : EMBED_MODEL
    }