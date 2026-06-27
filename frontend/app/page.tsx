"use client";
import { useState } from "react";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function runScan(target: string) {
  const res = await fetch(`${BASE_URL}/scans/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target }),
  });
  if (!res.ok) throw new Error("Erreur");
  return res.json();
}

async function getScanHistory() {
  const res = await fetch(`${BASE_URL}/scans/history`);
  if (!res.ok) throw new Error("Erreur");
  return res.json();
}

export default function Home() {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  async function handleScan() {
    if (!target) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await runScan(target);
      setResult(data);
    } catch (e) {
      setError("Erreur lors du scan. Verifie que le backend tourne.");
    } finally {
      setLoading(false);
    }
  }

  async function handleHistory() {
    const data = await getScanHistory();
    setHistory(data);
    setShowHistory(true);
  }

  const d = result?.diagnosis;

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-2xl mx-auto">

        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white mb-2">NetDiagAI</h1>
          <p className="text-gray-400">Diagnostic reseau intelligent propulse par IA</p>
        </div>

        <div className="bg-gray-900 rounded-2xl p-6 mb-6 border border-gray-800">
          <label className="block text-sm text-gray-400 mb-2">
            Cible a analyser (domaine ou IP)
          </label>
          <div className="flex gap-3">
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="ex: google.com ou 192.168.1.1"
              className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleScan}
              disabled={loading || !target}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-6 py-3 rounded-xl font-medium transition-colors"
            >
              {loading ? "Analyse..." : "Scanner"}
            </button>
          </div>
          {loading && (
            <p className="text-blue-400 text-sm mt-3">
              L'IA analyse le reseau, patiente quelques secondes...
            </p>
          )}
          {error && (
            <p className="text-red-400 text-sm mt-3">{error}</p>
          )}
        </div>

        {d && (
          <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">{d.statut_global}</h2>
              <div className="text-right">
                <div className="text-3xl font-bold text-blue-400">{d.score_sante}</div>
                <div className="text-xs text-gray-500">score sante /100</div>
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-4 text-gray-300 text-sm leading-relaxed">
              {d.resume}
            </div>

            {d.problemes?.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-400 mb-2 uppercase tracking-wide">
                  Problemes detectes
                </h3>
                <div className="space-y-2">
                  {d.problemes.map((p: any, i: number) => (
                    <div key={i} className="bg-red-950 border border-red-900 rounded-xl p-3">
                      <div className="flex justify-between items-start">
                        <span className="font-medium text-red-300">{p.titre}</span>
                        <span className="text-xs bg-red-900 text-red-300 px-2 py-0.5 rounded-full">
                          {p.severite}
                        </span>
                      </div>
                      <p className="text-sm text-red-400 mt-1">{p.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {d.recommandations?.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-400 mb-2 uppercase tracking-wide">
                  Recommandations
                </h3>
                <div className="space-y-2">
                  {d.recommandations.map((r: any, i: number) => (
                    <div key={i} className="bg-gray-800 rounded-xl p-3 flex gap-3">
                      <span className="text-green-400 mt-0.5">V</span>
                      <div>
                        <div className="font-medium text-white text-sm">{r.action}</div>
                        <div className="text-gray-400 text-xs mt-1">{r.detail}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="mt-4">
          <button
            onClick={handleHistory}
            className="text-gray-500 hover:text-gray-300 text-sm underline"
          >
            Voir l'historique des scans
          </button>
          {showHistory && history.length > 0 && (
            <div className="mt-4 bg-gray-900 rounded-2xl p-4 border border-gray-800">
              <h3 className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wide">
                Historique
              </h3>
              <div className="space-y-2">
                {history.map((s: any) => (
                  <div key={s.id} className="flex justify-between items-center bg-gray-800 rounded-xl px-4 py-3">
                    <span className="text-white font-medium">{s.target}</span>
                    <span className="text-gray-500 text-xs">{s.diagnosis?.statut_global || "-"}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </main>
  );
}