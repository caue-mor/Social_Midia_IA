import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import userEvent from "@testing-library/user-event";
import { ConversationHistory } from "@/components/chat/conversation-history";

global.fetch = vi.fn();

describe("ConversationHistory", () => {
  const mockConversations = [
    {
      id: "conv-1",
      first_message: "Hello, how are you?",
      created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(), // 5 mins ago
      agent_type: "assistant",
      updated_at: new Date().toISOString(),
    },
    {
      id: "conv-2",
      first_message: "What is the weather today?",
      created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
      agent_type: "weather",
      updated_at: new Date().toISOString(),
    },
  ];

  const mockMessages = [
    {
      role: "user",
      content: "Hello",
      created_at: new Date().toISOString(),
    },
    {
      role: "assistant",
      content: "Hi there!",
      created_at: new Date().toISOString(),
      agent_type: "assistant",
    },
  ];

  const defaultProps = {
    activeConversationId: null,
    onSelectConversation: vi.fn(),
    onNewConversation: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ conversations: mockConversations }),
    });
  });

  it("renders the new conversation button", async () => {
    render(<ConversationHistory {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText("Nova conversa")).toBeInTheDocument();
    });
  });

  it("fetches and displays conversations", async () => {
    render(<ConversationHistory {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText(/Hello, how are you\?/)).toBeInTheDocument();
      expect(screen.getByText(/What is the weather today\?/)).toBeInTheDocument();
    });
  });

  it("displays agent type badges", async () => {
    render(<ConversationHistory {...defaultProps} />);

    await waitFor(() => {
      const badges = screen.getAllByText(/assistant|weather/);
      expect(badges.length).toBeGreaterThan(0);
    });
  });

  it("displays relative time for conversations", async () => {
    render(<ConversationHistory {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText(/5m atrás/)).toBeInTheDocument();
      expect(screen.getByText(/2h atrás/)).toBeInTheDocument();
    });
  });

  it("calls onSelectConversation when clicking a conversation", async () => {
    const user = userEvent.setup();
    const onSelectConversation = vi.fn();

    (global.fetch as any).mockImplementation((url: string) => {
      if (url.includes("/messages")) {
        return Promise.resolve({
          ok: true,
          json: async () => ({ messages: mockMessages }),
        });
      }
      return Promise.resolve({
        ok: true,
        json: async () => ({ conversations: mockConversations }),
      });
    });

    render(
      <ConversationHistory
        {...defaultProps}
        onSelectConversation={onSelectConversation}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/Hello, how are you\?/)).toBeInTheDocument();
    });

    const conversationButton = screen.getByText(/Hello, how are you\?/).closest("button");
    if (conversationButton) {
      await user.click(conversationButton);
    }

    await waitFor(() => {
      expect(onSelectConversation).toHaveBeenCalledWith("conv-1", expect.any(Array));
    });
  });

  it("calls onNewConversation when clicking new conversation button", async () => {
    const user = userEvent.setup();
    const onNewConversation = vi.fn();

    render(
      <ConversationHistory
        {...defaultProps}
        onNewConversation={onNewConversation}
      />
    );

    await waitFor(() => {
      expect(screen.getByText("Nova conversa")).toBeInTheDocument();
    });

    await user.click(screen.getByText("Nova conversa"));

    expect(onNewConversation).toHaveBeenCalledTimes(1);
  });

  it("highlights the active conversation", async () => {
    const { container } = render(
      <ConversationHistory {...defaultProps} activeConversationId="conv-1" />
    );

    await waitFor(() => {
      const activeButton = container.querySelector(".border-\\[var\\(--primary\\)\\]");
      expect(activeButton).toBeInTheDocument();
    });
  });

  it("displays loading state initially", () => {
    render(<ConversationHistory {...defaultProps} />);

    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("displays empty state when no conversations", async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ conversations: [] }),
    });

    render(<ConversationHistory {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText("Nenhuma conversa ainda")).toBeInTheDocument();
    });
  });

  it("truncates long messages", async () => {
    const longMessage = "A".repeat(100);
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        conversations: [
          {
            id: "conv-long",
            first_message: longMessage,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        ],
      }),
    });

    render(<ConversationHistory {...defaultProps} />);

    await waitFor(() => {
      const displayedText = screen.getByText(/A+\.\.\./);
      expect(displayedText.textContent?.length).toBeLessThan(longMessage.length);
    });
  });
});
