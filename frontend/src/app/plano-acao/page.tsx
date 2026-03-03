"use client";

import { useState, useEffect, useRef, useCallback } from "react";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface PlanSlot {
  title: string;
  platform: string;
  content_type: string;
  scheduled_date: string;
  scheduled_time: string;
  topic: string;
  pillar: string;
  notes: string;
  status: string;
}

interface ContentPiece {
  title: string;
  platform: string;
  content_type: string;
  hook: string;
  body: string;
  caption: string;
  cta: string;
  hashtags: string[];
  visual_suggestion: string;
  slides: Record<string, unknown>[];
  story_frames: Record<string, unknown>[];
  thread_tweets: string[];
}

interface ScriptBlock {
  timestamp: string;
  visual: string;
  speech: string;
  text_overlay: string;
  effect: string;
  notes: string;
}

interface ScriptResult {
  title: string;
  platform: string;
  duration_seconds?: number;
  hook: string;
  blocks: ScriptBlock[];
  audio_suggestion?: string;
  hashtags: string[];
  caption: string;
}

interface QualityCheck {
  name: string;
  passed: boolean;
  severity: string;
  message: string;
  details: string;
}

interface QualityReport {
  verdict: string;
  score: number;
  checks: QualityCheck[];
  summary: string;
  recommendations: string[];
}

interface PipelineRun {
  id: string;
  version: number;
  status: string;
  config: Record<string, unknown>;
  created_at: string;
  completed_at?: string;
}

interface PipelineResult {
  pipeline_id: string;
  status: string;
  audit_result?: {
    best_posting_times: Record<string, string[]>;
    recommendations: string[];
    pillars: { name: string; description: string; percentage: number }[];
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
  };
  plan_result?: {
    slots?: PlanSlot[];
    weeks?: { week_number: number; start_date: string; end_date: string; slots: PlanSlot[] }[];
  };
  content_results: ContentPiece[];
  script_results: ScriptResult[];
  quality_report?: QualityReport;
}

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const PLATFORMS = [
  { value: "instagram", label: "Instagram", color: "#E1306C" },
  { value: "youtube", label: "YouTube", color: "#FF0000" },
  { value: "tiktok", label: "TikTok", color: "#00F2EA" },
  { value: "linkedin", label: "LinkedIn", color: "#0A66C2" },
];

const PIPELINE_STEPS = [
  { key: "init", label: "Iniciando" },
  { key: "audit", label: "Auditoria" },
  { key: "plan", label: "Planejamento" },
  { key: "content", label: "Conteudo" },
  { key: "scripts", label: "Roteiros" },
  { key: "quality", label: "Qualidade" },
  { key: "persist", label: "Salvando" },
];

