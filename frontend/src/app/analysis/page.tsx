"use client";

import { useState } from "react";

const platforms = [
  { value: "instagram", label: "Instagram", color: "#E1306C" },
  { value: "youtube", label: "YouTube", color: "#FF0000" },
  { value: "tiktok", label: "TikTok", color: "#000000" },
  { value: "linkedin", label: "LinkedIn", color: "#0077B5" },
];

const analysisTypes = [
  { value: "profile", label: "Perfil", description: "Analise completa do perfil" },
  { value: "trends", label: "Tendencias", description: "Busque trends por keyword" },
  { value: "viral", label: "Conteudo Viral", description: "Descubra conteudos virais" },
];

export default function AnalysisPage() {
  const [handle, setHandle] = useState("");
  const [platform, setPlatform] = useState("instagram");
  const [analysisType, setAnalysisType] = useState("profile");
  const [keywords, setKeywords] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [viralContent, setViralContent] = useState<any[]>([]);

  const analyzeProfile = async () => {
    if (!handle.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/analysis/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ platform, profile_handle: handle }),
      });
      const data = await res.json();
      setResult(data.response || JSON.stringify(data, null, 2));
    } catch {
      setResult("Erro de conexao.");
    } finally {
      setLoading(false);
    }
  };

  const searchTrends = async () => {
    if (!keywords.trim()) return;
    setLoading(true);
    try {
      const kws = keywords.split(",").map((k) => k.trim()).filter(Boolean);
      const res = await fetch("/api/analysis/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          platform,
          profile_handle: kws.join(", "),
        }),
      });
      const data = await res.json();
      setResult(data.response || JSON.stringify(data, null, 2));
    } catch {
      setResult("Erro de conexao.");
    } finally {
      setLoading(false);
    }
  };

  const fetchViral = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ platform });
      const res = await fetch(`/api/analysis/profile?${params}`);
      const data = await res.json();
      setViralContent(data.viral_content || []);
      setResult("");
    } catch {
      setResult("Erro ao buscar conteudo viral.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = () => {
    if (analysisType === "profile") analyzeProfile();
    else if (analysisType === "trends") searchTrends();
    else fetchViral();
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-2">Analise & Tendencias</h1>
      <p className="text-sm text-[var(--muted-foreground)] mb-6">
        Analise perfis, descubra tendencias e encontre conteudo viral
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Tipo de Analise</label>
            <div className="space-y-2">
              {analysisTypes.map((at) => (
                <button
                  key={at.value}
                  onClick={() => setAnalysisType(at.value)}
                  className={`w-full text-left p-3 rounded-lg border text-sm transition-colors ${
                    analysisType === at.value
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  <span className="font-medium">{at.label}</span>
                  <span className="block text-xs text-[var(--muted-foreground)] mt-0.5">
                    {at.description}
                  </span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Plataforma</label>
            <div className="grid grid-cols-2 gap-2">
              {platforms.map((p) => (
                <button
                  key={p.value}
                  onClick={() => setPlatform(p.value)}
                  className={`px-3 py-2 rounded-lg border text-sm transition-colors ${
                    platform === p.value
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          {analysisType === "profile" && (
            <div>
              <label className="block text-sm font-medium mb-2">Perfil</label>
              <input
                value={handle}
                onChange={(e) => setHandle(e.target.value)}
                placeholder="@usuario"
                className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
            </div>
          )}

          {analysisType === "trends" && (
            <div>
              <label className="block text-sm font-medium mb-2">Keywords</label>
              <input
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="marketing digital, IA, redes sociais"
                className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
              <p className="text-xs text-[var(--muted-foreground)] mt-1">
                Separe por virgula (max 5)
              </p>
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading || (analysisType === "profile" && !handle.trim()) || (analysisType === "trends" && !keywords.trim())}
            className="w-full py-3 rounded-lg bg-[var(--primary)] text-white font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
          >
            {loading ? "Analisando..." : analysisType === "viral" ? "Buscar Viral" : "Analisar"}
          </button>
        </div>

        <div className="lg:col-span-2">
          <label className="block text-sm font-medium mb-2">Resultados</label>
          <div className="min-h-[500px] p-4 rounded-lg border border-[var(--border)] bg-[var(--secondary)]">
            {result ? (
              <p className="text-sm whitespace-pre-wrap">{result}</p>
            ) : viralContent.length > 0 ? (
              <div className="space-y-3">
                {viralContent.map((item, i) => (
                  <div key={i} className="p-3 rounded-lg border border-[var(--border)] bg-[var(--card)]">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium uppercase text-[var(--muted-foreground)]">
                        {item.platform}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--primary)]/10 text-[var(--primary)]">
                        Score: {item.virality_score}
                      </span>
                    </div>
                    <p className="text-sm">{item.content_text}</p>
                    <div className="flex gap-1 mt-2 flex-wrap">
                      {(item.hashtags || []).map((h: string, j: number) => (
                        <span key={j} className="text-xs text-[var(--muted-foreground)]">{h}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full">
                <p className="text-sm text-[var(--muted-foreground)]">
                  Selecione um tipo de analise e clique para comecar
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
