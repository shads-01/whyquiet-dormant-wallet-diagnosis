import { test, expect } from "./fixtures";

test.describe("Evidence & ML Rigor Page", () => {
  test("displays ML rigor panel with headline Population B F1, rule baseline, and shuffled control", async ({ authedPage: page }) => {
    await page.goto("/#/evidence");

    // ML Rigor Panel
    const mlPanel = page.getByTestId("ml-rigor-panel");
    await expect(mlPanel).toBeVisible();

    // Headline Population B Macro-F1 Card
    await expect(page.getByTestId("headline-f1-card")).toBeVisible();
    await expect(page.getByTestId("headline-f1-value")).toContainText("%");

    // Rule Baseline Card
    await expect(page.getByTestId("rule-baseline-f1-card")).toBeVisible();
    await expect(page.getByTestId("rule-baseline-f1-value")).toContainText("%");

    // Shuffled Label Control Card
    await expect(page.getByTestId("shuffled-control-card")).toBeVisible();
    await expect(page.getByTestId("shuffled-control-value")).toContainText("%");
  });

  test("displays confusion matrix and demographic parity fairness tables", async ({ authedPage: page }) => {
    await page.goto("/#/evidence");

    // Confusion Matrix Table
    const cmCard = page.getByTestId("confusion-matrix-card");
    await expect(cmCard).toBeVisible();
    const cmTable = page.getByTestId("confusion-matrix-table");
    await expect(cmTable).toBeVisible();
    await expect(cmTable.locator("tbody tr")).toHaveCount(5);

    // Fairness Table
    const fairnessCard = page.getByTestId("fairness-card");
    await expect(fairnessCard).toBeVisible();
    const fairnessTable = page.getByTestId("fairness-table");
    await expect(fairnessTable).toBeVisible();
    await expect(fairnessTable.locator("tbody tr")).not.toHaveCount(0);
  });

  test("economic recovery section: handles rate toggling and renders ASSUMED badges", async ({ authedPage: page }) => {
    await page.goto("/#/evidence");

    // Money Card & ASSUMED badge
    const moneyCard = page.getByTestId("money-card");
    await expect(moneyCard).toBeVisible();
    // Net values are thousands of BDT: the axis must not round them to "0.0M"
    await expect(moneyCard.locator(".recharts-yAxis")).not.toContainText("M");
    await expect(page.getByTestId("assumed-badge")).toHaveText("ASSUMED");
    // Recovered users are people: whole numbers, not "21.103"
    await expect(page.getByTestId("users-recovered-model")).toHaveText(/^[\d,]+$/);

    // Check initial Net Value (4% base)
    const baseModelVal = await page.getByTestId("net-value-model").innerText();

    // Toggle to 1% Response
    await page.getByTestId("rate-toggle-1").click();
    const lowModelVal = await page.getByTestId("net-value-model").innerText();
    expect(lowModelVal).not.toBe(baseModelVal);

    // Toggle to 8% Response
    await page.getByTestId("rate-toggle-8").click();
    const highModelVal = await page.getByTestId("net-value-model").innerText();
    expect(highModelVal).not.toBe(lowModelVal);
    expect(highModelVal).not.toBe(baseModelVal);

    // Check Assumptions Box
    const assumptionsBox = page.getByTestId("assumptions-box");
    await expect(assumptionsBox).toBeVisible();
    await expect(assumptionsBox.locator("li")).not.toHaveCount(0);
  });

  test("mobile responsive view at 375px width", async ({ authedPage: page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/#/evidence");

    await expect(page.getByTestId("evidence-view")).toBeVisible();
    await expect(page.getByTestId("headline-f1-card")).toBeVisible();
    await expect(page.getByTestId("confusion-matrix-table")).toBeVisible();
    await expect(page.getByTestId("money-card")).toBeVisible();
  });
});

test.describe("Evidence phase 2 depth sections (real seed.json)", () => {
  test("shows refusal dial, baselines, error anatomy, calibration, label-free checks and stress tests", async ({ authedPage: page }) => {
    await page.goto("/#/evidence");

    const dial = page.getByTestId("refusal-dial-card");
    await expect(dial).toBeVisible();
    await expect(dial.locator(".recharts-line")).toHaveCount(2);
    await expect(page.getByTestId("baseline-ladder-table").locator("tbody tr")).toHaveCount(5);
    await expect(page.getByTestId("group-shift-table").locator("tbody tr")).toHaveCount(3);

    await expect(page.getByTestId("per-class-table").locator("tbody tr")).toHaveCount(5);
    await expect(page.getByTestId("ablation-table").locator("tbody tr")).toHaveCount(6);
    await expect(page.getByTestId("blended-tiles")).toContainText("refused");

    await expect(page.getByTestId("calibration-card").locator(".recharts-line")).toHaveCount(2);
    await expect(page.getByTestId("atc-estimate-value")).toHaveText(/^\d+\.\d%$/);
    await expect(page.getByTestId("cause-mix-table").locator("tbody tr")).toHaveCount(5);
    await expect(page.getByTestId("drift-table").locator("tbody tr")).toHaveCount(6);

    await expect(page.getByTestId("noise-dial-table").locator("tbody tr")).toHaveCount(4);
    await expect(page.getByTestId("unseen-refusal-value")).toContainText("refused");

    // The old card claimed calibration "within 5.2%" next to an error of 0.100
    await expect(page.getByTestId("ml-rigor-panel")).not.toContainText("5.2%");
  });

  test("money section shows the value-gated strategy next to the rule", async ({ authedPage: page }) => {
    await page.goto("/#/evidence");
    for (const s of ["rule", "model", "model_ev", "oracle"]) {
      await expect(page.getByTestId(`money-row-${s}`)).toBeVisible();
    }
    await expect(page.getByTestId("money-row-model_ev")).toContainText("skip");
  });

  test("sample bundle without depth still renders the original four sections", async ({ authedPage: page }) => {
    await page.route("**/seed.json", (route) => route.abort());
    await page.goto("/#/evidence");
    await expect(page.getByTestId("evidence-view")).toBeVisible();
    await expect(page.getByTestId("refusal-dial-card")).toHaveCount(0);
    await expect(page.getByTestId("money-row-model")).toBeVisible();
  });
});
