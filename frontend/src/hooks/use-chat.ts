"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { createClient } from "@/lib/supabase";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  agent_type?: string;
}

type ConnectionMode = "websocket" | "http" | "connecting";

const MAX_RECONNECT_RETRIES = 3;
const RECONNECT_BASE_DELAY_MS = 1000;

function getWsUrl(): string {
  const backendUrl =
    process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
  // Convert http(s):// to ws(s)://
  return backendUrl
    .replace(/^https:\/\//, "wss://")
    .replace(/^http:\/\//, "ws://");
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionMode, setConnectionMode] = useState<ConnectionMode>("connecting");

  const wsRef = useRef<WebSocket | null>(null);
  const retriesRef = useRef(0);
  const conversationIdRef = useRef<string | null>(null);
  const pendingResolveRef = useRef<((value: void) => void) | null>(null);
  const isUnmountedRef = useRef(false);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Get auth token from Supabase session
  const getToken = useCallback(async (): Promise<string | null> => {
    try {
      const supabase = createClient();
      const {
        data: { session },
      } = await supabase.auth.getSession();
      return session?.access_token ?? null;
    } catch {
      return null;
    }
  }, []);

  // Handle incoming WebSocket messages
  const handleWsMessage = useCallback((event: MessageEvent) => {
    try {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case "authenticated":
          // Server confirmed auth
          break;

        case "typing":
          setIsTyping(data.status === true);
          break;

        case "message":
          if (data.data) {
            // Update conversation ID from server response
            if (data.data.conversation_id) {
              conversationIdRef.current = data.data.conversation_id;
            }
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: data.data.response || "Erro ao processar.",
                timestamp: new Date(),
                agent_type: data.data.agent_type,
              },
            ]);
          }
          setIsLoading(false);
          if (pendingResolveRef.current) {
            pendingResolveRef.current();
            pendingResolveRef.current = null;
          }
          break;

        case "error":
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: data.message || "Erro desconhecido.",
              timestamp: new Date(),
            },
          ]);
          setIsLoading(false);
          setIsTyping(false);
          if (pendingResolveRef.current) {
            pendingResolveRef.current();
            pendingResolveRef.current = null;
          }
          break;

        default:
          break;
      }
    } catch {
      // Ignore malformed messages
    }
  }, []);

  // Connect WebSocket
  const connectWs = useCallback(
    async (token: string) => {
      // Clean up existing connection
      if (wsRef.current) {
        wsRef.current.onclose = null;
        wsRef.current.onerror = null;
        wsRef.current.onmessage = null;
        wsRef.current.close();
        wsRef.current = null;
      }

      const wsUrl = `${getWsUrl()}/api/v1/chat/ws?token=${encodeURIComponent(token)}`;

      return new Promise<boolean>((resolve) => {
        try {
          const ws = new WebSocket(wsUrl);
          const timeout = setTimeout(() => {
            ws.close();
            resolve(false);
          }, 5000);

          ws.onopen = () => {
            clearTimeout(timeout);
            wsRef.current = ws;
            setIsConnected(true);
            setConnectionMode("websocket");
            retriesRef.current = 0;
            resolve(true);
          };

          ws.onmessage = handleWsMessage;

          ws.onerror = () => {
            clearTimeout(timeout);
            resolve(false);
          };

          ws.onclose = () => {
            if (isUnmountedRef.current) return;

            wsRef.current = null;
            setIsConnected(false);

            // Attempt reconnection
            if (retriesRef.current < MAX_RECONNECT_RETRIES) {
              retriesRef.current += 1;
              const delay =
                RECONNECT_BASE_DELAY_MS * Math.pow(2, retriesRef.current - 1);
              reconnectTimerRef.current = setTimeout(async () => {
                const freshToken = await getToken();
                if (freshToken && !isUnmountedRef.current) {
                  const reconnected = await connectWs(freshToken);
                  if (!reconnected) {
                    setConnectionMode("http");
                  }
                }
              }, delay);
            } else {
              // Exhausted retries, fall back to HTTP
              setConnectionMode("http");
            }
          };
        } catch {
          resolve(false);
        }
      });
    },
    [handleWsMessage, getToken]
  );

  // Initialize connection on mount
  useEffect(() => {
    isUnmountedRef.current = false;
    let cancelled = false;

    const init = async () => {
      const token = await getToken();
      if (cancelled || !token) {
        if (!cancelled) setConnectionMode("http");
        return;
      }

      setConnectionMode("connecting");
      const connected = await connectWs(token);
      if (!connected && !cancelled) {
        setConnectionMode("http");
      }
    };

    init();

    return () => {
      cancelled = true;
      isUnmountedRef.current = true;
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
        reconnectTimerRef.current = null;
      }
      if (wsRef.current) {
        wsRef.current.onclose = null;
        wsRef.current.onerror = null;
        wsRef.current.onmessage = null;
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [getToken, connectWs]);

  // Send message via WebSocket
  const sendViaWs = useCallback(
    (content: string): Promise<void> => {
      return new Promise((resolve) => {
        if (
          !wsRef.current ||
          wsRef.current.readyState !== WebSocket.OPEN
        ) {
          resolve();
          return;
        }

        pendingResolveRef.current = resolve;

        const payload: Record<string, unknown> = { message: content };
        if (conversationIdRef.current) {
          payload.conversation_id = conversationIdRef.current;
        }

        wsRef.current.send(JSON.stringify(payload));
      });
    },
    []
  );

  // Send message via HTTP fallback
  const sendViaHttp = useCallback(
    async (content: string) => {
      try {
        const body: Record<string, unknown> = { message: content };
        if (conversationIdRef.current) {
          body.conversation_id = conversationIdRef.current;
        }

        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });

        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();

        if (data.conversation_id) {
          conversationIdRef.current = data.conversation_id;
        }

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.response || "Erro ao processar.",
            timestamp: new Date(),
            agent_type: data.agent_type,
          },
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Erro de conexao. Tente novamente.",
            timestamp: new Date(),
          },
        ]);
      }
    },
    []
  );

  // Main send function: tries WebSocket first, falls back to HTTP
  const sendMessage = useCallback(
    async (content: string) => {
      const trimmed = content.trim();
      if (!trimmed || isLoading) return;

      setIsLoading(true);

      // Add user message immediately
      setMessages((prev) => [
        ...prev,
        { role: "user", content: trimmed, timestamp: new Date() },
      ]);

      const wsOpen =
        wsRef.current && wsRef.current.readyState === WebSocket.OPEN;

      if (wsOpen) {
        setIsTyping(true);
        await sendViaWs(trimmed);
      } else {
        await sendViaHttp(trimmed);
      }

      setIsLoading(false);
      setIsTyping(false);
    },
    [isLoading, sendViaWs, sendViaHttp]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    conversationIdRef.current = null;
  }, []);

  const loadConversation = useCallback((conversationId: string, messages: Message[]) => {
    conversationIdRef.current = conversationId;
    setMessages(messages);
  }, []);

  const getCurrentConversationId = useCallback(() => {
    return conversationIdRef.current;
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
    isTyping,
    isConnected,
    connectionMode,
    clearMessages,
    loadConversation,
    getCurrentConversationId,
  };
}
