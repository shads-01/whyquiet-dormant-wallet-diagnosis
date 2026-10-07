import { test, expect } from "@playwright/test";

test.describe("Evidence & ML Rigor Page", () => {
  test("displays ML rigor panel, reliability diagram, and per-cause F1 breakdown", async ({ page }) => {
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

    // Reliability Diagram (Confidence Calibration)
    const reliabilityCard = page.getByTestId("reliability-diagram-card");
    await expect(reliabilityCard).toBeVisible();
    await expect(page.getByTestId("reliability-diagram-chart")).toBeVisible();
  });

  test("displays confusion matrix, per-cause F1 breakdown, and demographic parity fairness tables", async ({ page }) => {
    await page.goto("/#/evidence");

    // Confusion Matrix Table
    const cmCard = page.getByTestId("confusion-matrix-card");
    await expect(cmCard).toBeVisible();
    const cmTable = page.getByTestId("confusion-matrix-table");
    await expect(cmTable).toBeVisible();
    await expect(cmTable.locator("tbody tr")).toHaveCount(5);

    // Per-Cause F1 Breakdown Table
    const perCauseCard = page.getByTestId("per-cause-f1-card");
    await expect(perCauseCard).toBeVisible();
    const perCauseTable = page.getByTestId("per-cause-f1-table");
    await expect(perCauseTable).toBeVisible();
    await expect(perCauseTable.locator("tbody tr")).toHaveCount(5);

    // Fairness Table
    const fairnessCard = page.getByTestId("fairness-card");
    await expect(fairnessCard).toBeVisible();
    const fairnessTable = page.getByTestId("fairness-table");
    await expect(fairnessTable).toBeVisible();
    await expect(fairnessTable.locator("tbody tr")).not.toHaveCount(0);
  });

  test("economic recovery section: handles rate toggling and renders ASSUMED badges", async ({ page }) => {
    await page.goto("/#/evidence");

    // Break-even and Cost Sweep Panels
    await expect(page.getByTestId("break-even-panel")).toBeVisible();
    await expect(page.getByTestId("cost-sweep-panel")).toBeVisible();
    await expect(page.getByTestId("cost-sweep-table")).toBeVisible();

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

  test("displays refusal validity audit and falsifiability exhibits with calibrated numbers", async ({ page }) => {
    await page.goto("/#/evidence");

    // 5. Refusal Validity Audit
    const refusalCard = page.getByTestId("refusal-validity-card");
    await expect(refusalCard).toBeVisible();
    await expect(page.getByTestId("enrichment-ratio-value")).toContainText("×");
    await expect(page.getByTestId("forced-error-refused-value")).toContainText("%");
    await expect(page.getByTestId("forced-error-attr-value")).toContainText("%");
    await expect(page.getByTestId("refusal-caveat-text")).toContainText(
      "Refusal is calibrated against the simulator's own ambiguity flag; whether real ambiguity looks like ours is what real upay data would answer first."
    );

    // 6. Falsifiability & Robustness Stress-Testing
    const falsifiabilityCard = page.getByTestId("falsifiability-card");
    await expect(falsifiabilityCard).toBeVisible();
    await expect(page.getByTestId("verdict-flip-rate-value")).toContainText("%");
    await expect(page.getByTestId("pop-c-f1-value")).toContainText("%");
    await expect(page.getByTestId("pop-c-refusal-value")).toContainText("%");
    await expect(page.getByTestId("pilot-sample-size-value")).toContainText("wallets / arm");
    await expect(page.getByTestId("falsifiability-caveat-text")).toContainText(
      "Refusal is calibrated against the simulator's own ambiguity flag; whether real ambiguity looks like ours is what real upay data would answer first."
    );
  });

  test("mobile responsive view at 375px width", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/#/evidence");

    await expect(page.getByTestId("evidence-view")).toBeVisible();
    await expect(page.getByTestId("headline-f1-card")).toBeVisible();
    await expect(page.getByTestId("confusion-matrix-table")).toBeVisible();
    await expect(page.getByTestId("money-card")).toBeVisible();
    await expect(page.getByTestId("refusal-validity-card")).toBeVisible();
    await expect(page.getByTestId("falsifiability-card")).toBeVisible();
  });
});