const platformColor = (p: string) =>
  PLATFORMS.find((pl) => pl.value === p)?.color || "var(--primary)";

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function PlanoAcaoPage() {
  // --- Config state ---
  const [period, setPeriod] = useState<"weekly" | "monthly">("weekly");
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(["instagram", "youtube", "tiktok", "linkedin"]);
  const [focusTopics, setFocusTopics] = useState("");
  const [includeVideo, setIncludeVideo] = useState(true);

  // --- Generation state ---
  const [generating, setGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState("");
  const [stepMessage, setStepMessage] = useState("");
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [error, setError] = useState("");

  // --- UI state ---
  const [expandedSlot, setExpandedSlot] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<"plano" | "horarios" | "qualidade" | "historico">("plano");
  const [runs, setRuns] = useState<PipelineRun[]>([]);
  const [loadingRuns, setLoadingRuns] = useState(false);
  const [loadingRunDetail, setLoadingRunDetail] = useState(false);

  const abortRef = useRef<AbortController | null>(null);

  // --- Load history ---
  const loadRuns = useCallback(async () => {
    setLoadingRuns(true);
    try {
      const res = await fetch("/api/plano-acao?limit=10");
      if (res.ok) {
        const data = await res.json();
        setRuns(data.runs || []);
      }
    } catch {
      /* ignore */
    } finally {
      setLoadingRuns(false);
    }
  }, []);

  useEffect(() => {
    loadRuns();
  }, [loadRuns]);

  // --- Toggle platform ---
  const togglePlatform = (p: string) => {
    setSelectedPlatforms((prev) =>
      prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]
    );
  };

  // --- Generate ---
  const generate = async () => {
    if (selectedPlatforms.length === 0) return;
    setGenerating(true);
    setCurrentStep("init");
    setStepMessage("Iniciando pipeline...");
    setResult(null);
    setError("");
    setExpandedSlot(null);

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const res = await fetch("/api/plano-acao/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          period,
          platforms: selectedPlatforms,
          focus_topics: focusTopics.trim() ? focusTopics.split(",").map((t) => t.trim()) : null,
          include_video: includeVideo,
        }),
        signal: controller.signal,
      });

      if (!res.ok || !res.body) {
        setError("Erro ao conectar com o servidor.");
        setGenerating(false);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const payload = line.slice(6).trim();
          if (payload === "[DONE]") break;

          try {
            const msg = JSON.parse(payload);
            if (msg.type === "progress") {
              setCurrentStep(msg.step || "");
              setStepMessage(msg.message || "");
            } else if (msg.type === "complete") {
              setResult(msg.data);
              setActiveTab("plano");
            } else if (msg.type === "error") {
              setError(msg.message || "Erro desconhecido");
            }
          } catch {
            /* ignore parse errors */
          }
        }
      }
    } catch (e: unknown) {
      if (e instanceof DOMException && e.name === "AbortError") return;
      setError("Erro de conexao com o servidor.");
    } finally {
      setGenerating(false);
      abortRef.current = null;
      loadRuns();
    }
  };

  // --- Load run detail ---
  const loadRunDetail = async (runId: string) => {
    setLoadingRunDetail(true);
    try {
      const res = await fetch(`/api/plano-acao/${runId}`);
      if (res.ok) {
        const data = await res.json();
        setResult({
          pipeline_id: data.id,
          status: data.status,
          audit_result: data.audit_result,
          plan_result: data.plan_result,
          content_results: data.content_results || [],
          script_results: data.script_results || [],
          quality_report: data.quality_report,
        });
        setActiveTab("plano");
        setExpandedSlot(null);
      }
    } catch {
      /* ignore */
    } finally {
      setLoadingRunDetail(false);
    }
  };

  // --- Helpers ---
  const allSlots: PlanSlot[] = (() => {
    if (!result?.plan_result) return [];
    if (result.plan_result.slots) return result.plan_result.slots;
    if (result.plan_result.weeks) return result.plan_result.weeks.flatMap((w) => w.slots || []);
    return [];
  })();

  const slotsByDate = allSlots.reduce<Record<string, PlanSlot[]>>((acc, slot) => {
    const key = slot.scheduled_date || "Sem data";
    if (!acc[key]) acc[key] = [];
    acc[key].push(slot);
    return acc;
  }, {});

  const stepIndex = PIPELINE_STEPS.findIndex((s) => s.key === currentStep);
  const progressPercent = generating
    ? Math.round(((stepIndex + 1) / PIPELINE_STEPS.length) * 100)
    : 0;

  const findContent = (slot: PlanSlot, idx: number): ContentPiece | undefined => {
    if (!result?.content_results) return undefined;
    return (
      result.content_results.find(
        (c) =>
          c.title === slot.title &&
          c.platform === slot.platform
      ) || result.content_results[idx]
    );
  };

  const findScript = (slot: PlanSlot, idx: number): ScriptResult | undefined => {
    if (!result?.script_results) return undefined;
    return (
      result.script_results.find(
        (s) =>
          s.title === slot.title &&
          s.platform === slot.platform
      ) || result.script_results[idx]
    );
  };

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Plano de Acao</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* ============== LEFT: Config ============== */}
        <div className="space-y-6">
          {/* Period */}
          <div>
            <label className="block text-sm font-medium mb-2">Periodo</label>
            <div className="flex gap-2">
              {(["weekly", "monthly"] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => setPeriod(p)}
                  className={`px-4 py-2 rounded-lg border text-sm transition-colors ${
                    period === p
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  {p === "weekly" ? "Semanal" : "Mensal"}
                </button>
              ))}
            </div>
          </div>

          {/* Platforms */}
          <div>
            <label className="block text-sm font-medium mb-2">Plataformas</label>
            <div className="flex flex-wrap gap-2">
              {PLATFORMS.map((p) => (
                <button
                  key={p.value}
                  onClick={() => togglePlatform(p.value)}
                  className={`px-3 py-1.5 rounded-lg border text-sm transition-colors ${
                    selectedPlatforms.includes(p.value)
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          {/* Focus topics */}
          <div>
            <label className="block text-sm font-medium mb-2">Topicos foco (opcional)</label>
            <textarea
              value={focusTopics}
              onChange={(e) => setFocusTopics(e.target.value)}
              placeholder="Ex: marketing digital, IA, produtividade (separados por virgula)"
              rows={3}
              className="w-full px-4 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            />
          </div>

          {/* Video toggle */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIncludeVideo(!includeVideo)}
              className={`w-10 h-6 rounded-full transition-colors relative ${
                includeVideo ? "bg-[var(--primary)]" : "bg-[var(--border)]"
              }`}
            >
              <span
                className={`absolute top-0.5 w-5 h-5 rounded-full bg-white transition-transform ${
                  includeVideo ? "translate-x-4" : "translate-x-0.5"
                }`}
              />
            </button>
            <span className="text-sm">Incluir roteiros de video</span>
          </div>

          {/* Generate button */}
          <button
            onClick={generate}
            disabled={generating || selectedPlatforms.length === 0}
            className="w-full py-3 rounded-lg bg-[var(--primary)] text-white font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
          >
            {generating ? "Gerando..." : "Gerar Plano de Acao Completo"}
          </button>

          {/* Progress bar */}
          {generating && (
            <div className="space-y-2">
              <div className="w-full h-2 rounded-full bg-[var(--secondary)] overflow-hidden">
                <div
                  className="h-full bg-[var(--primary)] rounded-full transition-all duration-500"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
              <div className="flex justify-between text-xs text-[var(--muted-foreground)]">
                <span>{stepMessage}</span>
                <span>{progressPercent}%</span>
              </div>
              <div className="flex gap-1">
                {PIPELINE_STEPS.map((s, i) => (
                  <div
                    key={s.key}
                    className={`flex-1 h-1 rounded-full transition-colors ${
                      i <= stepIndex ? "bg-[var(--primary)]" : "bg-[var(--border)]"
                    }`}
                    title={s.label}
                  />
                ))}
              </div>
            </div>
          )}

          {error && (
            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
              {error}
            </div>
          )}
        </div>

        {/* ============== RIGHT: Results (2 cols wide) ============== */}
        <div className="lg:col-span-2">
          {!result && !generating && (
            <div className="flex items-center justify-center min-h-[400px] rounded-lg border border-[var(--border)] bg-[var(--secondary)]">
              <p className="text-[var(--muted-foreground)] text-sm">
                Configure e clique em &quot;Gerar Plano de Acao Completo&quot; para comecar.
              </p>
            </div>
          )}

          {generating && !result && (
            <div className="flex flex-col items-center justify-center min-h-[400px] rounded-lg border border-[var(--border)] bg-[var(--secondary)] gap-4">
              <div className="w-10 h-10 border-4 border-[var(--primary)] border-t-transparent rounded-full animate-spin" />
              <p className="text-sm text-[var(--muted-foreground)]">{stepMessage}</p>
            </div>
          )}

          {result && (
            <>
              {/* Tabs */}
              <div className="flex gap-1 mb-6 border-b border-[var(--border)]">
                {([
                  { key: "plano", label: "Plano" },
                  { key: "horarios", label: "Melhores Horarios" },
                  { key: "qualidade", label: "Qualidade" },
                  { key: "historico", label: "Historico" },
                ] as const).map((tab) => (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key)}
                    className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-px ${
                      activeTab === tab.key
                        ? "border-[var(--primary)] text-[var(--primary)]"
                        : "border-transparent text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Tab: Plano */}
              {activeTab === "plano" && (
                <div className="space-y-4">
                  {Object.keys(slotsByDate).length === 0 && (
                    <p className="text-sm text-[var(--muted-foreground)]">Nenhum slot encontrado no plano.</p>
                  )}
                  {Object.entries(slotsByDate).map(([date, slots]) => (
                    <div key={date} className="space-y-2">
                      <h3 className="text-sm font-semibold text-[var(--muted-foreground)] uppercase tracking-wide">
                        {formatDate(date)}
                      </h3>
                      {slots.map((slot, slotIdx) => {
                        const globalIdx = allSlots.indexOf(slot);
                        const isExpanded = expandedSlot === globalIdx;
                        const content = findContent(slot, globalIdx);
                        const script = findScript(slot, globalIdx);

                        return (
                          <div
                            key={`${date}-${slotIdx}`}
                            className="rounded-lg border border-[var(--border)] bg-[var(--card)] overflow-hidden"
                          >
                            <button
                              onClick={() => setExpandedSlot(isExpanded ? null : globalIdx)}
                              className="w-full flex items-center gap-3 p-3 text-left hover:bg-[var(--secondary)] transition-colors"
                            >
                              <span
                                className="w-2 h-2 rounded-full flex-shrink-0"
                                style={{ backgroundColor: platformColor(slot.platform) }}
                              />
                              <span
                                className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded flex-shrink-0"
                                style={{
                                  backgroundColor: platformColor(slot.platform) + "22",
                                  color: platformColor(slot.platform),
                                }}
                              >
                                {slot.platform}
                              </span>
                              <span className="text-xs text-[var(--muted-foreground)] flex-shrink-0">
                                {slot.content_type}
                              </span>
                              <span className="text-sm font-medium flex-1 truncate">
                                {slot.title || "Sem titulo"}
                              </span>
                              {slot.scheduled_time && (
                                <span className="text-xs text-[var(--muted-foreground)] flex-shrink-0">
                                  {slot.scheduled_time}
                                </span>
                              )}
                              <span className="text-xs text-[var(--muted-foreground)]">
                                {isExpanded ? "▲" : "▼"}
                              </span>
                            </button>

                            {isExpanded && (
                              <div className="border-t border-[var(--border)] p-4 space-y-4 text-sm">
                                {/* Slot info */}
                                {slot.topic && (
                                  <div>
                                    <span className="font-medium">Topico:</span>{" "}
                                    <span className="text-[var(--muted-foreground)]">{slot.topic}</span>
                                  </div>
                                )}
                                {slot.pillar && (
                                  <div>
                                    <span className="font-medium">Pilar:</span>{" "}
                                    <span className="text-[var(--muted-foreground)]">{slot.pillar}</span>
                                  </div>
                                )}

                                {/* Content piece */}
                                {content && (
                                  <div className="space-y-2 bg-[var(--secondary)] rounded-lg p-3">
                                    <h4 className="font-semibold text-xs uppercase tracking-wide text-[var(--primary)]">
                                      Conteudo
                                    </h4>
                                    {content.hook && (
                                      <div>
                                        <span className="font-medium">Hook:</span>{" "}
                                        <span className="text-[var(--muted-foreground)]">{content.hook}</span>
                                      </div>
                                    )}
                                    {content.body && (
                                      <div>
                                        <span className="font-medium">Body:</span>
                                        <p className="text-[var(--muted-foreground)] whitespace-pre-wrap mt-1">
                                          {content.body}
                                        </p>
                                      </div>
                                    )}
                                    {content.caption && (
                                      <div>
                                        <span className="font-medium">Caption:</span>
                                        <p className="text-[var(--muted-foreground)] whitespace-pre-wrap mt-1">
                                          {content.caption}
                                        </p>
                                      </div>
                                    )}
                                    {content.hashtags?.length > 0 && (
                                      <div className="flex flex-wrap gap-1">
                                        {content.hashtags.map((h, i) => (
                                          <span
                                            key={i}
                                            className="text-xs px-2 py-0.5 rounded-full bg-[var(--primary)]/10 text-[var(--primary)]"
                                          >
                                            {h.startsWith("#") ? h : `#${h}`}
                                          </span>
                                        ))}
                                      </div>
                                    )}
                                    {content.visual_suggestion && (
                                      <div>
                                        <span className="font-medium">Visual:</span>{" "}
                                        <span className="text-[var(--muted-foreground)]">
                                          {content.visual_suggestion}
                                        </span>
                                      </div>
                                    )}
                                    {content.cta && (
                                      <div>
                                        <span className="font-medium">CTA:</span>{" "}
                                        <span className="text-[var(--muted-foreground)]">{content.cta}</span>
                                      </div>
                                    )}
                                    {content.slides?.length > 0 && (
                                      <div>
                                        <span className="font-medium">Slides ({content.slides.length}):</span>
                                        <div className="mt-1 space-y-1">
                                          {content.slides.map((slide, i) => (
                                            <div
                                              key={i}
                                              className="text-xs p-2 rounded bg-[var(--card)] border border-[var(--border)]"
                                            >
                                              Slide {i + 1}: {JSON.stringify(slide)}
                                            </div>
                                          ))}
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                )}

                                {/* Script */}
                                {script && (
                                  <div className="space-y-2 bg-[var(--secondary)] rounded-lg p-3">
                                    <h4 className="font-semibold text-xs uppercase tracking-wide text-[var(--primary)]">
                                      Roteiro
                                    </h4>
                                    {script.duration_seconds && (
                                      <div className="text-xs text-[var(--muted-foreground)]">
                                        Duracao: {script.duration_seconds}s
                                      </div>
                                    )}
                                    {script.blocks?.map((block, bi) => (
                                      <div
                                        key={bi}
                                        className="text-xs p-2 rounded bg-[var(--card)] border border-[var(--border)] space-y-1"
                                      >
                                        {block.timestamp && (
                                          <span className="font-mono text-[var(--primary)]">
                                            [{block.timestamp}]
                                          </span>
                                        )}
                                        {block.visual && <p><strong>Visual:</strong> {block.visual}</p>}
                                        {block.speech && <p><strong>Fala:</strong> {block.speech}</p>}
                                        {block.text_overlay && (
                                          <p><strong>Texto:</strong> {block.text_overlay}</p>
                                        )}
                                      </div>
                                    ))}
                                  </div>
                                )}

                                {!content && !script && (
                                  <p className="text-xs text-[var(--muted-foreground)]">
                                    Detalhes do conteudo nao disponiveis para este slot.
                                  </p>
                                )}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  ))}
                </div>
              )}

              {/* Tab: Melhores Horarios */}
              {activeTab === "horarios" && (
                <div className="space-y-4">
                  {result.audit_result?.best_posting_times &&
                  Object.keys(result.audit_result.best_posting_times).length > 0 ? (
                    <div className="rounded-lg border border-[var(--border)] overflow-hidden">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="bg-[var(--secondary)]">
                            <th className="text-left p-3 font-medium">Plataforma</th>
                            <th className="text-left p-3 font-medium">Melhores Horarios</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(result.audit_result.best_posting_times).map(
                            ([platform, times]) => (
                              <tr key={platform} className="border-t border-[var(--border)]">
                                <td className="p-3">
                                  <span
                                    className="text-xs uppercase font-bold px-2 py-0.5 rounded"
                                    style={{
                                      backgroundColor: platformColor(platform) + "22",
                                      color: platformColor(platform),
                                    }}
                                  >
                                    {platform}
                                  </span>
                                </td>
                                <td className="p-3">
                                  <div className="flex flex-wrap gap-1">
                                    {(times || []).map((t, i) => (
                                      <span
                                        key={i}
                                        className="text-xs px-2 py-0.5 rounded-full bg-[var(--secondary)] border border-[var(--border)]"
                                      >
                                        {t}
                                      </span>
                                    ))}
                                  </div>
                                </td>
                              </tr>
                            )
                          )}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <p className="text-sm text-[var(--muted-foreground)]">
                      Dados de melhores horarios nao disponiveis.
                    </p>
                  )}

                  {/* Recommendations */}
                  {result.audit_result?.recommendations &&
                    result.audit_result.recommendations.length > 0 && (
                      <div className="rounded-lg border border-[var(--border)] p-4 space-y-2">
                        <h3 className="text-sm font-semibold">Recomendacoes</h3>
                        <ul className="space-y-1">
                          {result.audit_result.recommendations.map((r, i) => (
                            <li key={i} className="text-sm text-[var(--muted-foreground)] flex gap-2">
                              <span className="text-[var(--primary)] flex-shrink-0">-</span>
                              {r}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                </div>
              )}

              {/* Tab: Qualidade */}
              {activeTab === "qualidade" && (
                <div className="space-y-4">
                  {result.quality_report ? (
                    <>
                      {/* Score card */}
                      <div className="flex items-center gap-4 p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
                        <div
                          className={`text-3xl font-bold ${
                            result.quality_report.score >= 80
                              ? "text-green-500"
                              : result.quality_report.score >= 60
                              ? "text-yellow-500"
                              : "text-red-500"
                          }`}
                        >
                          {result.quality_report.score}
                        </div>
                        <div>
                          <div className="text-sm font-medium">Score de Qualidade</div>
                          <div className="text-xs text-[var(--muted-foreground)]">
                            Veredicto:{" "}
                            <span
                              className={`font-semibold ${
                                result.quality_report.verdict === "passed"
                                  ? "text-green-500"
                                  : result.quality_report.verdict === "warn"
                                  ? "text-yellow-500"
                                  : "text-red-500"
                              }`}
                            >
                              {result.quality_report.verdict.toUpperCase()}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Checks */}
                      {result.quality_report.checks?.length > 0 && (
                        <div className="rounded-lg border border-[var(--border)] overflow-hidden">
                          <table className="w-full text-sm">
                            <thead>
                              <tr className="bg-[var(--secondary)]">
                                <th className="text-left p-3 font-medium">Check</th>
                                <th className="text-left p-3 font-medium">Status</th>
                                <th className="text-left p-3 font-medium">Mensagem</th>
                              </tr>
                            </thead>
                            <tbody>
                              {result.quality_report.checks.map((check, i) => (
                                <tr key={i} className="border-t border-[var(--border)]">
                                  <td className="p-3 font-medium">{check.name}</td>
                                  <td className="p-3">
                                    <span
                                      className={`text-xs font-bold ${
                                        check.passed ? "text-green-500" : "text-red-500"
                                      }`}
                                    >
                                      {check.passed ? "OK" : "FALHA"}
                                    </span>
                                  </td>
                                  <td className="p-3 text-[var(--muted-foreground)]">
                                    {check.message}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}

                      {/* Summary */}
                      {result.quality_report.summary && (
                        <div className="rounded-lg border border-[var(--border)] p-4">
                          <h3 className="text-sm font-semibold mb-2">Resumo</h3>
                          <p className="text-sm text-[var(--muted-foreground)] whitespace-pre-wrap">
                            {result.quality_report.summary}
                          </p>
                        </div>
                      )}
                    </>
                  ) : (
                    <p className="text-sm text-[var(--muted-foreground)]">
                      Relatorio de qualidade nao disponivel.
                    </p>
                  )}
                </div>
              )}

              {/* Tab: Historico */}
              {activeTab === "historico" && (
                <div className="space-y-2">
                  {loadingRuns ? (
                    <p className="text-sm text-[var(--muted-foreground)]">Carregando...</p>
                  ) : runs.length === 0 ? (
                    <p className="text-sm text-[var(--muted-foreground)]">Nenhuma execucao anterior.</p>
                  ) : (
                    runs.map((run) => (
                      <button
                        key={run.id}
                        onClick={() => loadRunDetail(run.id)}
                        disabled={loadingRunDetail}
                        className="w-full flex items-center justify-between p-3 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:bg-[var(--secondary)] transition-colors text-left"
                      >
                        <div>
                          <div className="text-sm font-medium">
                            Pipeline v{run.version}
                          </div>
                          <div className="text-xs text-[var(--muted-foreground)]">
                            {new Date(run.created_at).toLocaleString("pt-BR")}
                          </div>
                        </div>
                        <span
                          className={`text-xs font-bold px-2 py-0.5 rounded ${
                            run.status === "completed"
                              ? "bg-green-500/10 text-green-500"
                              : run.status === "failed"
                              ? "bg-red-500/10 text-red-500"
                              : "bg-yellow-500/10 text-yellow-500"
                          }`}
                        >
                          {run.status}
                        </span>
                      </button>
                    ))
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Utility                                                            */
/* ------------------------------------------------------------------ */

function formatDate(dateStr: string): string {
  if (!dateStr || dateStr === "Sem data") return dateStr;
  try {
    const d = new Date(dateStr + "T00:00:00");
    const weekday = d.toLocaleDateString("pt-BR", { weekday: "long" });
    const formatted = d.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
    });
    return `${weekday}, ${formatted}`;
  } catch {
    return dateStr;
  }
}
