import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { ChatInput } from "@/components/chat/chat-input";

describe("ChatInput", () => {
  it("renders the input field and send button", () => {
    render(<ChatInput onSend={vi.fn()} />);

    expect(
      screen.getByPlaceholderText("Digite sua mensagem...")
    ).toBeInTheDocument();
    expect(screen.getByText("Enviar")).toBeInTheDocument();
  });

  it("disables send button when input is empty", () => {
    render(<ChatInput onSend={vi.fn()} />);

    const button = screen.getByText("Enviar");
    expect(button).toBeDisabled();
  });

  it("enables send button when input has text", async () => {
    const user = userEvent.setup();
    render(<ChatInput onSend={vi.fn()} />);

    const input = screen.getByPlaceholderText("Digite sua mensagem...");
    await user.type(input, "Hello");

    const button = screen.getByText("Enviar");
    expect(button).not.toBeDisabled();
  });

  it("calls onSend with trimmed text on button click", async () => {
    const mockSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={mockSend} />);

    const input = screen.getByPlaceholderText("Digite sua mensagem...");
    await user.type(input, "  Hello world  ");
    await user.click(screen.getByText("Enviar"));

    expect(mockSend).toHaveBeenCalledWith("Hello world");
  });

  it("calls onSend on Enter key press", async () => {
    const mockSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={mockSend} />);

    const input = screen.getByPlaceholderText("Digite sua mensagem...");
    await user.type(input, "Test message{Enter}");

    expect(mockSend).toHaveBeenCalledWith("Test message");
  });

  it("clears input after sending", async () => {
    const mockSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={mockSend} />);

    const input = screen.getByPlaceholderText(
      "Digite sua mensagem..."
    ) as HTMLInputElement;
    await user.type(input, "Hello{Enter}");

    expect(input.value).toBe("");
  });

  it("does not send empty or whitespace-only messages", async () => {
    const mockSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={mockSend} />);

    const input = screen.getByPlaceholderText("Digite sua mensagem...");
    await user.type(input, "   {Enter}");

    expect(mockSend).not.toHaveBeenCalled();
  });

  it("disables input and shows loading state when loading", () => {
    render(<ChatInput onSend={vi.fn()} loading={true} />);

    const input = screen.getByPlaceholderText("Digite sua mensagem...");
    expect(input).toBeDisabled();
    expect(screen.getByText("...")).toBeInTheDocument();
  });

  it("renders suggestion buttons when provided and input is empty", () => {
    render(
      <ChatInput
        onSend={vi.fn()}
        suggestions={["Criar post", "Analisar perfil"]}
      />
    );

    expect(screen.getByText("Criar post")).toBeInTheDocument();
    expect(screen.getByText("Analisar perfil")).toBeInTheDocument();
  });

  it("fills input when suggestion is clicked", async () => {
    const user = userEvent.setup();
    render(
      <ChatInput onSend={vi.fn()} suggestions={["Criar post"]} />
    );

    await user.click(screen.getByText("Criar post"));

    const input = screen.getByPlaceholderText(
      "Digite sua mensagem..."
    ) as HTMLInputElement;
    expect(input.value).toBe("Criar post");
  });
});
