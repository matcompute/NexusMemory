import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.memory_service import MemoryService
from dotenv import load_dotenv

load_dotenv()

class CompressionService:
    def __init__(self, memory_service: MemoryService):
        self.memory_service = memory_service
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=self.api_key,
            temperature=0,
            max_retries=6
        )

    def identify_stale_memories(self, days_old: int = 0) -> List[Dict[str, Any]]:
        """Find all memories that are not already compressed."""
        results = self.memory_service.collection.get(include=['metadatas', 'documents'])
        stale_memories = []
        
        if not results or not results['documents']:
            return []

        for i in range(len(results['documents'])):
            metadata = results['metadatas'][i]
            # Just take everything that isn't already a core fragment
            if metadata.get('type') != 'compressed_core':
                stale_memories.append({
                    "id": results['ids'][i],
                    "content": results['documents'][i],
                    "metadata": metadata
                })
                
        return stale_memories

    def compress_memories(self, memories: List[Dict[str, Any]]) -> str:
        """Synthesize multiple memories into a single core fragment."""
        if not memories:
            return ""

        combined_text = "\n".join([f"- {m['content']}" for m in memories])
        
        prompt = f"""
        You are a Cognitive Compression Engine. Your goal is to synthesize the following granular memory fragments into a single, high-density "Core Memory".
        Retain all important facts, names, dates, and technical details, but remove conversational filler and redundancy.

        Granular Fragments:
        {combined_text}

        Response:
        Provide ONLY the synthesized Core Memory text.
        """
        
        response = self.llm.invoke(prompt)
        content = response.content
        if isinstance(content, list):
            content = " ".join([str(part) for part in content])
        return content.strip()

    def run_compression_cycle(self, days_old: int = 0):
        """Perform the full identification and compression loop."""
        stale = self.identify_stale_memories(days_old)
        
        if not stale:
            return {"status": "skipped", "message": "No memories found to compress."}

        # Compress (even if only 1 fragment, just to prove it works)
        core_content = self.compress_memories(stale)
        
        # Store new core memory
        tags = list(set([tag for m in stale for tag in m['metadata'].get('tags', '').split(',') if tag]))
        tags.append("compressed-core")
        
        self.memory_service.store_memory(
            content=core_content,
            importance=9, # Compressed memories are usually high importance
            tags=tags
        )
        
        # Mark as compressed (in this version we'll just delete the old ones to save space as per user's request)
        for m in stale:
            self.memory_service.forget_memory(m['id'])
            
        return {
            "status": "success", 
            "fragments_compressed": len(stale),
            "new_core_fragment": core_content[:100] + "..."
        }
