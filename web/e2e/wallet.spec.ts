import { test, expect } from "./fixtures";

test.describe("Wallet Detail & Refusal Page", () => {
  test.beforeEach(async ({ authedPage: page }) => {
    // Pin to seed.sample.json: these tests use known sample wallets; real-data.spec.ts covers seed.json.
    await page.route("**/seed.json", (route) => route.fulfill({ status: 404 }));
  });

  test("attributed wallet: displays remedy, bilingual copy, boundary transparency notice, and charts", async ({ page }) => {
    // Navigate to known attributed wallet from sample seed
    await page.goto("/#/w/W-7K9A1B");

    // Check Header & Verdict
    await expect(page.getByTestId("wallet-id-header")).toHaveText("W-7K9A1B");
    await expect(page.getByTestId("wallet-verdict-chip")).toHaveText("Attributed");

    // Check Boundary Badge & Notice (W-7K9A1B has top prob 0.86 < 0.90)
    await expect(page.getByTestId("boundary-badge")).toBeVisible();
    await expect(page.getByTestId("boundary-notice")).toBeVisible();
    await expect(page.getByTestId("boundary-notice")).toContainText(
      "Near the refusal boundary — a small change in the decline shape would flip this verdict to refused."
    );
    await expect(page.getByTestId("boundary-notice")).toContainText("0.86");
    await expect(page.getByTestId("boundary-notice")).toContainText("0.80");

    // Check Rule vs Model comparison
    await expect(page.getByTestId("rule-vs-model-card")).toBeVisible();
    await expect(page.getByTestId("rule-vs-model-card")).toContainText("Message Everyone");

    // Check Attributed Remedy Card
    const remedyCard = page.getByTestId("remedy-card");
    await expect(remedyCard).toBeVisible();
    await expect(page.getByTestId("remedy-label")).toBeVisible();
    await expect(page.getByTestId("remedy-msg-en")).toBeVisible();
    await expect(page.getByTestId("remedy-msg-bn")).toBeVisible();

    // Check Charts & Feature Attributions
    await expect(page.getByTestId("decline-shape-card")).toBeVisible();
    await expect(page.getByTestId("posterior-chart-card")).toBeVisible();
    await expect(page.getByTestId("contributions-card")).toBeVisible();
  });

  test("refused wallet: displays exact refusal headline, reasons, boundary transparency block, and no action buttons", async ({ page }) => {
    // Navigate to known refused wallet from sample seed
    await page.goto("/#/w/W-6B8C1D");

    // Check Header & Verdict
    await expect(page.getByTestId("wallet-id-header")).toHaveText("W-6B8C1D");
    await expect(page.getByTestId("wallet-verdict-chip")).toHaveText("Refused");

    // Check Dedicated Refusal Panel & exact headline
    const refusalPanel = page.getByTestId("refusal-panel");
    await expect(refusalPanel).toBeVisible();
    await expect(page.getByTestId("refusal-headline")).toHaveText(
      "No attributable cause. I will not spend your money here."
    );

    // Check refusal reasons list
    const reasonsList = page.getByTestId("refusal-reasons-list");
    await expect(reasonsList).toBeVisible();
    await expect(reasonsList.locator("li")).not.toHaveCount(0);

    // Check Boundary Transparency: "What would change this verdict" block
    const whatWouldChangeBlock = page.getByTestId("what-would-change-block");
    await expect(whatWouldChangeBlock).toBeVisible();
    await expect(whatWouldChangeBlock).toContainText("What Would Change This Verdict");

    // Verify numerical metrics against dynamic thresholds (tau=0.50, delta=0.10 in sample seed)
    const probMetric = page.getByTestId("boundary-prob-metric");
    await expect(probMetric).toBeVisible();
    await expect(probMetric).toContainText("0.38");
    await expect(page.getByTestId("tau-target")).toContainText("0.50");

    const marginMetric = page.getByTestId("boundary-margin-metric");
    await expect(marginMetric).toBeVisible();
    await expect(marginMetric).toContainText("0.07");
    await expect(page.getByTestId("delta-target")).toContainText("0.10");

    // Verify NO action buttons or interactive controls exist on the refusal card (D13: refusals are terminal)
    await expect(refusalPanel.locator("button")).toHaveCount(0);
    await expect(refusalPanel.locator("input")).toHaveCount(0);
    await expect(refusalPanel.locator("select")).toHaveCount(0);

    // Check decline shape and posterior charts are rendered
    await expect(page.getByTestId("decline-shape-card")).toBeVisible();
    await expect(page.getByTestId("posterior-chart-card")).toBeVisible();
  });

  test("empty state: shows helpful not-found message and returns to queue", async ({ authedPage: page }) => {
    await page.goto("/#/w/W-UNKNOWN99");

    await expect(page.getByTestId("wallet-not-found-state")).toBeVisible();
    await page.getByTestId("back-to-queue-btn").click();

    await expect(page).toHaveURL(/#\/$/);
    await expect(page.getByTestId("queue-view")).toBeVisible();
  });

  test("back button in header returns to triage queue", async ({ authedPage: page }) => {
    await page.goto("/#/w/W-7K9A1B");
    await page.getByTestId("back-button").click();

    await expect(page).toHaveURL(/#\/$/);
    await expect(page.getByTestId("queue-view")).toBeVisible();
  });
});
