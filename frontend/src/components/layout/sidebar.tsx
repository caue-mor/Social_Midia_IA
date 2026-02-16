"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/components/auth/auth-provider";

const navItems = [
  { label: "Dashboard", href: "/", icon: "🏠" },
  { label: "Chat IA", href: "/chat", icon: "💬" },
  { label: "Conteudo", href: "/content", icon: "✍️" },
  { label: "Analise", href: "/analysis", icon: "📊" },
  { label: "Calendario", href: "/calendar", icon: "📅" },
  { label: "Relatorios", href: "/reports", icon: "📈" },
  { label: "Configuracoes", href: "/settings", icon: "⚙️" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, signOut } = useAuth();

  return (
    <aside className="w-64 border-r border-[var(--border)] bg-[var(--card)] flex flex-col">
      <div className="p-4 border-b border-[var(--border)]">
        <h2 className="text-lg font-bold text-[var(--primary)]">AgenteSocial</h2>
        <p className="text-xs text-[var(--muted-foreground)]">IA para Redes Sociais</p>
      </div>

      <nav className="flex-1 p-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors mb-1 ${
                isActive
                  ? "bg-[var(--primary)] text-white"
                  : "text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--secondary)]"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-[var(--border)]">
        {user && (
          <div className="mb-2">
            <p className="text-xs text-[var(--muted-foreground)] truncate">{user.email}</p>
            <button
              onClick={signOut}
              className="text-xs text-red-500 hover:underline mt-1"
            >
              Sair
            </button>
          </div>
        )}
        <p className="text-xs text-[var(--muted-foreground)]">v0.1.0</p>
      </div>
    </aside>
  );
}
