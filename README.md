# 🧠 NexusMemory: The Infinite Context Engine

NexusMemory is a high-performance **Cognitive Memory Layer** designed to solve the "Infinite Context" problem in autonomous agent systems. It acts as an external middleware that gives agents a persistent "Brain" to recall conversations and data from months ago.

---

## 🚀 Key Features

- **Semantic Recall**: Concept-based retrieval using ChromaDB and Sentence-Transformers. Understands the difference between keywords and intent.
- **Cognitive Compression**: An intelligent background engine that synthesizes granular, old memories into high-density "Core Fragments" using Gemini 1.5 Flash.
- **Cross-Session Persistence**: Maintains state across restarts, allowing agents to resume complex workflows with full contextual awareness.
- **Memory Management**: Full CRUD capabilities for memories with importance-based weighting and tagging.

---

## 🛠️ Tech Stack

- **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Persistent Vector Store)
- **Engine**: [Google Gemini 1.5 Flash](https://aistudio.google.com/) (for Synthesis & Summarization)
- **Embeddings**: `all-MiniLM-L6-v2` (Local, High-Performance)
- **Backend**: FastAPI
- **Frontend**: React (Vite, TypeScript, Lucide-React)

---

## 📂 Project Structure

```text
NexusMemory/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── memory_service.py      # Vector Store Operations
│   │   │   └── compression_service.py # Cognitive Synthesis Logic
│   │   └── main.py                    # API Entry Point
│   └── chroma_db/                     # Local Vector Database
├── frontend/
│   ├── src/
│   │   └── pages/
│   │       └── MemoryPage.tsx         # Cognitive Dashboard
│   └── package.json
└── IMPLEMENTATION_PLAN.md             # The Roadmap
```

---

## ⚙️ How it Works: Cognitive Compression

1. **Detection**: The system identifies fragments that are older than a set threshold.
2. **Synthesis**: Related fragments are sent to the Gemini 1.5 Flash engine.
3. **Encoding**: Gemini compresses the granular data into a single "Core Memory" while retaining all critical facts.
4. **Archival**: The original granular fragments are removed, leaving a lean, high-density knowledge base.

---

*This project is part of a Senior AI/ML Portfolio by **Mulat Ayinet Tiruye**, demonstrating mastery in Agentic Systems and Autonomous Orchestration.*
