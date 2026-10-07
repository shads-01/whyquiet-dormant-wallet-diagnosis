import { useEffect, useMemo, useState } from "react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid } from "recharts";
import { loadSeed, CAUSE_LABELS, type Cause, type SeedBundle } from "./seed";
import { Card, Chip, Skeleton, ErrorState } from "./design/ui";

const CAUSES = Object.keys(CAUSE_LABELS) as Cause[];
const WINDOW_START = 26; // weeks 26-51: the 26-week window the wallet page draws

type Summary = { count: number; avgSilent: number; avgConfidence: number; shape: { week: number; txns: number }[] };

function summarise(bundle: SeedBundle, cause: Cause): Summary {
  const rows = bundle.wallets.filter((w) => w.verdict === "attributed" && w.cause === cause);
  const sums = new Map<number, { total: number; n: number }>();
  for (const w of rows) {
    for (const s of w.series) {
      if (s.week < WINDOW_START) continue;
      const acc = sums.get(s.week) ?? { total: 0, n: 0 };
      acc.total += s.txn_count;
      acc.n += 1;
      sums.set(s.week, acc);
    }
  }
  const mean = (f: (w: SeedBundle["wallets"][number]) => number) =>
    rows.length ? rows.reduce((t, w) => t + f(w), 0) / rows.length : 0;
  return {
    count: rows.length,
    avgSilent: mean((w) => w.weeks_silent),
    avgConfidence: mean((w) => w.posterior[cause]),
    shape: [...sums].sort((a, b) => a[0] - b[0]).map(([week, a]) => ({ week, txns: Math.round((a.total / a.n) * 100) / 100 })),
  };
}

export default function Causes() {
  const [bundle, setBundle] = useState<SeedBundle | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = () =>
    loadSeed().then(setBundle).catch((e) => setError(e instanceof Error ? e.message : "Failed to load causes."));
  useEffect(() => {
    load();
  }, []);

  const summaries = useMemo(
    () => (bundle ? Object.fromEntries(CAUSES.map((c) => [c, summarise(bundle, c)])) as Record<Cause, Summary> : null),
    [bundle],
  );

  if (error) {
    return <ErrorState title="Could not load causes" body={error} onRetry={() => { setError(null); load(); }} testid="causes-error" />;
  }
  if (!bundle || !summaries) {
    return (
      <div className="space-y-6" data-testid="causes-loading">
        <Skeleton w={280} h={32} />
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {CAUSES.map((c) => <Card key={c} className="p-6"><Skeleton w="100%" h={220} /></Card>)}
        </div>
      </div>
    );
  }

  const refused = bundle.wallets.filter((w) => w.verdict === "refused").length;

  return (
    <div className="space-y-6" data-testid="causes-view">
      <div>
        <h1 className="t-2xl font-bold text-[var(--text)]">Five Causes</h1>
        <p className="t-sm text-[var(--text-muted)] mt-1">
          A wallet going quiet is five different problems with five different fixes. Each card shows what that
          cause looks like in the last 26 weeks of the {bundle.wallets.length}-wallet sample, and the remedy it gets.
          {" "}{refused} sample wallets match none of them cleanly and are refused instead.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {CAUSES.map((cause) => {
          const s = summaries[cause];
          const remedy = bundle.remedies[cause];
          return (
            <Card key={cause} className="p-5 space-y-4 flex flex-col" data-testid={`cause-card-${cause}`}>
              <div className="flex items-start justify-between gap-2">
                <h2 className="t-md font-semibold text-[var(--text)]">{CAUSE_LABELS[cause]}</h2>
                <Chip tone="accent" data-testid={`cause-count-${cause}`}>{s.count} wallets</Chip>
              </div>

              <div
                className="w-full h-32"
                role="img"
                aria-label={`Average weekly transactions for ${CAUSE_LABELS[cause]} wallets over the last 26 weeks`}
              >
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={s.shape} margin={{ top: 4, right: 4, left: -28, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                    <XAxis dataKey="week" stroke="var(--text-faint)" fontSize={10} tickLine={false} interval={4} />
                    <YAxis stroke="var(--text-faint)" fontSize={10} tickLine={false} />
                    <Area type="monotone" dataKey="txns" stroke="var(--accent)" strokeWidth={2} fill="var(--accent-soft)" isAnimationActive={false} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <dl className="grid grid-cols-2 gap-2 t-xs">
                <div>
                  <dt className="text-[var(--text-muted)]">Avg weeks silent</dt>
                  <dd className="font-mono tnum text-[var(--text)]">{s.avgSilent.toFixed(1)}</dd>
                </div>
                <div>
                  <dt className="text-[var(--text-muted)]">Avg confidence</dt>
                  <dd className="font-mono tnum text-[var(--text)]">{(s.avgConfidence * 100).toFixed(0)}%</dd>
                </div>
              </dl>

              <div className="space-y-1 t-xs flex-1">
                <p className="font-semibold text-[var(--text)]">
                  Remedy: {remedy.label} <span className="font-mono text-[var(--text-muted)]">৳{remedy.unit_cost_bdt} each</span>
                  {" "}<Chip tone="warning">ASSUMED</Chip>
                </p>
                <p className="text-[var(--text-muted)]">{remedy.message_en}</p>
                <p lang="bn" className="text-[var(--text-muted)]">{remedy.message_bn}</p>
              </div>

              <a
                href={`#/batches?cause=${cause}`}
                className="btn btn-secondary btn-sm self-start"
                data-testid={`propose-${cause}`}
              >
                Propose a batch for {CAUSE_LABELS[cause]}
              </a>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
