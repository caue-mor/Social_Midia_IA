"use client";

import { useState, useEffect, useCallback } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import ReactMarkdown from "react-markdown";

const REPORT_TYPES = [
  { value: "weekly", label: "Semanal" },
  { value: "monthly", label: "Mensal" },
  { value: "quarterly", label: "Trimestral" },
  { value: "custom", label: "Personalizado" },
];

const SECTIONS = [
  { value: "overview", label: "Resumo Executivo" },
  { value: "content", label: "Performance de Conteudo" },
  { value: "engagement", label: "Metricas de Engajamento" },
  { value: "growth", label: "Analise de Crescimento" },
  { value: "top_content", label: "Top Conteudos" },
  { value: "recommendations", label: "Recomendacoes" },
];

interface Report {
  id: string;
  type: string;
  title: string;
  content: string;
  period_start?: string;
  period_end?: string;
  sections?: string[];
  created_at: string;
}

// Mock chart data to show when no real analytics data is available
const MOCK_CHART_DATA = [
  { name: "Posts", value: 0 },
  { name: "Reels", value: 0 },
  { name: "Stories", value: 0 },
  { name: "Carrosseis", value: 0 },
  { name: "Videos", value: 0 },
];

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [view, setView] = useState<"list" | "detail" | "generate">("list");

  // Generate form state
  const [reportType, setReportType] = useState("weekly");
  const [periodStart, setPeriodStart] = useState("");
  const [periodEnd, setPeriodEnd] = useState("");
  const [selectedSections, setSelectedSections] = useState<string[]>([
    "overview",
    "content",
    "engagement",
    "growth",
    "top_content",
    "recommendations",
  ]);

  const fetchReports = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/reports");
      if (res.ok) {
        const data = await res.json();
        setReports(data.reports || []);
      }
    } catch {
      // silent fail
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  // Set default period dates
  useEffect(() => {
    const now = new Date();
    const end = now.toISOString().split("T")[0];
    const start = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0];
    setPeriodStart(start);
    setPeriodEnd(end);
  }, []);

  const toggleSection = (section: string) => {
    setSelectedSections((prev) =>
      prev.includes(section)
        ? prev.filter((s) => s !== section)
        : [...prev, section]
    );
  };

  const generateReport = async () => {
    if (!periodStart || !periodEnd) return;
    setGenerating(true);
    try {
      const res = await fetch("/api/reports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          report_type: reportType,
          period_start: periodStart,
          period_end: periodEnd,
          include_sections: selectedSections,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.report) {
          setSelectedReport(data.report);
          setView("detail");
        } else if (data.response) {
          // Fallback if report was not saved
          setSelectedReport({
            id: "temp",
            type: reportType,
            title: `Relatorio ${reportType} - ${periodStart} a ${periodEnd}`,
            content: data.response,
            period_start: periodStart,
            period_end: periodEnd,
            sections: selectedSections,
            created_at: new Date().toISOString(),
          });
          setView("detail");
        }
        fetchReports();
      }
    } catch {
      // silent fail
    } finally {
      setGenerating(false);
    }
  };

  const deleteReport = async (reportId: string) => {
    try {
      const res = await fetch(`/api/reports?id=${reportId}`, { method: "DELETE" });
      if (res.ok) {
        setReports((prev) => prev.filter((r) => r.id !== reportId));
        if (selectedReport?.id === reportId) {
          setSelectedReport(null);
          setView("list");
        }
      }
    } catch {
      // silent fail
    }
  };

  const openReport = async (report: Report) => {
    // If content is already present, show directly
    if (report.content) {
      setSelectedReport(report);
      setView("detail");
      return;
    }
    // Fetch full report
    try {
      const res = await fetch(`/api/reports?id=${report.id}`);
      if (res.ok) {
        const data = await res.json();
        setSelectedReport(data.report || report);
        setView("detail");
      }
    } catch {
      setSelectedReport(report);
      setView("detail");
    }
  };

  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
    } catch {
      return dateStr;
    }
  };

  const typeLabel = (type: string) => {
    return REPORT_TYPES.find((t) => t.value === type)?.label || type;
  };

  // --- DETAIL VIEW ---
  if (view === "detail" && selectedReport) {
    return (
      <div className="p-8">
        <button
          onClick={() => { setView("list"); setSelectedReport(null); }}
          className="mb-4 text-sm text-[var(--primary)] hover:underline"
        >
          &larr; Voltar para lista
        </button>

        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold">{selectedReport.title}</h1>
            <p className="text-sm text-[var(--muted-foreground)] mt-1">
              {typeLabel(selectedReport.type)} | Criado em {formatDate(selectedReport.created_at)}
            </p>
          </div>
          {selectedReport.id !== "temp" && (
            <button
              onClick={() => deleteReport(selectedReport.id)}
              className="px-3 py-1 text-sm rounded-lg border border-red-300 text-red-600 hover:bg-red-50 transition-colors"
            >
              Excluir
            </button>
          )}
        </div>

        {/* Content performance chart */}
        <div className="mb-8 p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <h3 className="text-sm font-semibold mb-3">Performance por Tipo de Conteudo</h3>
          <div style={{ width: "100%", height: 220 }}>
            <ResponsiveContainer>
              <BarChart data={MOCK_CHART_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} stroke="var(--muted-foreground)" />
                <YAxis tick={{ fontSize: 12 }} stroke="var(--muted-foreground)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "var(--card)",
                    border: "1px solid var(--border)",
                    borderRadius: "8px",
                    fontSize: "12px",
                  }}
                />
                <Bar dataKey="value" fill="var(--primary)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-xs text-[var(--muted-foreground)] mt-2">
            Os dados do grafico serao preenchidos automaticamente conforme voce publica conteudo.
          </p>
        </div>

        {/* Report markdown content */}
        <div className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)] prose prose-sm max-w-none">
          <ReactMarkdown>{selectedReport.content || "Nenhum conteudo disponivel."}</ReactMarkdown>
        </div>
      </div>
    );
  }

  // --- GENERATE VIEW ---
  if (view === "generate") {
    return (
      <div className="p-8">
        <button
          onClick={() => setView("list")}
          className="mb-4 text-sm text-[var(--primary)] hover:underline"
        >
          &larr; Voltar para lista
        </button>

        <h1 className="text-2xl font-bold mb-6">Gerar Novo Relatorio</h1>

        <div className="max-w-2xl space-y-6">
          {/* Report type */}
          <div>
            <label className="block text-sm font-medium mb-2">Tipo de Relatorio</label>
            <div className="flex gap-2">
              {REPORT_TYPES.map((t) => (
                <button
                  key={t.value}
                  onClick={() => setReportType(t.value)}
                  className={`px-4 py-2 rounded-lg border text-sm transition-colors ${
                    reportType === t.value
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          {/* Date range */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Periodo Inicio</label>
              <input
                type="date"
                value={periodStart}
                onChange={(e) => setPeriodStart(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Periodo Fim</label>
              <input
                type="date"
                value={periodEnd}
                onChange={(e) => setPeriodEnd(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
            </div>
          </div>

          {/* Sections */}
          <div>
            <label className="block text-sm font-medium mb-2">Secoes do Relatorio</label>
            <div className="grid grid-cols-2 gap-2">
              {SECTIONS.map((s) => (
                <button
                  key={s.value}
                  onClick={() => toggleSection(s.value)}
                  className={`px-3 py-2 rounded-lg border text-sm text-left transition-colors ${
                    selectedSections.includes(s.value)
                      ? "border-[var(--primary)] bg-[var(--primary)]/10"
                      : "border-[var(--border)] hover:border-[var(--primary)]"
                  }`}
                >
                  <span className="mr-2">{selectedSections.includes(s.value) ? "V" : " "}</span>
                  {s.label}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={generateReport}
            disabled={generating || !periodStart || !periodEnd || selectedSections.length === 0}
            className="w-full py-3 rounded-lg bg-[var(--primary)] text-white font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
          >
            {generating ? "Gerando relatorio com IA..." : "Gerar Relatorio"}
          </button>
        </div>
      </div>
    );
  }

  // --- LIST VIEW ---
  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Relatorios</h1>
          <p className="text-sm text-[var(--muted-foreground)] mt-1">
            {reports.length} relatorio{reports.length !== 1 ? "s" : ""} gerado{reports.length !== 1 ? "s" : ""}
          </p>
        </div>
        <button
          onClick={() => setView("generate")}
          className="px-4 py-2 rounded-lg bg-[var(--primary)] text-white text-sm font-medium hover:opacity-90 transition-opacity"
        >
          Gerar Novo Relatorio
        </button>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <p className="text-sm text-[var(--muted-foreground)]">Relatorios Gerados</p>
          <p className="text-2xl font-bold mt-1">{reports.length}</p>
        </div>
        <div className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <p className="text-sm text-[var(--muted-foreground)]">Ultimo Relatorio</p>
          <p className="text-2xl font-bold mt-1">
            {reports.length > 0 ? formatDate(reports[0].created_at) : "--"}
          </p>
        </div>
        <div className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <p className="text-sm text-[var(--muted-foreground)]">Tipos</p>
          <p className="text-2xl font-bold mt-1">
            {new Set(reports.map((r) => r.type)).size || 0}
          </p>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="text-sm text-[var(--muted-foreground)] mb-4">Carregando relatorios...</div>
      )}

      {/* Reports list */}
      {reports.length > 0 ? (
        <div className="space-y-3">
          {reports.map((report) => (
            <div
              key={report.id}
              className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:border-[var(--primary)]/50 transition-colors cursor-pointer"
              onClick={() => openReport(report)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium truncate">{report.title}</h3>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--primary)]/10 text-[var(--primary)]">
                      {typeLabel(report.type)}
                    </span>
                    <span className="text-xs text-[var(--muted-foreground)]">
                      {formatDate(report.created_at)}
                    </span>
                    {report.period_start && report.period_end && (
                      <span className="text-xs text-[var(--muted-foreground)]">
                        {report.period_start} a {report.period_end}
                      </span>
                    )}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteReport(report.id);
                  }}
                  className="ml-4 text-xs text-[var(--muted-foreground)] hover:text-red-500 transition-colors"
                >
                  Excluir
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        !loading && (
          <div className="p-8 rounded-lg border border-[var(--border)] bg-[var(--card)] text-center">
            <p className="text-[var(--muted-foreground)] mb-4">
              Nenhum relatorio gerado ainda. Use a IA para gerar seu primeiro relatorio de performance.
            </p>
            <button
              onClick={() => setView("generate")}
              className="inline-block px-4 py-2 rounded-lg bg-[var(--primary)] text-white text-sm"
            >
              Gerar Primeiro Relatorio
            </button>
          </div>
        )
      )}
    </div>
  );
}
