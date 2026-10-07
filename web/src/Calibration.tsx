import { useEffect, useMemo, useState } from "react";
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, ZAxis } from "recharts";
import { loadSeed, type RefusalPoint, type SeedBundle } from "./seed";
import { Button, Card, Chip, EmptyState, ErrorState, Skeleton } from "./design/ui";

const TAU = { min: 0.5, max: 0.9 };
const DELTA = { min: 0.1, max: 0.4 };
const pct = (x: number, digits = 1) => `${(x * 100).toFixed(digits)}%`;
const same = (a: number, b: number) => Math.abs(a - b) < 1e-6;

// Same rule as src/model/score.py `decide`: refuse when the top cause is below tau or leads the runner-up by less than delta.
function refuses(posterior: Record<string, number>, tau: number, delta: number): boolean {
  const [first = 0, second = 0] = Object.values(posterior).sort((a, b) => b - a);
  return first < tau - 1e-9 || first - second < delta - 1e-9;
}

export default function Calibration() {
  const [bundle, setBundle] = useState<SeedBundle | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tau, setTau] = useState<number | null>(null);
  const [delta, setDelta] = useState<number | null>(null);

  const load = () =>
    loadSeed()
      .then((b) => {
        setBundle(b);
        setTau(b.meta.tau);
        setDelta(b.meta.delta);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load calibration data."));
  useEffect(() => {
    load();
  }, []);

  const sweep = bundle?.report.refusal_sweep;
  const now = useMemo(
    () => (tau === null || delta === null ? undefined : sweep?.find((p) => same(p.tau, tau) && same(p.delta, delta))),
    [sweep, tau, delta],
  );
  const shipped = useMemo(
    () => (bundle ? sweep?.find((p) => same(p.tau, bundle.meta.tau) && same(p.delta, bundle.meta.delta)) : undefined),
    [sweep, bundle],
  );
  const flipped = useMemo(() => {
    if (!bundle || tau === null || delta === null) return [];
    return bundle.wallets.filter((w) => refuses(w.posterior, tau, delta) !== (w.verdict === "refused"));
  }, [bundle, tau, delta]);

  if (error) return <ErrorState title="Could not load calibration data" body={error} onRetry={() => { setError(null); load(); }} testid="calibration-error" />;
  if (!bundle || tau === null || delta === null) {
    return (
      <div className="space-y-6" data-testid="calibration-loading">
        <Skeleton w={280} h={32} />
        <Card className="p-6"><Skeleton w="100%" h={260} /></Card>
      </div>
    );
  }
  if (!sweep?.length) {
    return (
      <EmptyState
        title="Refusal sweep not exported yet"
        body="Re-run scripts/export_seed.py to add report.refusal_sweep to seed.json."
        testid="calibration-pending"
      />
    );
  }

  const stillAttributed = bundle.wallets.length - bundle.wallets.filter((w) => refuses(w.posterior, tau, delta)).length;
  const isShipped = same(tau, bundle.meta.tau) && same(delta, bundle.meta.delta);
  const others = sweep.filter((p) => p !== now && p !== shipped);

  return (
    <div className="space-y-6" data-testid="calibration-view">
      <div>
        <h1 className="t-2xl font-bold text-[var(--text)]">Refusal Dial</h1>
        <p className="t-sm text-[var(--text-muted)] mt-1">
          The model refuses a wallet when its best guess is not confident enough (<b>tau</b>) or barely beats the
          runner-up (<b>delta</b>). Turn the dial up and it refuses more but is right more often on the rest; turn it
          down and more wallets get a remedy, with more mistakes. Scored on all {bundle.meta.n_wallets_b_total.toLocaleString()} population B wallets.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 sm:p-6 space-y-5" data-testid="dial-card">
          <label className="block space-y-1">
            <span className="flex justify-between t-sm font-semibold text-[var(--text)]">
              <span>Confidence bar (tau)</span>
              <span className="font-mono tnum" data-testid="tau-value">{tau.toFixed(2)}</span>
            </span>
            <input
              type="range" min={TAU.min} max={TAU.max} step={0.05} value={tau}
              onChange={(e) => setTau(Number(e.target.value))}
              data-testid="tau-slider" className="w-full" style={{ accentColor: "var(--accent)" }}
            />
          </label>
          <label className="block space-y-1">
            <span className="flex justify-between t-sm font-semibold text-[var(--text)]">
              <span>Lead over runner-up (delta)</span>
              <span className="font-mono tnum" data-testid="delta-value">{delta.toFixed(2)}</span>
            </span>
            <input
              type="range" min={DELTA.min} max={DELTA.max} step={0.05} value={delta}
              onChange={(e) => setDelta(Number(e.target.value))}
              data-testid="delta-slider" className="w-full" style={{ accentColor: "var(--accent)" }}
            />
          </label>

          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-[var(--radius)] bg-[var(--surface-2)]">
              <div className="t-xs text-[var(--text-muted)]">Refusal rate (population B)</div>
              <div className="t-xl font-bold font-mono tnum text-[var(--text)]" data-testid="refusal-rate">
                {now ? pct(now.refusal_rate) : "n/a"}
              </div>
              {shipped && <div className="t-xs text-[var(--text-faint)]">shipped: {pct(shipped.refusal_rate)}</div>}
            </div>
            <div className="p-3 rounded-[var(--radius)] bg-[var(--surface-2)]">
              <div className="t-xs text-[var(--text-muted)]">Macro-F1 on the wallets kept</div>
              <div className="t-xl font-bold font-mono tnum text-[var(--text)]" data-testid="macro-f1">
                {now ? pct(now.macro_f1) : "n/a"}
              </div>
              {shipped && <div className="t-xs text-[var(--text-faint)]">shipped: {pct(shipped.macro_f1)}</div>}
            </div>
          </div>

          <div className="flex items-center justify-between gap-3">
            {isShipped ? <Chip tone="success">Shipped setting</Chip> : <Chip tone="warning">Not the shipped setting</Chip>}
            <Button
              variant="secondary" size="sm" disabled={isShipped} data-testid="dial-reset"
              onClick={() => { setTau(bundle.meta.tau); setDelta(bundle.meta.delta); }}
            >
              Reset to shipped
            </Button>
          </div>
        </Card>

        <Card className="p-5 sm:p-6 space-y-3" data-testid="tradeoff-card">
          <h2 className="t-md font-semibold text-[var(--text)]">Every setting the tuner tried</h2>
          <div
            className="w-full h-64"
            role="img"
            aria-label="Scatter of refusal rate against macro-F1 for every tau and delta pair, with the current setting highlighted"
          >
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 10, left: -10, bottom: 18 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis
                  type="number" dataKey="refusal_rate" domain={["auto", "auto"]} stroke="var(--text-faint)" fontSize={11}
                  tickFormatter={(v) => pct(v, 0)} label={{ value: "Refusal rate", position: "insideBottom", offset: -10, fontSize: 11, fill: "var(--text-muted)" }}
                />
                <YAxis
                  type="number" dataKey="macro_f1" domain={["auto", "auto"]} stroke="var(--text-faint)" fontSize={11}
                  tickFormatter={(v) => pct(v, 0)}
                />
                <ZAxis range={[40, 40]} />
                <Scatter data={others as RefusalPoint[]} fill="var(--text-faint)" fillOpacity={0.5} isAnimationActive={false} />
                {shipped && <Scatter data={[shipped]} fill="var(--warning)" isAnimationActive={false} />}
                {now && <Scatter data={[now]} fill="var(--accent)" shape="diamond" isAnimationActive={false} />}
              </ScatterChart>
            </ResponsiveContainer>
          </div>
          <p className="t-xs text-[var(--text-muted)]">
            Faded dots: other settings. Amber dot: shipped. Diamond: your dial. Up and to the left is better (fewer refusals, higher accuracy).
          </p>
        </Card>
      </div>

      <Card className="p-5 sm:p-6 space-y-3" data-testid="flip-card">
        <h2 className="t-md font-semibold text-[var(--text)]">What changes in the {bundle.wallets.length}-wallet sample</h2>
        <p className="t-sm text-[var(--text-muted)]" data-testid="flip-summary">
          {stillAttributed} wallets get a cause, {bundle.wallets.length - stillAttributed} are refused.{" "}
          {flipped.length === 0 ? "Same verdicts as the shipped setting." : `${flipped.length} differ from the shipped setting.`}
        </p>
        {flipped.length > 0 && (
          <ul className="flex flex-wrap gap-2">
            {flipped.slice(0, 12).map((w) => (
              <li key={w.wallet_id}>
                <a href={`#/w/${w.wallet_id}`} className="chip chip-neutral font-mono">
                  {w.wallet_id} {w.verdict === "refused" ? "now gets a cause" : "now refused"}
                </a>
              </li>
            ))}
            {flipped.length > 12 && <li className="t-xs text-[var(--text-muted)] self-center">and {flipped.length - 12} more</li>}
          </ul>
        )}
      </Card>
    </div>
  );
}
