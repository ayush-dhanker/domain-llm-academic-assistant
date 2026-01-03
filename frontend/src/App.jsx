import { useMemo, useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

function SourceCard({ s }) {
  const title = s?.section || s?.module_name || "Unknown source";
  const para = s?.paragraph ? ` ${s.paragraph}` : "";
  const doc = s?.doc_type ? `(${s.doc_type})` : "";

  return (
    <div className="sourceCard">
      <div className="sourceTitle">{title}{para} <span className="muted">{doc}</span></div>
    </div>
  );
}

export default function App() {
  const [question, setQuestion] = useState("What is the standard duration of the Master’s program?");
  const [topK, setTopK] = useState(4);

  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [error, setError] = useState("");

  const canAsk = useMemo(() => question.trim().length >= 3 && !loading, [question, loading]);

  async function ask() {
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const res = await fetch(`${API_BASE}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, top_k: topK }),
      });

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(`API error ${res.status}: ${msg}`);
      }

      const data = await res.json();
      setAnswer(data.answer || "");
      setSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (e) {
      setError(e.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function onKeyDown(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      if (canAsk) ask();
    }
  }

  return (
    <div className="page app">
      <div className="container">
        <header className="header">
          <div>
            <h1>Academic Regulations Assistant</h1>
            <p className="muted">RAG + LoRA-tuned TinyLlama • Based on OVGU regulations</p>
          </div>

          <a className="muted link" href={`${API_BASE}/docs`} target="_blank" rel="noreferrer">
            API Docs
          </a>
        </header>

        <div className="card">
          <label className="label">Ask a question</label>
          <textarea
            className="textarea"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="e.g., How long is the standard duration of the program?"
            rows={4}
          />

          <div className="row">
            <div className="controls">
              <label className="label muted">Top K</label>
              <select className="select" value={topK} onChange={(e) => setTopK(Number(e.target.value))}>
                {[2, 3, 4, 5, 6].map((k) => (
                  <option key={k} value={k}>{k}</option>
                ))}
              </select>
            </div>

            <button className="button" disabled={!canAsk} onClick={ask}>
              {loading ? "Thinking…" : "Ask"}
            </button>
          </div>

          <div className="hint muted">
            Tip: Press <b>Ctrl/⌘ + Enter</b> to submit.
          </div>
        </div>

        {error && (
          <div className="card errorCard">
            <div className="errorTitle">Error</div>
            <div className="errorText">{error}</div>
          </div>
        )}

        {(answer || loading) && (
          <div className="card">
            <div className="label">Answer</div>
            <div className="answerBox">
              {loading ? <span className="muted">Generating answer…</span> : answer || <span className="muted">No answer.</span>}
            </div>
          </div>
        )}

        {sources.length > 0 && (
          <div className="card">
            <div className="label">Sources</div>
            <div className="sourcesGrid">
              {sources.map((s, i) => (
                <SourceCard key={i} s={s} />
              ))}
            </div>
          </div>
        )}

        <footer className="footer muted">
          Backend: <code>{API_BASE}</code>
        </footer>
      </div>
    </div>
  );
}
