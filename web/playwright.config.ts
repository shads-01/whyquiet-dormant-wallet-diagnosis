import { defineConfig } from "@playwright/test";

// E2E_API_PORT / E2E_WEB_PORT run the suite beside a dev server already on 8008/5173 (vite reads API_PORT).
const api = process.env.E2E_API_PORT ?? "8008";
const web = process.env.E2E_WEB_PORT ?? "5173";

export default defineConfig({
  testDir: "e2e",
  use: { baseURL: `http://localhost:${web}`, reducedMotion: "reduce" },
  webServer: [
    // SCORE_API_KEY lets e2e/score.spec.ts reach the real model without Supabase (D55)
    { command: `cd .. && uv run uvicorn src.api.main:app --port ${api}`, url: `http://localhost:${api}/api/health`, reuseExistingServer: true, timeout: 60000, env: { SCORE_API_KEY: "e2e-score-key" } },
    { command: `npm run dev -- --port ${web} --strictPort`, url: `http://localhost:${web}`, reuseExistingServer: true, timeout: 60000, env: { API_PORT: api } },
  ],
});
