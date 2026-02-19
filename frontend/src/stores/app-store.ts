import { create } from "zustand";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  agent_type?: string;
}

interface AppState {
  // Chat state
  chatMessages: Message[];
  chatConversationId: string | null;
  addChatMessage: (message: Message) => void;
  setChatMessages: (messages: Message[]) => void;
  setChatConversationId: (id: string | null) => void;
  clearChat: () => void;

  // Calendar state
  calendarDate: Date;
  setCalendarDate: (date: Date) => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Chat
  chatMessages: [],
  chatConversationId: null,
  addChatMessage: (message) =>
    set((state) => ({ chatMessages: [...state.chatMessages, message] })),
  setChatMessages: (messages) => set({ chatMessages: messages }),
  setChatConversationId: (id) => set({ chatConversationId: id }),
  clearChat: () => set({ chatMessages: [], chatConversationId: null }),

  // Calendar
  calendarDate: new Date(),
  setCalendarDate: (date) => set({ calendarDate: date }),
}));
