import { test, expect } from "./fixtures";

test.describe("Recovery-rate simulator", () => {
  test("agrees with the exported money table at 1%, 4% and 8%", async ({ authedPage: page, request }) => {
    // D66: The UI table now renders `money_ev` (a different exact-wallet calculation), but the simulator
    // still simulates `money_table` (counts-based). We must verify it against the exported `report.money`.
    const seed = await (await request.get("/seed.json")).json();
    const moneyTable = seed.report.money;
    const formatBDT = (amount: number) =>
      new Intl.NumberFormat("en-BD", { style: "currency", currency: "BDT", maximumFractionDigits: 0 })
        .format(amount)
        .replace("BDT", "৳")
        .trim();

    await page.goto("/#/evidence");
    await expect(page.getByTestId("simulator-card")).toBeVisible();
    for (const pct of [1, 4, 8]) {
      await page.getByTestId(`rate-toggle-${pct}`).click();
      await page.getByTestId("sim-slider").fill(String(pct / 100));
      for (const s of ["rule", "model", "oracle"]) {
        const expectedVal = moneyTable.find((m: any) => m.strategy === s && m.recovery_rate === pct / 100).value_bdt;
        const expectedText = formatBDT(expectedVal).replace(/\s/g, "");
        await expect.poll(async () => (await page.getByTestId(`sim-value-${s}`).innerText()).replace(/\s/g, "")).toBe(expectedText);
      }
    }
  });

  test("says which side of the break-even line you are on", async ({ authedPage: page }) => {
    await page.goto("/#/evidence");
    await page.getByTestId("sim-slider").fill("0.01");
    await expect(page.getByTestId("sim-verdict")).toContainText("blanket message wins");
    await page.getByTestId("sim-slider").fill("0.08");
    await expect(page.getByTestId("sim-verdict")).toContainText("You are above that line");
  });
});
