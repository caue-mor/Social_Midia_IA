"use client";

import { useState, useEffect, useCallback } from "react";

const DAY_LABELS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];

const PLATFORM_COLORS: Record<string, { bg: string; text: string; dot: string }> = {
  instagram: { bg: "bg-pink-100", text: "text-pink-800", dot: "bg-pink-500" },
  youtube: { bg: "bg-red-100", text: "text-red-800", dot: "bg-red-500" },
  tiktok: { bg: "bg-gray-900", text: "text-white", dot: "bg-gray-900" },
  linkedin: { bg: "bg-blue-100", text: "text-blue-800", dot: "bg-blue-500" },
};

const STATUS_BADGES: Record<string, { label: string; cls: string }> = {
  scheduled: { label: "Agendado", cls: "bg-blue-100 text-blue-700" },
  published: { label: "Publicado", cls: "bg-green-100 text-green-700" },
  draft: { label: "Rascunho", cls: "bg-yellow-100 text-yellow-700" },
};

const PLATFORMS = [
  { value: "instagram", label: "Instagram" },
  { value: "youtube", label: "YouTube" },
  { value: "tiktok", label: "TikTok" },
  { value: "linkedin", label: "LinkedIn" },
];

interface CalendarEvent {
  id: string;
  title: string;
  platform: string;
  scheduled_at: string;
  status: string;
  notes?: string;
  content_id?: string;
}

