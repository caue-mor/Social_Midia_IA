"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { format } from "date-fns";
import { StatsCard } from "@/components/dashboard/stats-card";
import { ContentChart } from "@/components/dashboard/content-chart";
import { PlatformChart } from "@/components/dashboard/platform-chart";
import { ContentPiece, CalendarEvent } from "@/types";

const quickActions = [
  { title: "Chat com IA", description: "Converse com o assistente", href: "/chat", icon: "💬" },
  { title: "Criar Conteudo", description: "Gere posts e legendas", href: "/content", icon: "✍️" },
  { title: "Analise de Perfil", description: "Analise suas redes", href: "/analysis", icon: "📊" },
  { title: "Calendario", description: "Planeje publicacoes", href: "/calendar", icon: "📅" },
  { title: "Relatorios", description: "Performance e metricas", href: "/reports", icon: "📈" },
  { title: "Configuracoes", description: "Perfis e preferencias", href: "/settings", icon: "⚙️" },
];

interface DashboardStats {
  totalContent: number;
  scheduledEvents: number;
  publishedContent: number;
  engagementRate: string;
}

export default function HomePage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalContent: 0,
    scheduledEvents: 0,
    publishedContent: 0,
    engagementRate: "--",
  });
  const [content, setContent] = useState<ContentPiece[]>([]);
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        setLoading(true);
        setError(null);

        // Fetch content library
        const contentRes = await fetch("/api/content");
        if (!contentRes.ok) {
          throw new Error("Falha ao carregar conteudos");
        }
        const contentData = await contentRes.json();
        const allContent: ContentPiece[] = contentData.content || [];

        // Fetch calendar events for current month
        const currentMonth = format(new Date(), "yyyy-MM");
        const eventsRes = await fetch(`/api/calendar?month=${currentMonth}`);
        if (!eventsRes.ok) {
          throw new Error("Falha ao carregar eventos");
        }
        const eventsData = await eventsRes.json();
        const allEvents: CalendarEvent[] = eventsData.events || [];

        // Calculate stats
        const publishedCount = allContent.filter(
          (item) => item.status.toLowerCase() === "published"
        ).length;

        const scheduledCount = allEvents.filter(
          (event) => event.status.toLowerCase() === "scheduled"
        ).length;

        setContent(allContent);
        setEvents(allEvents);
        setStats({
          totalContent: allContent.length,
          scheduledEvents: scheduledCount,
          publishedContent: publishedCount,
          engagementRate: "--", // TODO: Fetch from analytics when available
        });
      } catch (err) {
        console.error("Dashboard data fetch error:", err);
        setError(err instanceof Error ? err.message : "Erro ao carregar dados");
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  // Get recent content (last 5)
  const recentContent = content
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  // Get upcoming events (next 5)
  const upcomingEvents = events
    .filter((event) => new Date(event.scheduled_at) >= new Date())
    .sort((a, b) => new Date(a.scheduled_at).getTime() - new Date(b.scheduled_at).getTime())
    .slice(0, 5);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold">AgenteSocial</h1>
        <p className="text-[var(--muted-foreground)] mt-2">
          Seu ecossistema de IA para gestao completa de redes sociais
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <StatsCard
          title="Conteudos Gerados"
          value={loading ? "..." : stats.totalContent}
          description={error ? "Conecte-se" : "Total"}
        />
        <StatsCard
          title="Agendados"
          value={loading ? "..." : stats.scheduledEvents}
          description={error ? "Conecte-se" : "Este mes"}
        />
        <StatsCard
          title="Publicados"
          value={loading ? "..." : stats.publishedContent}
          description={error ? "Conecte-se" : "Este mes"}
        />
        <StatsCard
          title="Engajamento"
          value={`${stats.engagementRate}%`}
          description="Conecte um perfil"
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-8 p-4 rounded-lg bg-red-50 border border-red-200 text-red-800">
          <p className="text-sm font-medium">Erro ao carregar dados</p>
          <p className="text-xs mt-1">{error}</p>
        </div>
      )}

      {/* Charts Section */}
      {!loading && content.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <ContentChart content={content} />
          <PlatformChart content={content} />
        </div>
      )}

      {/* Recent Content Section */}
      {!loading && recentContent.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">Conteudos Recentes</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentContent.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:border-[var(--primary)] transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-[var(--primary)] uppercase">
                    {item.platform}
                  </span>
                  <span
                    className={`text-xs px-2 py-1 rounded-full ${
                      item.status.toLowerCase() === "published"
                        ? "bg-green-100 text-green-800"
                        : item.status.toLowerCase() === "draft"
                        ? "bg-gray-100 text-gray-800"
                        : "bg-yellow-100 text-yellow-800"
                    }`}
                  >
                    {item.status}
                  </span>
                </div>
                {item.title && (
                  <h3 className="font-semibold mb-2 line-clamp-1">{item.title}</h3>
                )}
                <p className="text-sm text-[var(--muted-foreground)] line-clamp-2 mb-2">
                  {item.body}
                </p>
                <p className="text-xs text-[var(--muted-foreground)]">
                  {format(new Date(item.created_at), "dd MMM yyyy, HH:mm")}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upcoming Events Section */}
      {!loading && upcomingEvents.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">Proximos Agendamentos</h2>
          <div className="space-y-3">
            {upcomingEvents.map((event) => (
              <div
                key={event.id}
                className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)] flex items-center justify-between hover:border-[var(--primary)] transition-colors"
              >
                <div className="flex-1">
                  <h3 className="font-semibold mb-1">{event.title}</h3>
                  <div className="flex items-center gap-4 text-sm text-[var(--muted-foreground)]">
                    <span className="uppercase font-medium text-[var(--primary)]">
                      {event.platform}
                    </span>
                    <span>{format(new Date(event.scheduled_at), "dd MMM yyyy, HH:mm")}</span>
                  </div>
                </div>
                <span
                  className={`text-xs px-3 py-1 rounded-full ${
                    event.status.toLowerCase() === "scheduled"
                      ? "bg-blue-100 text-blue-800"
                      : event.status.toLowerCase() === "published"
                      ? "bg-green-100 text-green-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {event.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <h2 className="text-lg font-semibold mb-4">Acoes Rapidas</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {quickActions.map((action) => (
          <Link
            key={action.href}
            href={action.href}
            className="block p-6 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:border-[var(--primary)] transition-colors"
          >
            <span className="text-2xl">{action.icon}</span>
            <h3 className="text-lg font-semibold mt-3">{action.title}</h3>
            <p className="text-sm text-[var(--muted-foreground)] mt-1">
              {action.description}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
