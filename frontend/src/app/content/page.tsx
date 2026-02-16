"use client";

import { useState } from "react";

const contentTypes = [
  { value: "post", label: "Post", icon: "📱" },
  { value: "story", label: "Story", icon: "📸" },
  { value: "reel", label: "Reel", icon: "🎬" },
  { value: "carrossel", label: "Carrossel", icon: "🎠" },
  { value: "thread", label: "Thread", icon: "🧵" },
  { value: "podcast_script", label: "Roteiro Podcast", icon: "🎙️" },
];

const platforms = [
  { value: "instagram", label: "Instagram" },
  { value: "youtube", label: "YouTube" },
  { value: "tiktok", label: "TikTok" },
  { value: "linkedin", label: "LinkedIn" },
];

const tones = [
  { value: "casual", label: "Casual" },
  { value: "formal", label: "Formal" },
  { value: "humoristico", label: "Humoristico" },
  { value: "educativo", label: "Educativo" },
  { value: "inspiracional", label: "Inspiracional" },
];

export default function ContentPage() {
  const [contentType, setContentType] = useState("post");
  const [platform, setPlatform] = useState("instagram");
  const [tone, setTone] = useState("casual");
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/content/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content_type: contentType, platform, tone, topic }),
      });
      const data = await res.json();
      setResult(data.body || data.response || "Erro ao gerar conteudo.");
    } catch {
      setResult("Erro de conexao.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Criar Conteudo</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Tipo de Conteudo</label>
            <div className="grid grid-cols-3 gap-2">
              {contentTypes.map((ct) => (
                <button
                  key={ct.value}
                  onClick={() => setContentType(ct.value)}
                  className={`p-3 rounded-lg border text-sm text-center transition-colors ${
                    contentType === ct.value
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  <span className="text-xl block mb-1">{ct.icon}</span>
                  {ct.label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Plataforma</label>
            <div className="flex gap-2">
              {platforms.map((p) => (
                <button
                  key={p.value}
                  onClick={() => setPlatform(p.value)}
                  className={`px-4 py-2 rounded-lg border text-sm transition-colors ${
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

          <div>
            <label className="block text-sm font-medium mb-2">Tom</label>
            <div className="flex flex-wrap gap-2">
              {tones.map((t) => (
                <button
                  key={t.value}
                  onClick={() => setTone(t.value)}
                  className={`px-3 py-1 rounded-full text-sm transition-colors ${
                    tone === t.value
                      ? "bg-[var(--primary)] text-white"
                      : "border border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Tema / Topico</label>
            <textarea
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Descreva sobre o que voce quer criar..."
              rows={4}
              className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            />
          </div>

          <button
            onClick={generate}
            disabled={loading || !topic.trim()}
            className="w-full py-3 rounded-lg bg-[var(--primary)] text-white font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
          >
            {loading ? "Gerando..." : "Gerar Conteudo"}
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Resultado</label>
          <div className="min-h-[400px] p-4 rounded-lg border border-[var(--border)] bg-[var(--secondary)]">
            {result ? (
              <p className="text-sm whitespace-pre-wrap">{result}</p>
            ) : (
              <p className="text-sm text-[var(--muted-foreground)]">
                O conteudo gerado aparecera aqui...
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
