interface StatsCardProps {
  title: string;
  value: string | number;
  description?: string;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
}

export function StatsCard({ title, value, description, trend, trendValue }: StatsCardProps) {
  const trendColor = trend === "up" ? "text-green-500" : trend === "down" ? "text-red-500" : "text-[var(--muted-foreground)]";

  return (
    <div className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)]">
      <p className="text-sm text-[var(--muted-foreground)]">{title}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
      {(description || trendValue) && (
        <p className={`text-xs mt-1 ${trendColor}`}>
          {trendValue && (
            <span>
              {trend === "up" ? "+" : trend === "down" ? "" : ""}{trendValue}{" "}
            </span>
          )}
          {description}
        </p>
      )}
    </div>
  );
}
