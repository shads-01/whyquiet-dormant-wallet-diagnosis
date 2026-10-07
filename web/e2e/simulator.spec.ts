import { test, expect } from "@playwright/test";

test.describe("Recovery-rate simulator", () => {
  test("agrees with the exported money table at 1%, 4% and 8%", async ({ page }) => {
    await page.goto("/#/evidence");
    await expect(page.getByTestId("simulator-card")).toBeVisible();
    for (const pct of [1, 4, 8]) {
      await page.getByTestId(`rate-toggle-${pct}`).click();
      await page.getByTestId("sim-slider").fill(String(pct / 100));
      for (const s of ["rule", "model", "oracle"]) {
        const table = (await page.getByTestId(`net-value-${s}`).innerText()).replace(/\s/g, "");
        await expect.poll(async () => (await page.getByTestId(`sim-value-${s}`).innerText()).replace(/\s/g, "")).toBe(table);
      }
    }
  });

  test("says which side of the break-even line you are on", async ({ page }) => {
    await page.goto("/#/evidence");
    await page.getByTestId("sim-slider").fill("0.01");
    await expect(page.getByTestId("sim-verdict")).toContainText("blanket message wins");
    await page.getByTestId("sim-slider").fill("0.08");
    await expect(page.getByTestId("sim-verdict")).toContainText("You are above that line");
  });
});
