import { expect, type Page } from "@playwright/test";
import * as fs from "fs";
import { test } from "./fixtures";
import AxeBuilder from "@axe-core/playwright";

// e2e has no Supabase, so sign-in is mocked and each /api/score call is forwarded to the REAL API with the
// e2e API key instead of the mock bearer token (playwright.config.ts). The scores come from the real model.
async function mockScoreApi(page: Page, scoreAuth: (string | undefined)[] = []) {
  await page.route("**/api/score", async (route) => {
    const headers = { ...route.request().headers() };
    scoreAuth.push(headers["authorization"]);
    delete headers["authorization"];
    await route.fulfill({ response: await route.fetch({ headers: { ...headers, "x-api-key": "e2e-score-key" } }) });
  });
}

test.describe("Score a Ledger File", () => {
  test("signed out: shows app-level sign-in gate instead of scoring UI", async ({ page }) => {
    await page.goto("/#/score");
    // D68: the global gate intercepts before Score.tsx renders.
    await expect(page.getByTestId("signin-gate")).toBeVisible();
    await expect(page.getByTestId("score-sample-btn")).toHaveCount(0);
  });

  test("sample ledger is scored live: 20 wallets, attributed and refused, token sent", async ({ authedPage: page }) => {
    const auth: (string | undefined)[] = [];
    await page.goto("/#/score");
    await mockScoreApi(page, auth);

    // Read the sample ledger from disk and upload it
    const sampleLedger = fs.readFileSync("public/sample-ledger.csv");
    await page.getByTestId("score-file-input").setInputFiles({
      name: "sample-ledger.csv", mimeType: "text/csv", buffer: sampleLedger,
    });

    await expect(page.getByTestId("score-results")).toContainText("20 wallets scored");
    await expect(page.getByTestId("score-results")).toContainText("16 attributed");
    await expect(page.getByTestId("score-results")).toContainText("4 refused");
    await expect(page.getByTestId("score-table").locator("tbody tr")).toHaveCount(20);
    await expect(page.getByTestId("score-table")).toContainText("below the 0.85 bar");
    expect(auth).toEqual(["Bearer e2e-token"]);
  });

  test("an uploaded file without the required columns shows the problem", async ({ authedPage: page }) => {
    await page.goto("/#/score");
    await mockScoreApi(page);
    await page.getByTestId("score-file-input").setInputFiles({
      name: "bad.csv", mimeType: "text/csv", buffer: Buffer.from("wallet_id,week\nW-AAAAAA,3\n"),
    });
    await expect(page.getByTestId("score-error")).toContainText("Missing column(s): acquired_week");
  });

  test("Score page with results passes WCAG 2.1 AA", async ({ authedPage: page }) => {
    await page.goto("/#/score");
    await mockScoreApi(page);
    const sampleLedger = fs.readFileSync("public/sample-ledger.csv");
    await page.getByTestId("score-file-input").setInputFiles({
      name: "sample-ledger.csv", mimeType: "text/csv", buffer: sampleLedger,
    });
    await expect(page.getByTestId("score-table")).toBeVisible();
    const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
    expect(results.violations).toEqual([]);
  });
});
