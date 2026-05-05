import { useState, useEffect } from 'react';
import { Brain, Search, Plus, Trash2, Zap, Clock, Tag } from 'lucide-react';
import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8007/api' });

export default function MemoryPage() {
  const [memories, setMemories] = useState<any[]>([]);
  const [query, setQuery] = useState("");
  const [newContent, setNewContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<any>({ count: 0, engine: "INITIALIZING..." });

  const [expandedQuery, setExpandedQuery] = useState("");

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/health');
      setStats({
        ...res.data.stats,
        engine: res.data.engine
      });
    } catch (err) {
      console.error(err);
    }
  };

  const startSession = async () => {
    try {
      setLoading(true);
      const res = await api.get('/session/start');
      alert(`Session Started: ${res.data.session_id}\n\nRetrieved ${res.data.snapshot.core_knowledge.length} Core Fragments and ${res.data.snapshot.recent_history.length} Recent History items.`);
    } catch (err) {
      alert("Failed to initialize session.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: any) => {
    const val = e.target.value;
    setQuery(val);
    if (val.length > 2) {
      try {
        const res = await api.post('/recall', { query: val, limit: 10 });
        setMemories(res.data.results);
        setExpandedQuery(res.data.expanded_query);
      } catch (err) {
        console.error(err);
      }
    } else {
      setMemories([]);
      setExpandedQuery("");
    }
  };

  const handleStore = async () => {
    if (!newContent) return;
    setLoading(true);
    try {
      await api.post('/memories', { content: newContent, importance: 8, tags: ["user-input"] });
      setNewContent("");
      fetchStats();
      alert("Memory stored in Long-Term Retrieval.");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteMemory = async (id: string) => {
    try {
      await api.delete(`/memories/${id}`);
      setMemories(memories.filter(m => m.id !== id));
      fetchStats();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="memory-container">
      {/* Sidebar: Ingestion */}
      <div className="sidebar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '40px' }}>
          <Brain color="var(--glow-purple)" size={32} />
          <h1 style={{ margin: 0, fontSize: '24px', letterSpacing: '-1.5px' }}>NexusMemory</h1>
        </div>

        <div className="glass-card" style={{ padding: '16px', background: 'rgba(59, 130, 246, 0.05)', marginBottom: '12px' }}>
           <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>SYSTEM STATUS</div>
           <div style={{ fontSize: '14px', fontWeight: 600, color: 'var(--glow-blue)' }}>{stats.engine || "OPTIMIZED"}</div>
        </div>

        <div className="glass-card" style={{ padding: '16px', background: 'rgba(139, 92, 246, 0.05)' }}>
           <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>STORED FRAGMENTS</div>
           <div style={{ fontSize: '24px', fontWeight: 800 }}>{stats.count}</div>
        </div>

        <div style={{ marginTop: '10px' }}>
           <button 
             className="action-btn" 
             style={{ background: 'transparent', border: '1px solid var(--glow-purple)', color: 'var(--glow-purple)', fontSize: '12px', padding: '8px', marginBottom: '8px' }}
             onClick={async () => {
               try {
                 setLoading(true);
                 const res = await api.post('/compress?days=0'); // Force compression for demo
                 alert(res.data.status === 'success' ? `Successfully compressed ${res.data.fragments_compressed} fragments!` : res.data.message);
                 fetchStats();
               } catch (err) {
                 alert("Compression failed: Key fragments insufficient.");
               } finally {
                 setLoading(false);
               }
             }}
           >
             TRIGGER COGNITIVE COMPRESSION
           </button>
           <button 
             className="action-btn" 
             style={{ background: 'transparent', border: '1px solid var(--glow-blue)', color: 'var(--glow-blue)', fontSize: '12px', padding: '8px' }}
             onClick={startSession}
           >
             START AGENT SESSION
           </button>
        </div>

        <div style={{ marginTop: '30px' }}>
           <label style={{ fontSize: '12px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Ingest New Fragment</label>
           <textarea 
             className="search-bar" 
             style={{ height: '120px', marginTop: '10px', resize: 'none', fontSize: '14px' }}
             placeholder="What should the agent remember?"
             value={newContent}
             onChange={(e) => setNewContent(e.target.value)}
           />
           <button className="action-btn" onClick={handleStore} disabled={loading}>
             {loading ? "ENCODING..." : "STORE IN LONG-TERM RECALL"}
           </button>
        </div>

        <div style={{ flex: 1 }}></div>
        <p style={{ fontSize: '11px', color: 'var(--text-dim)', textAlign: 'center' }}>
           Powered by ChromaDB Vector Engine & Local All-MiniLM Embeddings
        </p>
      </div>

      {/* Main Viewport: Recall */}
      <div className="viewport">
        <div style={{ position: 'relative' }}>
          <Search style={{ position: 'absolute', left: '16px', top: '18px' }} color="var(--text-dim)" size={20} />
          <input 
            className="search-bar" 
            style={{ paddingLeft: '50px', marginBottom: '8px' }}
            placeholder="Search through the agent's semantic memories..."
            value={query}
            onChange={handleSearch}
          />
          {expandedQuery && (
            <div style={{ fontSize: '11px', color: 'var(--glow-blue)', marginBottom: '24px', fontStyle: 'italic' }}>
              Semantic expansion: {expandedQuery}
            </div>
          )}
        </div>

        <div style={{ marginTop: '20px' }}>
          {memories.length === 0 && query.length > 2 && (
            <p style={{ color: 'var(--text-dim)' }}>No semantic matches found for "{query}".</p>
          )}

          {memories.map((m, i) => (
            <div key={m.id} className="glass-card" style={{ position: 'relative' }}>
               <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
                      <span className="memory-tag"><Clock size={10} style={{ marginRight: '4px' }}/> {m.metadata.timestamp.split('T')[0]}</span>
                      <span className="memory-tag"><Zap size={10} style={{ marginRight: '4px' }}/> Semantic Match: {Math.round((1 - m.distance) * 100)}%</span>
                    </div>
                    <p style={{ margin: 0, fontSize: '15px', lineHeight: 1.6 }}>{m.content}</p>
                  </div>
                  <button 
                    onClick={() => deleteMemory(m.id)}
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '8px' }}
                  >
                    <Trash2 size={18} color="#ef4444" />
                  </button>
               </div>
               
               <div className="importance-bar">
                  <div className="importance-fill" style={{ width: `${m.metadata.importance * 10}%` }}></div>
               </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
