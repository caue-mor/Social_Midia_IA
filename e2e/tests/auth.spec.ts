import { test, expect } from "@playwright/test";

test("login form has email and password fields", async ({ page }) => {
  await page.goto("/login");
  await expect(page.locator('input[type="email"]')).toBeVisible();
  await expect(page.locator('input[type="password"]')).toBeVisible();
});

test("signup link exists on login page", async ({ page }) => {
  await page.goto("/login");
  const signupLink = page.locator('a[href="/signup"]');
  await expect(signupLink).toBeVisible();
});
