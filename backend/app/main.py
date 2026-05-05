from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from app.services.memory_service import MemoryService
from app.services.compression_service import CompressionService
from app.services.query_service import QueryService

app = FastAPI(title="NexusMemory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_manager = MemoryService()
compressor = CompressionService(memory_manager)
query_expander = QueryService()

class MemoryInput(BaseModel):
    content: str
    importance: int = 5
    tags: List[str] = []

class QueryInput(BaseModel):
    query: str
    limit: int = 5

@app.get("/api/health")
def health():
    return {
        "status": "ok", 
        "stats": memory_manager.get_stats(),
        "engine": "Cognitive Compression Enabled"
    }

@app.post("/api/memories")
def create_memory(item: MemoryInput):
    try:
        memory_id = memory_manager.store_memory(item.content, item.importance, item.tags)
        return {"id": memory_id, "status": "stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recall")
def recall_memories(item: QueryInput):
    try:
        # Phase 2: Enhanced Semantic Bridge (Query Expansion)
        expanded_query = query_expander.expand_query(item.query)
        memories = memory_manager.recall_memories(expanded_query, item.limit)
        return {
            "results": memories, 
            "original_query": item.query,
            "expanded_query": expanded_query
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compress")
def trigger_compression(days: int = 7):
    """Trigger the cognitive compression cycle."""
    try:
        result = compressor.run_compression_cycle(days_old=days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/start")
def initialize_session():
    """Returns a consolidated knowledge snapshot for a new agent session."""
    try:
        # Retrieve the most important 'Core Fragments' and recent memories
        core_memories = memory_manager.recall_memories("Core essential facts and summaries", n_results=5)
        recent_memories = memory_manager.recall_memories("*", n_results=10) # Get latest fragments
        
        return {
            "session_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "snapshot": {
                "core_knowledge": core_memories,
                "recent_history": recent_memories
            },
            "instruction": "Inject these memories into your initial system prompt to resume persistent state."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/memories/{memory_id}")
def delete_memory(memory_id: str):
    try:
        memory_manager.forget_memory(memory_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
