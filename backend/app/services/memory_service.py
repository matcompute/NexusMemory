import os
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import uuid

class MemoryService:
    def __init__(self):
        self.db_path = "./chroma_db"
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Use a high-quality local embedding function (no API cost)
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="nexus_memories",
            embedding_function=self.emb_fn,
            metadata={"hnsw:space": "cosine"} # Use cosine similarity for better semantic matching
        )

    def store_memory(self, content: str, importance: int = 5, tags: list = []):
        """Store a new memory with metadata."""
        memory_id = str(uuid.uuid4())
        self.collection.add(
            documents=[content],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "importance": importance,
                "tags": ",".join(tags)
            }],
            ids=[memory_id]
        )
        return memory_id

    def recall_memories(self, query: str, n_results: int = 5):
        """Retrieve memories based on semantic similarity."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_memories = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_memories.append({
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        return formatted_memories

    def forget_memory(self, memory_id: str):
        """Delete a specific memory."""
        self.collection.delete(ids=[memory_id])
        return True

    def get_stats(self):
        """Get collection statistics."""
        return {
            "count": self.collection.count(),
            "name": "nexus_memories"
        }
