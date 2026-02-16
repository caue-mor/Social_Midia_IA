"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { ContentPiece } from "@/types";

interface PlatformChartProps {
  content: ContentPiece[];
}

const PLATFORM_COLORS: Record<string, string> = {
  instagram: "#E1306C",
  youtube: "#FF0000",
  tiktok: "#000000",
  linkedin: "#0077B5",
  twitter: "#1DA1F2",
  facebook: "#1877F2",
};

export function PlatformChart({ content }: PlatformChartProps) {
  // Aggregate content by platform
  const platformCounts = content.reduce((acc, item) => {
    const platform = item.platform.toLowerCase();
    acc[platform] = (acc[platform] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const chartData = Object.entries(platformCounts).map(([platform, count]) => ({
    name: platform.charAt(0).toUpperCase() + platform.slice(1),
    value: count,
    color: PLATFORM_COLORS[platform] || "var(--primary)",
  }));

  if (chartData.length === 0) {
    return (
      <div className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
        <h3 className="text-lg font-semibold mb-4">Distribuicao por Plataforma</h3>
        <div className="flex items-center justify-center h-[300px] text-[var(--muted-foreground)]">
          Sem dados para exibir
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 rounded-lg border border-[var(--border)] bg-[var(--card)]">
      <h3 className="text-lg font-semibold mb-4">Distribuicao por Plataforma</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="var(--primary)"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              color: "var(--foreground)",
            }}
          />
          <Legend
            wrapperStyle={{ color: "var(--foreground)" }}
            iconType="circle"
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
