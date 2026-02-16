interface EventCardProps {
  title: string;
  platform: string;
  scheduledAt: string;
  status: string;
  onEdit?: () => void;
}

export function EventCard({ title, platform, scheduledAt, status, onEdit }: EventCardProps) {
  const date = new Date(scheduledAt);
  const time = date.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });

  return (
    <div
      className="p-2 rounded text-xs border border-[var(--border)] bg-[var(--card)] cursor-pointer hover:border-[var(--primary)] transition-colors"
      onClick={onEdit}
    >
      <div className="flex items-center gap-1">
        <span className="font-medium truncate">{title}</span>
      </div>
      <div className="flex items-center gap-1 mt-1 text-[var(--muted-foreground)]">
        <span>{time}</span>
        <span className="capitalize">{platform}</span>
      </div>
    </div>
  );
}
