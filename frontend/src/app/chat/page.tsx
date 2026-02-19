"use client";

import { useRef, useEffect, useState } from "react";
import { ChatMessage } from "@/components/chat/chat-message";
import { ChatInput } from "@/components/chat/chat-input";
import { ConversationHistory } from "@/components/chat/conversation-history";
import { useChat } from "@/hooks/use-chat";

const suggestions = [
  "Analise meu perfil do Instagram",
  "Crie um post sobre marketing digital",
  "Quais sao as trends de hoje?",
  "Gere um roteiro de podcast",
];

function ConnectionIndicator({
  mode,
  isConnected,
}: {
  mode: "websocket" | "http" | "connecting";
  isConnected: boolean;
}) {
  const dotColor =
    mode === "websocket" && isConnected
      ? "bg-green-500"
      : mode === "http"
        ? "bg-yellow-500"
        : "bg-gray-400";

  const label =
    mode === "websocket" && isConnected
      ? "Tempo real"
      : mode === "http"
        ? "HTTP"
        : "Conectando...";

  return (
    <div className="flex items-center gap-1.5" title={`Modo de conexao: ${label}`}>
      <span className={`inline-block w-2 h-2 rounded-full ${dotColor}`} />
      <span className="text-xs text-[var(--muted-foreground)]">{label}</span>
    </div>
  );
}

export default function ChatPage() {
  const {
    messages,
    sendMessage,
    isLoading,
    isTyping,
    isConnected,
    connectionMode,
    clearMessages,
    loadConversation,
    getCurrentConversationId,
  } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const previousMessageCountRef = useRef(0);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // Trigger refresh when a new conversation is created
  useEffect(() => {
    if (messages.length > previousMessageCountRef.current) {
      const hasNewMessage = messages.length > 0;
      const currentConversationId = getCurrentConversationId();

      // If we have messages and a conversation ID, refresh the sidebar
      if (hasNewMessage && currentConversationId) {
        setRefreshTrigger(prev => prev + 1);
      }
    }
    previousMessageCountRef.current = messages.length;
  }, [messages, getCurrentConversationId]);

  const handleSelectConversation = (id: string, conversationMessages: any[]) => {
    loadConversation(id, conversationMessages);
  };

  const handleNewConversation = () => {
    clearMessages();
  };

  return (
    <div className="flex h-full">
      <ConversationHistory
        activeConversationId={getCurrentConversationId()}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        refreshTrigger={refreshTrigger}
      />

      <div className="flex flex-col flex-1 h-full">
        <div className="p-4 border-b border-[var(--border)] flex items-center justify-between md:ml-0 ml-12">
        <div>
          <h1 className="text-xl font-bold">Chat com IA</h1>
          <p className="text-sm text-[var(--muted-foreground)]">
            Converse com o assistente para criar conteudo, analisar perfis e mais
          </p>
        </div>
        <ConnectionIndicator mode={connectionMode} isConnected={isConnected} />
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <p className="text-4xl mb-4">💬</p>
              <p className="text-[var(--muted-foreground)]">
                Envie uma mensagem para comecar
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <ChatMessage key={i} role={msg.role} content={msg.content} />
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-[var(--secondary)] px-4 py-2 rounded-lg">
              <div className="flex items-center gap-1">
                <span
                  className="w-2 h-2 rounded-full bg-[var(--muted-foreground)] animate-bounce"
                  style={{ animationDelay: "0ms" }}
                />
                <span
                  className="w-2 h-2 rounded-full bg-[var(--muted-foreground)] animate-bounce"
                  style={{ animationDelay: "150ms" }}
                />
                <span
                  className="w-2 h-2 rounded-full bg-[var(--muted-foreground)] animate-bounce"
                  style={{ animationDelay: "300ms" }}
                />
              </div>
            </div>
          </div>
        )}

        {isLoading && !isTyping && (
          <div className="flex justify-start">
            <div className="bg-[var(--secondary)] px-4 py-2 rounded-lg">
              <p className="text-sm text-[var(--muted-foreground)] animate-pulse">
                Pensando...
              </p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        onSend={sendMessage}
        loading={isLoading}
        suggestions={messages.length === 0 ? suggestions : []}
      />
      </div>
    </div>
  );
}
