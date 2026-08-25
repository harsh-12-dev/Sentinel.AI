import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { scanUrl } from "../api/scan";
import { logout } from "../api/auth";

const LEVEL_STYLES = {
  LOW: "bg-green-500/10 border-green-500/40 text-green-300",
  SUSPICIOUS: "bg-amber-500/10 border-amber-500/40 text-amber-300",
  HIGH: "bg-red-500/10 border-red-500/40 text-red-300",
};

const BAR_COLORS = {
  LOW: "bg-green-500",
  SUSPICIOUS: "bg-amber-500",
  HIGH: "bg-red-500",
};

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleScan(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const data = await scanUrl(url);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Scan failed. Try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-slate-900">
      <header className="border-b border-slate-800 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-white">🛡️ Sentinel AI</h1>
        <button
          onClick={handleLogout}
          className="text-sm text-slate-400 hover:text-white transition"
        >
          Logout
        </button>
      </header>

      <main className="max-w-2xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-semibold text-white mb-1">
          Check a link
        </h2>
        <p className="text-slate-400 mb-6">
          Paste any URL to see if it looks safe.
        </p>

        <form onSubmit={handleScan} className="flex gap-2 mb-6">
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
            className="flex-1 bg-slate-800 text-white rounded px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium rounded px-6 transition"
          >
            {loading ? "Scanning..." : "Scan"}
          </button>
        </form>

        {error && (
          <div className="bg-red-500/10 border border-red-500/40 text-red-300 rounded p-4">
            {error}
          </div>
        )}

        {result && (
          <div className={`border rounded-lg p-6 ${LEVEL_STYLES[result.risk_level]}`}>
            <div className="flex justify-between items-start mb-4">
              <div>
                <div className="text-2xl font-bold">{result.risk_level}</div>
                <div className="text-sm opacity-70 break-all mt-1">
                  {result.domain}
                </div>
              </div>
              <div className="text-3xl font-bold">{result.risk_score}</div>
            </div>

            <div className="w-full bg-slate-700/50 rounded-full h-2 mb-5">
              <div
                className={`h-2 rounded-full ${BAR_COLORS[result.risk_level]}`}
                style={{ width: `${result.risk_score}%` }}
              />
            </div>

            {result.reasons?.length > 0 ? (
              <ul className="space-y-2 text-sm">
                {result.reasons.map((reason, i) => (
                  <li key={i} className="flex gap-2">
                    <span>•</span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm opacity-70">
                No risk signals detected.
              </p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}