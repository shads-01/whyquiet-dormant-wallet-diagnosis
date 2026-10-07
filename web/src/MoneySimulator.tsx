import { useMemo, useState } from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, ReferenceLine, Legend, Tooltip } from "recharts";
import { breakEven, simulate } from "./money";
import type { MoneyInputs } from "./seed";
import { Card, Chip } from "./design/ui";

const bdt = (x: number) => `${x < 0 ? "-" : ""}৳${Math.abs(Math.round(x)).toLocaleString("en-US")}`;
const NAMES = { rule: "Blanket SMS (rule)", model: "WhyQuiet model", oracle: "Oracle (upper bound)" } as const;
const COLORS = { rule: "var(--text-muted)", model: "var(--accent)", oracle: "var(--success)" } as const;
const RATES = Array.from({ length: 21 }, (_, i) => i / 200); // 0% .. 10% in 0.5% steps

export default function MoneySimulator({ inputs }: { inputs: MoneyInputs }) {
  const [rate, setRate] = useState(0.04);
  const now = simulate(inputs, rate);
  const even = useMemo(() => breakEven(inputs), [inputs]);
  const curve = useMemo(
    () => RATES.map((r) => {
      const o = simulate(inputs, r);
      return { rate: r, rule: o.rule.value, model: o.model.value, oracle: o.oracle.value };
    }),
    [inputs],
  );

  return (
    <Card className="p-5 sm:p-6 space-y-5" data-testid="simulator-card">
      <div>
        <div className="flex items-center gap-2">
          <h2 className="t-lg font-bold text-[var(--text)]">10. Recovery-Rate Simulator</h2>
          <Chip tone="warning">ASSUMED</Chip>
        </div>
        <p className="t-xs text-[var(--text-muted)] mt-0.5">
          What share of messaged wallets come back is the number we know least. Drag it and see where the targeted
          model starts to beat one blanket SMS to everyone.
        </p>
      </div>

      <label className="block space-y-1">
        <span className="flex justify-between t-sm font-semibold text-[var(--text)]">
          <span>Recovery rate for a correctly targeted remedy</span>
          <span className="font-mono tnum" data-testid="sim-rate">{(rate * 100).toFixed(1)}%</span>
        </span>
        <input
          type="range" min={0} max={0.1} step={0.005} value={rate}
          onChange={(e) => setRate(Number(e.target.value))}
          data-testid="sim-slider" className="w-full" style={{ accentColor: "var(--accent)" }}
        />
      </label>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {(["rule", "model", "oracle"] as const).map((s) => (
          <div key={s} className="p-3 rounded-[var(--radius)] bg-[var(--surface-2)]">
            <div className="t-xs text-[var(--text-muted)]">{NAMES[s]}</div>
            <div
              className={`t-xl font-bold font-mono tnum ${now[s].value >= 0 ? "text-[var(--accent)]" : "text-[var(--danger)]"}`}
              data-testid={`sim-value-${s}`}
            >
              {bdt(now[s].value)}
            </div>
            <div className="t-xs text-[var(--text-faint)]">
              {Math.round(now[s].recovered).toLocaleString()} users back, {bdt(now[s].cost)} spent
            </div>
          </div>
        ))}
      </div>

      <p className="t-sm text-[var(--text)]" data-testid="sim-verdict">
        {even === null
          ? "At no recovery rate does the model beat the blanket SMS under these assumptions."
          : `The model nets more than the blanket SMS once the recovery rate passes ${(even * 100).toFixed(1)}%. ` +
            (rate >= even ? "You are above that line." : "You are below that line: the cheap blanket message wins here.")}
      </p>

      <div className="w-full h-64" role="img" aria-label="Net value in taka against recovery rate for the blanket SMS, the model and the oracle">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={curve} margin={{ top: 10, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
            <XAxis
              type="number" dataKey="rate" domain={[0, 0.1]} ticks={[0, 0.02, 0.04, 0.06, 0.08, 0.1]}
              stroke="var(--text-faint)" fontSize={11} tickFormatter={(v) => `${Math.round(v * 100)}%`}
            />
            <YAxis width={56} stroke="var(--text-faint)" fontSize={11} tickFormatter={(v) => `${v < 0 ? "-" : ""}৳${Math.abs(Math.round(v / 1000))}k`} />
            <Tooltip
              formatter={(v) => bdt(Number(v))} labelFormatter={(v) => `${(Number(v) * 100).toFixed(1)}% recovery`}
              contentStyle={{ backgroundColor: "var(--surface)", borderColor: "var(--border)", borderRadius: "var(--radius-sm)", fontSize: 12 }}
            />
            <Legend />
            {(["rule", "model", "oracle"] as const).map((s) => (
              <Line key={s} type="monotone" dataKey={s} name={NAMES[s]} stroke={COLORS[s]} strokeWidth={s === "model" ? 3 : 2} dot={false} isAnimationActive={false} />
            ))}
            <ReferenceLine x={rate} stroke="var(--accent)" strokeDasharray="4 2" />
            <ReferenceLine y={0} stroke="var(--border)" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
