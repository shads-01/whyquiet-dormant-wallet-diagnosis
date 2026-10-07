import { useId, useState } from "react";
import { scoreWallets, type ScoreResponse, type ScoreResult, type UserSession, type WalletHistory } from "./api";
import { Button, Card, Chip, EmptyState, Table } from "./design/ui";

const HEADER = ["wallet_id", "acquired_week", "fee_week", "pay_cycle"];
const CHUNK = 500; // the API's per-request cap

/** Flat ledger CSV (one row per wallet-week, docs/contracts/ingest.md) -> API wallet objects. */
function parseLedger(text: string): WalletHistory[] {
  const [head, ...lines] = text.trim().split(/\r?\n/);
  const cols = head.replace(/^﻿/, "").split(",").map((c) => c.trim());
  const missing = [...HEADER, "week", "txn_count", "amount_bdt"].filter((c) => !cols.includes(c));
  if (missing.length) throw new Error(`Missing column(s): ${missing.join(", ")}`);
  const wallets = new Map<string, WalletHistory>();
  for (const [n, line] of lines.entries()) {
    if (!line.trim()) continue;
    const cells = line.split(",");
    const rec = Object.fromEntries(cols.map((c, i) => [c, (cells[i] ?? "").trim()]));
    const num = (c: string) => {
      const v = Number(rec[c] || 0);
      if (Number.isNaN(v)) throw new Error(`Row ${n + 2}: ${c} is not a number`);
      return v;
    };
    let w = wallets.get(rec.wallet_id);
    if (!w) {
      w = {
        wallet_id: rec.wallet_id,
        acquired_week: num("acquired_week"),
        fee_week: num("fee_week"),
        pay_cycle: rec.pay_cycle as WalletHistory["pay_cycle"],
        weeks: [],
      };
      wallets.set(rec.wallet_id, w);
    }
    w.weeks.push({
      week: num("week"),
      txn_count: num("txn_count"),
      amount_bdt: num("amount_bdt"),
      cashin_count: num("cashin_count"),
      cashout_ok: num("cashout_ok"),
      cashout_fail: num("cashout_fail"),
      app_share: rec.app_share ? num("app_share") : null,
      district_changed: ["1", "true", "True"].includes(rec.district_changed),
    });
  }
  return [...wallets.values()];
}

