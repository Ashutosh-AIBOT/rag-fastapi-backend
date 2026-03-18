from rag import retrieve, get_stats

# ─────────────────────────────────────────────────
# TOOLS DEFINITION
# ─────────────────────────────────────────────────

TOOLS = {
    "search_documents": {
        "description": "Search uploaded documents for relevant information",
        "when_to_use" : "when user asks about uploaded files or specific knowledge"
    },
    "direct_answer": {
        "description": "Answer directly from model knowledge",
        "when_to_use" : "for general questions not needing documents"
    },
    "get_db_stats": {
        "description": "Get ChromaDB stats",
        "when_to_use" : "when user asks how many docs are stored"
    }
}

# ─────────────────────────────────────────────────
# DECIDE WHICH TOOL TO USE
# ─────────────────────────────────────────────────

def decide_tool(query: str) -> str:
    """
    Simple keyword based tool routing
    Returns tool name to use
    """
    query_lower = query.lower()

    # stats keywords
    if any(w in query_lower for w in ["how many docs", "stats", "database", "stored"]):
        return "get_db_stats"

    # document search keywords
    doc_keywords = ["according to", "in the document", "from the file",
                    "what does it say", "based on", "uploaded", "pdf", "file"]
    if any(w in query_lower for w in doc_keywords):
        return "search_documents"

    # check if docs exist — if yes, always try RAG first
    stats = get_stats()
    if stats["total_chunks"] > 0:
        return "search_documents"

    return "direct_answer"


# ─────────────────────────────────────────────────
# EXECUTE TOOL
# ─────────────────────────────────────────────────

def execute_tool(tool_name: str, query: str):
    """Run the selected tool and return result"""

    if tool_name == "search_documents":
        chunks = retrieve(query, top_k=3)
        return {
            "tool"   : "search_documents",
            "chunks" : chunks,
            "found"  : len(chunks) > 0
        }

    elif tool_name == "get_db_stats":
        return {
            "tool" : "get_db_stats",
            "stats": get_stats()
        }

    else:
        return {
            "tool"  : "direct_answer",
            "chunks": []
        }
