import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { StatsCard } from "@/components/dashboard/stats-card";

describe("StatsCard", () => {
  it("renders title, value, and description", () => {
    render(
      <StatsCard title="Total Posts" value={42} description="Last 30 days" />
    );

    expect(screen.getByText("Total Posts")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
    expect(screen.getByText("Last 30 days")).toBeInTheDocument();
  });

  it("renders string value correctly", () => {
    render(<StatsCard title="Revenue" value="R$ 1.200" />);

    expect(screen.getByText("Revenue")).toBeInTheDocument();
    expect(screen.getByText("R$ 1.200")).toBeInTheDocument();
  });

  it("shows positive trend indicator with up arrow prefix", () => {
    render(
      <StatsCard
        title="Followers"
        value={1500}
        trend="up"
        trendValue="12%"
      />
    );

    const trendElement = screen.getByText("+12%", { exact: false });
    expect(trendElement).toBeInTheDocument();
    expect(trendElement.closest("p")).toHaveClass("text-green-500");
  });

  it("shows negative trend indicator without extra prefix", () => {
    render(
      <StatsCard
        title="Bounce Rate"
        value="45%"
        trend="down"
        trendValue="-5%"
      />
    );

    const trendElement = screen.getByText("-5%", { exact: false });
    expect(trendElement).toBeInTheDocument();
    expect(trendElement.closest("p")).toHaveClass("text-red-500");
  });

  it("shows neutral trend with muted color", () => {
    render(
      <StatsCard
        title="Engagement"
        value="3.2%"
        trend="neutral"
        trendValue="0%"
      />
    );

    const trendElement = screen.getByText("0%", { exact: false });
    expect(trendElement).toBeInTheDocument();
    expect(trendElement.closest("p")).toHaveClass(
      "text-[var(--muted-foreground)]"
    );
  });

  it("does not render description row when no description or trendValue", () => {
    const { container } = render(
      <StatsCard title="Simple" value={10} />
    );

    const paragraphs = container.querySelectorAll("p");
    // Should only have title and value paragraphs, no description row
    expect(paragraphs).toHaveLength(2);
  });
});
