import { test, expect } from "@playwright/test";

const CAUSES = ["job_exit", "migration", "solved_problem", "fee_shock", "supply_failure"];

test.describe("Five Causes page", () => {
  test("shows one card per cause with wallets, a remedy and a Bangla message", async ({ page }) => {
    await page.goto("/#/causes");
    await expect(page.getByTestId("causes-view")).toBeVisible();
    for (const c of CAUSES) {
      const card = page.getByTestId(`cause-card-${c}`);
      await expect(card).toBeVisible();
      await expect(page.getByTestId(`cause-count-${c}`)).toHaveText(/^[1-9]\d* wallets$/);
      await expect(card.locator("[lang=bn]")).not.toBeEmpty();
      await expect(card.locator(".recharts-area")).toHaveCount(1);
    }
  });

  test("Propose a batch opens Batches with that cause preselected", async ({ page }) => {
    await page.goto("/#/causes");
    await page.getByTestId("propose-fee_shock").click();
    await expect(page).toHaveURL(/#\/batches\?cause=fee_shock/);
    await expect(page.getByTestId("propose-cause-select")).toHaveValue("fee_shock");
  });

  test("mobile nav reaches the page and the cards fit a 375px screen", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/#/");
    await page.getByRole("navigation", { name: "Mobile Navigation" }).getByRole("link", { name: "Causes" }).click();
    await expect(page.getByTestId("causes-view")).toBeVisible();
    const box = await page.getByTestId("causes-view").boundingBox();
    expect(box!.x + box!.width).toBeLessThanOrEqual(375);
  });
});
