# WhyQuiet Operations Runbook

This runbook documents standard operational procedures for WhyQuiet to prevent live demo disruptions, manage credentials safely, and verify platform resilience.

---

## 1. Demo Account Password Rotation

WhyQuiet ships with pre-configured public demo credentials (`analyst@whyquiet.demo` and `approver@whyquiet.demo`) for hackathon judges and evaluators. In the event of password compromise, credential pollution, or pre-judging refresh, follow this end-to-end rotation procedure.

### Step 1: Update Passwords in Supabase Auth

1. Set the new passwords in your local `.env` (or export as environment variables):
   ```bash
   DEMO_ANALYST_PASSWORD="<new-analyst-password>"
   DEMO_APPROVER_PASSWORD="<new-approver-password>"
   ```
2. Execute the idempotent user seeding script:
   ```bash
   uv run --env-file .env python supabase/seed_demo_users.py
   ```
   *Expected output:*
   ```text
   updated analyst@whyquiet.demo -> analyst
   updated approver@whyquiet.demo -> approver
   ```

### Step 2: Update Quick-Fill Passwords in Web Console

1. Open `web/src/App.tsx` and update the `DEMO_PASSWORDS` mapping:
   ```typescript
   const DEMO_PASSWORDS: Record<string, string> = {
     "analyst@whyquiet.demo": "<new-analyst-password>",
     "approver@whyquiet.demo": "<new-approver-password>",
   };
   ```

### Step 3: Verify and Deploy

1. Verify build and tests remain green:
   ```bash
   uv run pytest -q
   cd web && npm run build
   ```
2. Commit and deploy:
   ```bash
   git add web/src/App.tsx
   git commit -m "ops: rotate demo account passwords"
   git push origin main
   ```
3. Test authentication on the live site (`https://whyquiet.vercel.app`):
   ```bash
   curl -s -X POST https://whyquiet.vercel.app/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"analyst@whyquiet.demo","password":"<new-analyst-password>"}'
   ```
   *Expected output:* HTTP 200 with JWT `access_token` and `"role": "analyst"`. Verify the old password returns HTTP 401.

---

## 2. Pre-Demo Wake & Supabase Status Ping

Supabase free-tier projects automatically pause after 7 days of inactivity. To ensure the write path is online before a live demonstration or judging session:

### Step 1: Run Pre-Flight Ping

Execute the Makefile ping target from the repository root:
```bash
make ping
```

*Output when online (Exit code 0):*
```text
OK (https://<project-ref>.supabase.co)
```

*Output when paused or unreachable (Exit code 1):*
```text
PAUSED (HTTP 503)
```

*(Without Make / Direct curl equivalent):*
```bash
URL=$(grep -E '^SUPABASE_URL=' .env | cut -d= -f2- | tr -d '\r')
KEY=$(grep -E '^SUPABASE_SERVICE_ROLE_KEY=' .env | cut -d= -f2- | tr -d '\r')
curl -s -o /dev/null -w "%{http_code}" -H "apikey: $KEY" "$URL/rest/v1/"
```

### Step 2: Unpause / Wake if Paused

1. If `make ping` returns `PAUSED`, log in to the [Supabase Dashboard](https://supabase.com/dashboard).
2. Select the WhyQuiet project.
3. Click **Restore project** / **Unpause project**.
4. Wait 60–90 seconds for compute provisioning.
5. Re-run `make ping` until `OK` is returned.
6. Verify live API status:
   ```bash
   curl -s https://whyquiet.vercel.app/api/health
   ```
   *Expected output:* `{"status":"ok","version":"0.1.0","store":"supabase","stub":false}`.

---

## 3. 503 Offline Banner Verification

WhyQuiet is engineered for zero-crash graceful degradation. If the Supabase write path goes offline or is unconfigured, read screens continue functioning with full diagnostic fidelity from `seed.json`, while write endpoints return HTTP 503 and the UI surfaces an informative offline banner.

### Verification Procedure:

1. **Verify local degradation:**
   - Launch the API with an empty `.env` (no Supabase credentials):
     ```bash
     uv run uvicorn src.api.main:app --port 8008
     ```
   - Query `/api/batches`:
     ```bash
     curl -i http://localhost:8008/api/batches
     ```
     *Expected response:* `HTTP/1.1 503 Service Unavailable`, `{"detail":"Write path offline"}`.
2. **Verify frontend banner:**
   - Run the frontend with `cd web && npm run dev`.
   - Navigate to `http://localhost:5173/#/batches`.
   - Confirm the banner renders: *"Write path offline — running in read-only mode"*.
   - Confirm read routes (`#/`, `#/w/W-1SVVT9`, `#/evidence`) load and operate with zero JavaScript errors.
