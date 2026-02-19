"use client";

import { useEffect, useState, useCallback } from "react";
import { Menu, X, Plus } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  agent_type?: string;
}

interface Conversation {
  id: string;
  first_message: string;
  created_at: string;
  agent_type?: string;
  updated_at: string;
}

interface ConversationHistoryProps {
  activeConversationId: string | null;
  onSelectConversation: (id: string, messages: Message[]) => void;
  onNewConversation: () => void;
  refreshTrigger?: number;
}

export function ConversationHistory({
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  refreshTrigger = 0,
}: ConversationHistoryProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  const fetchConversations = useCallback(async () => {
    try {
      const res = await fetch("/api/chat/conversations");
      if (res.ok) {
        const data = await res.json();
        setConversations(data.conversations || []);
      }
    } catch (error) {
      console.error("Failed to fetch conversations:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations, refreshTrigger]);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth >= 768) {
        setIsOpen(true);
      }
    };
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const handleSelectConversation = async (id: string) => {
    try {
      const res = await fetch(`/api/chat/conversations/${id}/messages`);
      if (res.ok) {
        const data = await res.json();
        const messages: Message[] = (data.messages || []).map((msg: any) => ({
          role: msg.role,
          content: msg.content,
          timestamp: new Date(msg.created_at),
          agent_type: msg.agent_type,
        }));
        onSelectConversation(id, messages);
        if (isMobile) setIsOpen(false);
      }
    } catch (error) {
      console.error("Failed to load conversation:", error);
    }
  };

  const handleNewConversation = () => {
    onNewConversation();
    if (isMobile) setIsOpen(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Agora";
    if (diffMins < 60) return `${diffMins}m atrás`;
    if (diffHours < 24) return `${diffHours}h atrás`;
    if (diffDays < 7) return `${diffDays}d atrás`;
    return date.toLocaleDateString("pt-BR", { day: "2-digit", month: "short" });
  };

  const truncateMessage = (msg: string, maxLength: number = 50) => {
    if (msg.length <= maxLength) return msg;
    return msg.substring(0, maxLength) + "...";
  };

  return (
    <>
      {isMobile && (
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="fixed top-4 left-4 z-50 p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] text-[var(--foreground)] hover:bg-[var(--secondary)] transition-colors md:hidden"
          aria-label={isOpen ? "Fechar histórico" : "Abrir histórico"}
        >
          {isOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      )}

      <div
        className={`
          ${isMobile ? "fixed inset-y-0 left-0 z-40" : "relative"}
          w-72 bg-[var(--card)] border-r border-[var(--border)] flex flex-col
          transition-transform duration-300
          ${isMobile && !isOpen ? "-translate-x-full" : "translate-x-0"}
        `}
      >
        <div className="p-4 border-b border-[var(--border)]">
          <button
            onClick={handleNewConversation}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-[var(--primary)] text-white font-medium hover:opacity-90 transition-opacity"
          >
            <Plus size={18} />
            Nova conversa
          </button>
        </div>

        <div className="flex-1 overflow-y-auto">
          {isLoading ? (
            <div className="p-4 text-center text-sm text-[var(--muted-foreground)]">
              Carregando...
            </div>
          ) : conversations.length === 0 ? (
            <div className="p-4 text-center text-sm text-[var(--muted-foreground)]">
              Nenhuma conversa ainda
            </div>
          ) : (
            <div className="space-y-1 p-2">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => handleSelectConversation(conv.id)}
                  className={`
                    w-full text-left p-3 rounded-lg transition-colors
                    ${
                      activeConversationId === conv.id
                        ? "bg-[var(--secondary)] border border-[var(--primary)]"
                        : "hover:bg-[var(--secondary)] border border-transparent"
                    }
                  `}
                >
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <p className="text-sm text-[var(--foreground)] line-clamp-2 flex-1">
                      {truncateMessage(conv.first_message)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-[var(--muted-foreground)]">
                      {formatDate(conv.created_at)}
                    </span>
                    {conv.agent_type && (
                      <span className="px-2 py-0.5 text-xs rounded-full bg-[var(--primary)]/20 text-[var(--primary)] border border-[var(--primary)]/30">
                        {conv.agent_type}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {isMobile && isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
