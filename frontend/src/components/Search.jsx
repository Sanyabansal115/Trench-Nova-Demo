import React, { useState } from "react";
import axios from "axios";

export default function Search() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [latency, setLatency] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getConfidenceScore = (distance) => {
    // If distance is 0.0016, this returns ~98% match
    const confidence = Math.max(0, 1 - distance * 10);
    return (confidence * 100).toFixed(0) + "%";
  };

  const search = async () => {
    if (!q) return;
    setLoading(true);
    setError(null);
    try {
      const start = performance.now();
      const res = await axios.post("http://localhost:5000/search", 
        { query: q, top_k: 5 },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      const end = performance.now();
      setLatency(Math.round(end - start));
      setResults(res.data.results || []);
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || "Unknown error";
      setError(`Search failed: ${errorMsg}`);
      setResults([]);
      console.error("Full error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <div style={{ marginBottom: 12 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Enter query..."
          style={{ width: "60%", padding: 8, marginRight: 8 }}
        />
        <button onClick={search} disabled={loading || !q}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {latency !== null && <div style={{ marginBottom: 8 }}>Client latency: {latency} ms</div>}
      {error && <div style={{ color: "red", marginBottom: 8 }}>{error}</div>}

      <ul>
        {results.map((r) => (
          <li key={r.id} style={{ marginBottom: 10 }}>
            <div><strong>Score:</strong> {r.score ? r.score.toFixed(3) : "—"}</div>
            <div><strong>Confidence:</strong> {getConfidenceScore(r.score)}</div>
            <div style={{ marginTop: 4 }}>{r.text}</div>
            <div style={{ marginTop: 4, color: "#666", fontSize: 12 }}>ID: {r.id}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
