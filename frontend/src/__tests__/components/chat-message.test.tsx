import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ChatMessage } from "@/components/chat/chat-message";

// Mock react-markdown since it uses ESM and doesn't play well with jsdom
vi.mock("react-markdown", () => ({
  default: ({ children }: { children: string }) => (
    <div data-testid="markdown">{children}</div>
  ),
}));

describe("ChatMessage", () => {
  it("renders user message with correct alignment", () => {
    const { container } = render(
      <ChatMessage role="user" content="Hello there" />
    );

    expect(screen.getByText("Hello there")).toBeInTheDocument();
    // User messages should be right-aligned
    const wrapper = container.firstElementChild;
    expect(wrapper).toHaveClass("justify-end");
  });

  it("renders user message as plain text (not markdown)", () => {
    render(<ChatMessage role="user" content="Hello **bold**" />);

    // User messages render as <p> not through ReactMarkdown
    const textElement = screen.getByText("Hello **bold**");
    expect(textElement.tagName).toBe("P");
    expect(textElement).toHaveClass("whitespace-pre-wrap");
  });

  it("renders assistant message with correct alignment", () => {
    const { container } = render(
      <ChatMessage role="assistant" content="Hi, how can I help?" />
    );

    expect(screen.getByText("Hi, how can I help?")).toBeInTheDocument();
    // Assistant messages should be left-aligned
    const wrapper = container.firstElementChild;
    expect(wrapper).toHaveClass("justify-start");
  });

  it("renders assistant message through markdown", () => {
    render(
      <ChatMessage role="assistant" content="Here is **bold** text" />
    );

    // Should pass through the mocked ReactMarkdown
    const markdownEl = screen.getByTestId("markdown");
    expect(markdownEl).toBeInTheDocument();
    expect(markdownEl).toHaveTextContent("Here is **bold** text");
  });

  it("applies primary background to user messages", () => {
    const { container } = render(
      <ChatMessage role="user" content="Test" />
    );

    const bubble = container.querySelector(".bg-\\[var\\(--primary\\)\\]");
    expect(bubble).toBeInTheDocument();
  });

  it("applies secondary background to assistant messages", () => {
    const { container } = render(
      <ChatMessage role="assistant" content="Test" />
    );

    const bubble = container.querySelector(".bg-\\[var\\(--secondary\\)\\]");
    expect(bubble).toBeInTheDocument();
  });
});
