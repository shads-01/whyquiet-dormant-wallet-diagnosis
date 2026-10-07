import { test, expect } from "./fixtures";
import AxeBuilder from "@axe-core/playwright";

test.describe("Frontend Accessibility Audits (WCAG 2.1 AA)", () => {
  // Route mocks are set per-test; sessionStorage is seeded by the authedPage / authedPageApprover fixture.


  test("Triage Queue page passes WCAG 2.1 AA in light & dark modes", async ({ authedPage: page }) => {
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/");
    await expect(page.getByTestId("queue-view")).toBeVisible();

    // 1. Audit Light Mode (default)
    const lightAxeResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(lightAxeResults.violations).toEqual([]);

    // 2. Audit Dark Mode
    await page.getByTestId("mode-toggle").click();
    await expect(page.locator("html")).toHaveAttribute("data-mode", "dark");
    const darkAxeResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(darkAxeResults.violations).toEqual([]);
  });

  test("Wallet Detail (Attributed) passes WCAG 2.1 AA", async ({ authedPage: page }) => {
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/w/W-7K9A1B");
    await expect(page.getByTestId("wallet-view")).toBeVisible();
    await expect(page.getByTestId("remedy-card")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test("Wallet Detail (Refused) passes WCAG 2.1 AA", async ({ authedPage: page }) => {
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/w/W-6B8C1D");
    await expect(page.getByTestId("wallet-view")).toBeVisible();
    await expect(page.getByTestId("refusal-panel")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test("Batches & Governance page passes WCAG 2.1 AA", async ({ authedPage: page }) => {
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/batches");
    await expect(page.getByTestId("batches-view")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test("Evidence & ML Rigor page passes WCAG 2.1 AA", async ({ authedPage: page }) => {
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/evidence");
    await expect(page.getByTestId("evidence-view")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test("Sign In Modal passes WCAG 2.1 AA", async ({ page }) => {
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/");
    await page.getByTestId("open-login-btn").click();
    await expect(page.getByTestId("login-modal")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test("Decision Modal passes WCAG 2.1 AA", async ({ authedPageApprover: page }) => {
    // Mock login API so the manual sign-in UI flow works if ever needed,
    // but sessionStorage is already seeded with approver creds by the fixture.
    await page.route("**/api/auth/login", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          access_token: "mock-token",
          token_type: "bearer",
          user_id: "approver@whyquiet.demo",
          email: "approver@whyquiet.demo",
          role: "approver",
        }),
      })
    );
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
    await page.goto("/#/batches");
    await expect(page.getByTestId("batches-view")).toBeVisible();

    // Click Approve on first proposed batch
    const approveBtn = page.locator("[data-testid^='approve-btn-']").first();
    await expect(approveBtn).toBeVisible();
    await approveBtn.click();
    await expect(page.getByTestId("decision-modal")).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  for (const [name, route, testid] of [
    ["Five Causes", "/#/causes", "causes-view"],
    ["Refusal Dial", "/#/calibration", "calibration-view"],
    ["Evidence with simulator", "/#/evidence", "simulator-card"],
  ]) {
    test(`${name} passes WCAG 2.1 AA in light & dark modes (real seed)`, async ({ authedPage: page }) => {
      await page.goto(route);
      await expect(page.getByTestId(testid)).toBeVisible();
      const tags = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"];
      expect((await new AxeBuilder({ page }).withTags(tags).analyze()).violations).toEqual([]);
      await page.getByTestId("mode-toggle").click();
      await expect(page.locator("html")).toHaveAttribute("data-mode", "dark");
      expect((await new AxeBuilder({ page }).withTags(tags).analyze()).violations).toEqual([]);
    });
  }
});