function resultsCsv(results: ScoreResult[]): string {
  const esc = (s: string) => (/[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s);
  const rows = results.map((r) =>
    [r.wallet_id, r.verdict, r.cause ?? "", Math.max(0, ...Object.values(r.posterior)).toFixed(3), r.weeks_silent,
      r.remedy?.remedy_code ?? "", r.remedy?.unit_cost_bdt ?? 0, esc(r.refusal_reasons.join(" | "))].join(","));
  return ["wallet_id,verdict,cause,confidence,weeks_silent,remedy_code,unit_cost_bdt,refusal_reasons", ...rows].join("\n");
}

function download(name: string, text: string) {
  const url = URL.createObjectURL(new Blob([text], { type: "text/csv" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

export default function Score({ user, onOpenLogin }: { user: UserSession | null; onOpenLogin: () => void }) {
  const fileId = useId();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [out, setOut] = useState<{ meta: Omit<ScoreResponse, "results">; results: ScoreResult[]; ms: number } | null>(null);

  const run = async (text: string) => {
    setBusy(true);
    setError(null);
    setOut(null);
    try {
      const wallets = parseLedger(text);
      if (!wallets.length) throw new Error("The file has no wallet rows.");
      const start = performance.now();
      const results: ScoreResult[] = [];
      let meta: Omit<ScoreResponse, "results"> | null = null;
      for (let i = 0; i < wallets.length; i += CHUNK) {
        const { results: part, ...m } = await scoreWallets(wallets.slice(i, i + CHUNK));
        results.push(...part);
        meta = m;
      }
      setOut({ meta: meta!, results, ms: performance.now() - start });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Scoring failed.");
    } finally {
      setBusy(false);
    }
  };

  const useSample = async () => {
    const res = await fetch("/sample-ledger.csv");
    await run(await res.text());
  };

  const refused = out?.results.filter((r) => r.verdict === "refused").length ?? 0;

  return (
    <div className="space-y-6" data-testid="score-view">
      <div>
        <h1 className="t-2xl font-bold text-[var(--text)]">Score a Ledger File</h1>
        <p className="text-sm text-[var(--text-muted)] mt-1 max-w-3xl">
          Upload weekly wallet totals exported from the ledger (one row per wallet-week, no names or phone numbers).
          The live model on this server returns a cause or a refusal for each wallet. It is the same model as the
          Triage Queue. upay systems can call the same endpoint with an API key:{" "}
          <a href="/api/docs#/default/score_api_score_post" className="text-[var(--accent)] underline">POST /api/score</a>.
        </p>
      </div>

      {!user ? (
        <EmptyState
          title="Sign in to score"
          body="Live scoring runs on the server, so it needs an analyst or approver account. The demo accounts work."
          action={<Button onClick={onOpenLogin} data-testid="score-sign-in">Sign in</Button>}
          testid="score-signin-required"
        />
      ) : (
        <Card className="p-4 flex flex-wrap items-center gap-3">
          <label htmlFor={fileId} className="btn btn-primary has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-[var(--ring)]">
            Upload CSV
          </label>
          {/* Not .sr-only: that class un-clips on :focus, so the dialog's focus would insert the input and shove the buttons aside. */}
          <input
            id={fileId}
            type="file"
            accept=".csv,text/csv"
            className="absolute w-px h-px opacity-0 pointer-events-none"
            data-testid="score-file-input"
            disabled={busy}
            onChange={async (e) => {
              const f = e.target.files?.[0];
              if (f) await run(await f.text());
              e.target.value = "";
            }}
          />
          <Button variant="secondary" onClick={useSample} loading={busy} data-testid="score-sample-btn">
            Score the sample ledger
          </Button>
          <a href="/sample-ledger.csv" download className="text-xs text-[var(--accent)] underline">
            Download sample CSV (20 wallets)
          </a>
          {busy && <span role="status" className="text-xs text-[var(--text-muted)]">Scoring…</span>}
        </Card>
      )}

      {error && (
        <div role="alert" className="text-sm text-[var(--danger)]" data-testid="score-error">
          {error}
        </div>
      )}

      {out && (
        <div className="space-y-3" data-testid="score-results">
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <Chip tone="accent">{out.results.length} wallets scored</Chip>
            <Chip tone="success">{out.results.length - refused} attributed</Chip>
            <Chip tone="warning">{refused} refused</Chip>
            <Chip>model {out.meta.model_version} · τ {out.meta.tau} · δ {out.meta.delta}</Chip>
            <Chip>{Math.round(out.ms)} ms round trip</Chip>
            <Button variant="ghost" size="sm" onClick={() => download("triage.csv", resultsCsv(out.results))}>
              Download results CSV
            </Button>
          </div>
          <Table testid="score-table">
            <thead>
              <tr>
                <th scope="col">Wallet</th>
                <th scope="col">Verdict</th>
                <th scope="col">Cause</th>
                <th scope="col">Confidence</th>
                <th scope="col">Weeks silent</th>
                <th scope="col">Remedy</th>
                <th scope="col">Why refused</th>
              </tr>
            </thead>
            <tbody>
              {out.results.map((r) => (
                <tr key={r.wallet_id} data-testid={`score-row-${r.wallet_id}`}>
                  <th scope="row" className="font-mono">{r.wallet_id}</th>
                  <td>
                    <Chip tone={r.verdict === "attributed" ? "success" : "warning"}>{r.verdict}</Chip>
                  </td>
                  <td>{r.cause ?? "—"}</td>
                  <td>{Object.keys(r.posterior).length ? Math.max(...Object.values(r.posterior)).toFixed(2) : "—"}</td>
                  <td>{r.weeks_silent}</td>
                  <td>{r.remedy ? `${r.remedy.label} (৳${r.remedy.unit_cost_bdt})` : "—"}</td>
                  <td className="text-[var(--text-muted)]">{r.refusal_reasons.join("; ") || "—"}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      )}
    </div>
  );
}
