import { test, expect } from "@playwright/test";

test("homepage loads", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/AgenteSocial/);
});

test("login page accessible", async ({ page }) => {
  await page.goto("/login");
  await expect(page.locator("form")).toBeVisible();
});

test("redirects to login when not authenticated", async ({ page }) => {
  await page.goto("/chat");
  await expect(page).toHaveURL(/login/);
});
