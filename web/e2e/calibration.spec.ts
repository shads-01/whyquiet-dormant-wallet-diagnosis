import { test, expect } from "./fixtures";

type Seed = { meta: { tau: number; delta: number }; report: { ml: { refusal_rate_b: number; macro_f1_b: number } } };

test.describe("Refusal Dial", () => {
  test("starts on the shipped setting and matches the headline numbers", async ({ authedPage: page, request }) => {
    const seed: Seed = await (await request.get("/seed.json")).json();
    await page.goto("/#/calibration");
    await expect(page.getByTestId("calibration-view")).toBeVisible();
    await expect(page.getByTestId("tau-value")).toHaveText(seed.meta.tau.toFixed(2));
    await expect(page.getByTestId("delta-value")).toHaveText(seed.meta.delta.toFixed(2));
    await expect(page.getByTestId("refusal-rate")).toHaveText(`${(seed.report.ml.refusal_rate_b * 100).toFixed(1)}%`);
    await expect(page.getByTestId("macro-f1")).toHaveText(`${(seed.report.ml.macro_f1_b * 100).toFixed(1)}%`);
    await expect(page.getByTestId("dial-reset")).toBeDisabled();
    await expect(page.getByTestId("flip-summary")).toContainText("Same verdicts as the shipped setting");
  });

  test("a stricter dial refuses more, changes sample verdicts, and reset restores the shipped setting", async ({ authedPage: page }) => {
    await page.goto("/#/calibration");
    const rate = async () => parseFloat((await page.getByTestId("refusal-rate").innerText()).replace("%", ""));
    const before = await rate();
    await page.getByTestId("tau-slider").fill("0.9");
    await page.getByTestId("delta-slider").fill("0.4");
    await expect(page.getByTestId("tau-value")).toHaveText("0.90");
    expect(await rate()).toBeGreaterThan(before);
    await expect(page.getByTestId("flip-summary")).toContainText("differ from the shipped setting");
    await page.getByTestId("dial-reset").click();
    expect(await rate()).toBe(before);
  });
});
