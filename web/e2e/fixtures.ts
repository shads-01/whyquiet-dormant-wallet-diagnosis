/**
 * Shared Playwright fixtures for specs that require an authenticated session.
 *
 * D68 added a global auth gate in App.tsx that renders a sign-in wall whenever
 * `sessionStorage` has no `wq_user` entry. `authedPage` / `authedPageApprover`
 * seed sessionStorage via `addInitScript` — no network, no UI clicks — so every
 * existing test can keep its own navigation logic unchanged.
 *
 * Usage:
 *   import { test, expect } from "./fixtures";
 *   // `page` is now the auto-authed page; use it exactly like before.
 */
import { test as base, type Page } from "@playwright/test";

/** Minimal UserSession that satisfies App.tsx's `getStoredUser()` check. */
const ANALYST_SESSION = JSON.stringify({
  email: "analyst@whyquiet.demo",
  user_id: "analyst@whyquiet.demo",
  role: "analyst",
  access_token: "e2e-token",
});

const APPROVER_SESSION = JSON.stringify({
  email: "approver@whyquiet.demo",
  user_id: "approver@whyquiet.demo",
  role: "approver",
  access_token: "e2e-token",
});

/** Seeds sessionStorage before the page's first script runs. */
async function seedSession(page: Page, session: string): Promise<void> {
  await page.addInitScript((s: string) => {
    sessionStorage.setItem("wq_token", "e2e-token");
    sessionStorage.setItem("wq_user", s);
  }, session);
}

export const test = base.extend<{
  authedPage: Page;
  authedPageApprover: Page;
}>({
  /** `page` with analyst session pre-seeded into sessionStorage. */
  authedPage: async ({ page }, use) => {
    await seedSession(page, ANALYST_SESSION);
    // eslint-disable-next-line react-hooks/rules-of-hooks
    await use(page);
  },
  /** `page` with approver session pre-seeded into sessionStorage. */
  authedPageApprover: async ({ page }, use) => {
    await seedSession(page, APPROVER_SESSION);
    // eslint-disable-next-line react-hooks/rules-of-hooks
    await use(page);
  },
});

export { expect } from "@playwright/test";
