import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getHistory } from "../api/scan";

const LEVEL_STYLES = {
  LOW: "bg-green-500/10 text-green-300 border-green-500/40",
  SUSPICIOUS: "bg-amber-500/10 text-amber-300 border-amber-500/40",
  HIGH: "bg-red-500/10 text-red-300 border-red-500/40",
};

export default function History() {
  const [scans, setScans] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then((data) => setScans(Array.isArray(data) ? data : data.items || []))
      .catch(() => setError("Could not load history."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-slate-900">
      <header className="border-b border-slate-800 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-white">🛡️ Sentinel AI</h1>
        <Link
          to="/dashboard"
          className="text-sm text-slate-400 hover:text-white transition"
        >
          ← Back to scanner
        </Link>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-semibold text-white mb-6">Scan history</h2>

        {loading && <p className="text-slate-400">Loading...</p>}

        {error && (
          <div className="bg-red-500/10 border border-red-500/40 text-red-300 rounded p-4">
            {error}
          </div>
        )}

        {!loading && !error && scans.length === 0 && (
          <p className="text-slate-400">No scans yet.</p>
        )}

        <div className="space-y-3">
          {scans.map((scan) => (
            <div
              key={scan.id}
              className="bg-slate-800 rounded-lg p-4 flex justify-between items-center gap-4"
            >
              <div className="min-w-0">
                <div className="text-white text-sm truncate">{scan.url}</div>
                <div className="text-slate-500 text-xs mt-1">
                  {scan.domain}
                </div>
              </div>

              <div
                className={`shrink-0 border rounded px-3 py-1 text-sm font-medium ${
                  LEVEL_STYLES[scan.risk_level]
                }`}
              >
                {scan.risk_level} · {scan.risk_score}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}