export default function CalendarPage() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedDay, setSelectedDay] = useState<number | null>(null);
  const [generating, setGenerating] = useState(false);
  const [planResult, setPlanResult] = useState("");

  // New event form state
  const [newTitle, setNewTitle] = useState("");
  const [newPlatform, setNewPlatform] = useState("instagram");
  const [newTime, setNewTime] = useState("12:00");
  const [newStatus, setNewStatus] = useState("scheduled");
  const [newNotes, setNewNotes] = useState("");

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const monthKey = `${year}-${String(month + 1).padStart(2, "0")}`;
  const monthName = currentDate.toLocaleDateString("pt-BR", { month: "long", year: "numeric" });

  const fetchEvents = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/calendar?month=${monthKey}`);
      if (res.ok) {
        const data = await res.json();
        setEvents(data.events || []);
      }
    } catch {
      // silent fail
    } finally {
      setLoading(false);
    }
  }, [monthKey]);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  const goToPrevMonth = () => {
    setCurrentDate(new Date(year, month - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(year, month + 1, 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const openNewEventModal = (day: number) => {
    setSelectedDay(day);
    setNewTitle("");
    setNewPlatform("instagram");
    setNewTime("12:00");
    setNewStatus("scheduled");
    setNewNotes("");
    setShowModal(true);
  };

  const createEvent = async () => {
    if (!newTitle.trim() || selectedDay === null) return;
    const scheduledAt = `${year}-${String(month + 1).padStart(2, "0")}-${String(selectedDay).padStart(2, "0")}T${newTime}:00`;
    try {
      const res = await fetch("/api/calendar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: newTitle,
          platform: newPlatform,
          scheduled_at: scheduledAt,
          status: newStatus,
          notes: newNotes || null,
        }),
      });
      if (res.ok) {
        setShowModal(false);
        fetchEvents();
      }
    } catch {
      // silent fail
    }
  };

  const deleteEvent = async (eventId: string) => {
    try {
      const res = await fetch(`/api/calendar?eventId=${eventId}`, { method: "DELETE" });
      if (res.ok) {
        fetchEvents();
      }
    } catch {
      // silent fail
    }
  };

  const generatePlan = async () => {
    setGenerating(true);
    setPlanResult("");
    try {
      const res = await fetch("/api/calendar/generate-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ period: "weekly", platforms: ["instagram", "youtube", "tiktok", "linkedin"] }),
      });
      if (res.ok) {
        const data = await res.json();
        setPlanResult(data.response || "Plano gerado com sucesso. Recarregue para ver os eventos.");
        fetchEvents();
      } else {
        setPlanResult("Erro ao gerar plano editorial.");
      }
    } catch {
      setPlanResult("Erro de conexao ao gerar plano.");
    } finally {
      setGenerating(false);
    }
  };

  const getEventsForDay = (day: number): CalendarEvent[] => {
    const dayStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    return events.filter((e) => e.scheduled_at?.startsWith(dayStr));
  };

  const today = new Date();
  const isCurrentMonth = month === today.getMonth() && year === today.getFullYear();

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Calendario Editorial</h1>
          <p className="text-sm text-[var(--muted-foreground)] mt-1">
            {events.length} evento{events.length !== 1 ? "s" : ""} neste mes
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={generatePlan}
            disabled={generating}
            className="px-4 py-2 rounded-lg bg-[var(--primary)] text-white text-sm font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
          >
            {generating ? "Gerando..." : "Gerar Plano Editorial"}
          </button>
        </div>
      </div>

      {/* Plan result banner */}
      {planResult && (
        <div className="mb-6 p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium">Resultado do Plano Editorial</p>
            <button
              onClick={() => setPlanResult("")}
              className="text-xs text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
            >
              Fechar
            </button>
          </div>
          <p className="text-sm whitespace-pre-wrap text-[var(--muted-foreground)]">{planResult}</p>
        </div>
      )}

      {/* Month navigation */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <button
            onClick={goToPrevMonth}
            className="px-3 py-1 rounded-lg border border-[var(--border)] text-sm hover:bg-[var(--secondary)] transition-colors"
          >
            &larr;
          </button>
          <button
            onClick={goToToday}
            className="px-3 py-1 rounded-lg border border-[var(--border)] text-sm hover:bg-[var(--secondary)] transition-colors"
          >
            Hoje
          </button>
          <button
            onClick={goToNextMonth}
            className="px-3 py-1 rounded-lg border border-[var(--border)] text-sm hover:bg-[var(--secondary)] transition-colors"
          >
            &rarr;
          </button>
        </div>
        <p className="text-lg font-semibold capitalize">{monthName}</p>
      </div>

      {/* Loading indicator */}
      {loading && (
        <div className="mb-4 text-sm text-[var(--muted-foreground)]">Carregando eventos...</div>
      )}

      {/* Calendar grid */}
      <div className="grid grid-cols-7 gap-1">
        {/* Day headers */}
        {DAY_LABELS.map((day) => (
          <div key={day} className="p-2 text-center text-xs font-semibold text-[var(--muted-foreground)] uppercase">
            {day}
          </div>
        ))}

        {/* Empty cells before first day */}
        {Array.from({ length: firstDay }).map((_, i) => (
          <div key={`empty-${i}`} className="min-h-[100px] p-2 rounded-lg bg-[var(--secondary)]/30" />
        ))}

        {/* Day cells */}
        {Array.from({ length: daysInMonth }).map((_, i) => {
          const day = i + 1;
          const isToday = isCurrentMonth && day === today.getDate();
          const dayEvents = getEventsForDay(day);

          return (
            <div
              key={day}
              onClick={() => openNewEventModal(day)}
              className={`min-h-[100px] p-2 rounded-lg border text-sm cursor-pointer transition-colors group ${
                isToday
                  ? "border-[var(--primary)] bg-[var(--primary)]/5"
                  : "border-[var(--border)] hover:border-[var(--primary)]/50"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span
                  className={`text-xs font-semibold ${
                    isToday
                      ? "bg-[var(--primary)] text-white w-5 h-5 rounded-full flex items-center justify-center"
                      : "text-[var(--foreground)]"
                  }`}
                >
                  {day}
                </span>
                <span className="text-xs text-[var(--muted-foreground)] opacity-0 group-hover:opacity-100 transition-opacity">
                  +
                </span>
              </div>

              {/* Events for this day */}
              <div className="space-y-1">
                {dayEvents.slice(0, 3).map((evt) => {
                  const colors = PLATFORM_COLORS[evt.platform] || PLATFORM_COLORS.instagram;
                  return (
                    <div
                      key={evt.id}
                      className={`px-1.5 py-0.5 rounded text-[10px] leading-tight truncate ${colors.bg} ${colors.text}`}
                      title={`${evt.title} (${evt.platform}) - ${evt.status}`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      {evt.title}
                    </div>
                  );
                })}
                {dayEvents.length > 3 && (
                  <p className="text-[10px] text-[var(--muted-foreground)]">
                    +{dayEvents.length - 3} mais
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Platform legend */}
      <div className="flex items-center gap-4 mt-4 pt-4 border-t border-[var(--border)]">
        <span className="text-xs text-[var(--muted-foreground)]">Plataformas:</span>
        {Object.entries(PLATFORM_COLORS).map(([name, colors]) => (
          <div key={name} className="flex items-center gap-1.5">
            <span className={`w-2.5 h-2.5 rounded-full ${colors.dot}`} />
            <span className="text-xs capitalize">{name}</span>
          </div>
        ))}
      </div>

      {/* New Event Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="w-full max-w-md mx-4 p-6 rounded-xl bg-[var(--card)] border border-[var(--border)] shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">
                Novo Evento - {selectedDay}/{month + 1}/{year}
              </h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-[var(--muted-foreground)] hover:text-[var(--foreground)] text-xl leading-none"
              >
                &times;
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Titulo</label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="Ex: Post sobre dicas de marketing"
                  className="w-full px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Plataforma</label>
                <div className="flex gap-2">
                  {PLATFORMS.map((p) => {
                    const colors = PLATFORM_COLORS[p.value] || PLATFORM_COLORS.instagram;
                    return (
                      <button
                        key={p.value}
                        onClick={() => setNewPlatform(p.value)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs transition-colors ${
                          newPlatform === p.value
                            ? "border-[var(--primary)] bg-[var(--primary)]/10"
                            : "border-[var(--border)] hover:border-[var(--primary)]"
                        }`}
                      >
                        <span className={`w-2 h-2 rounded-full ${colors.dot}`} />
                        {p.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Horario</label>
                  <input
                    type="time"
                    value={newTime}
                    onChange={(e) => setNewTime(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Status</label>
                  <select
                    value={newStatus}
                    onChange={(e) => setNewStatus(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                  >
                    <option value="scheduled">Agendado</option>
                    <option value="draft">Rascunho</option>
                    <option value="published">Publicado</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Notas (opcional)</label>
                <textarea
                  value={newNotes}
                  onChange={(e) => setNewNotes(e.target.value)}
                  placeholder="Anotacoes sobre o conteudo..."
                  rows={2}
                  className="w-full px-3 py-2 rounded-lg bg-[var(--secondary)] border border-[var(--border)] text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                />
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => setShowModal(false)}
                  className="flex-1 py-2 rounded-lg border border-[var(--border)] text-sm font-medium hover:bg-[var(--secondary)] transition-colors"
                >
                  Cancelar
                </button>
                <button
                  onClick={createEvent}
                  disabled={!newTitle.trim()}
                  className="flex-1 py-2 rounded-lg bg-[var(--primary)] text-white text-sm font-medium disabled:opacity-50 hover:opacity-90 transition-opacity"
                >
                  Criar Evento
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
