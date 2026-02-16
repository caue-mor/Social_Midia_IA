"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { ContentPiece } from "@/types";
import { format, subDays, startOfDay } from "date-fns";
import { ptBR } from "date-fns/locale";

interface ContentChartProps {
  content: ContentPiece[];
}

export function ContentChart({ content }: ContentChartProps) {
  // Generate data for last 7 days
  const chartData = Array.from({ length: 7 }, (_, i) => {
    const date = startOfDay(subDays(new Date(), 6 - i));
    const dateStr = format(date, "yyyy-MM-dd");
    const count = content.filter((item) => {
      const itemDate = format(new Date(item.created_at), "yyyy-MM-dd");
      return itemDate === dateStr;
    }).length;

    return {
      date: format(date, "dd MMM", { locale: ptBR }),
      count,
    };
  });

  return (
    <div className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
      <h3 className="text-lg font-semibold mb-4">Conteudos Criados (7 dias)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
          <XAxis
            dataKey="date"
            tick={{ fill: "var(--muted-foreground)", fontSize: 12 }}
            stroke="var(--border)"
          />
          <YAxis
            tick={{ fill: "var(--muted-foreground)", fontSize: 12 }}
            stroke="var(--border)"
            allowDecimals={false}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              color: "var(--foreground)",
            }}
            labelStyle={{ color: "var(--foreground)" }}
          />
          <Bar dataKey="count" fill="var(--primary)" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
