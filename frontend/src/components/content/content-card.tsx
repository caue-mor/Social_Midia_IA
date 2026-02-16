interface ContentCardProps {
  title?: string;
  body: string;
  platform: string;
  contentType: string;
  status: string;
  createdAt: string;
  onEdit?: () => void;
}

const platformColors: Record<string, string> = {
  instagram: "bg-pink-100 text-pink-700",
  youtube: "bg-red-100 text-red-700",
  tiktok: "bg-gray-100 text-gray-700",
  linkedin: "bg-blue-100 text-blue-700",
};

const statusColors: Record<string, string> = {
  draft: "bg-yellow-100 text-yellow-700",
  scheduled: "bg-blue-100 text-blue-700",
  published: "bg-green-100 text-green-700",
  archived: "bg-gray-100 text-gray-500",
};

export function ContentCard({ title, body, platform, contentType, status, createdAt, onEdit }: ContentCardProps) {
  return (
    <div className="p-4 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:border-[var(--primary)] transition-colors">
      <div className="flex items-center gap-2 mb-2">
        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${platformColors[platform] || "bg-gray-100 text-gray-700"}`}>
          {platform}
        </span>
        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[status] || ""}`}>
          {status}
        </span>
        <span className="text-xs text-[var(--muted-foreground)] ml-auto">
          {contentType}
        </span>
      </div>
      {title && <h3 className="font-medium text-sm mb-1">{title}</h3>}
      <p className="text-sm text-[var(--muted-foreground)] line-clamp-3">{body}</p>
      <div className="flex items-center justify-between mt-3">
        <span className="text-xs text-[var(--muted-foreground)]">
          {new Date(createdAt).toLocaleDateString("pt-BR")}
        </span>
        {onEdit && (
          <button
            onClick={onEdit}
            className="text-xs text-[var(--primary)] hover:underline"
          >
            Editar
          </button>
        )}
      </div>
    </div>
  );
}
