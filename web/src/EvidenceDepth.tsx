// Phase 2 evidence sections (D66): data comes from report.depth, written by scripts/depth.py.
import type { ReactNode } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ReferenceDot,
  ReferenceLine,
} from "recharts";
import type { Cause, Depth } from "./seed";
import { Card, Chip, Table } from "./design/ui";

const CAUSE_LABELS: Record<Cause, string> = {
  job_exit: "Job Exit",
  migration: "Migration",
  solved_problem: "Solved Problem",
  fee_shock: "Fee Shock",
  supply_failure: "Supply Failure",
};

const pct = (x: number, digits = 1) => `${(x * 100).toFixed(digits)}%`;
const causeLabel = (c: string) => CAUSE_LABELS[c as Cause] ?? c.replace("_", " ");

const TOOLTIP_STYLE = {
  backgroundColor: "var(--surface)",
  borderColor: "var(--border)",
  borderRadius: "var(--radius-sm)",
  fontSize: 12,
};

const BASELINE_LABELS: Record<string, string> = {
  majority: "Always guess the most common cause",
  expert_rule: "Hand-written analyst rules",
  logreg: "Logistic regression (answers every wallet)",
  lightgbm: "LightGBM (answers every wallet)",
  lightgbm_refusal: "LightGBM with calibrated refusal (shipped)",
};

const FAMILY_LABELS: Record<string, string> = {
  volume_shape: "Volume & decline shape",
  salary_cashin: "Salary / cash-in rhythm",
  fee_ticket: "Fee & ticket size",
  agent_failures: "Agent cash-out failures",
  location_channel: "Location & channel",
  burst: "One-off burst",
};

function Section({ n, title, lead, testid, children }: { n: number; title: string; lead: ReactNode; testid: string; children: ReactNode }) {
  return (
    <Card className="p-5 sm:p-6 space-y-5" data-testid={testid}>
      <div>
        <h2 className="t-md font-semibold text-[var(--text)]">
          {n}. {title}
        </h2>
        <p className="t-xs text-[var(--text-muted)] mt-0.5 max-w-3xl">{lead}</p>
      </div>
      {children}
    </Card>
  );
}

function Stat({ label, value, note, testid, strong }: { label: string; value: string; note: string; testid?: string; strong?: boolean }) {
  return (
    <div className="p-4 rounded-[var(--radius)] bg-[var(--surface-2)] border border-[var(--border)]">
      <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">{label}</div>
      <div className={`t-xl font-bold font-mono mt-1 ${strong ? "text-[var(--accent)]" : "text-[var(--text)]"}`} data-testid={testid}>
        {value}
      </div>
      <p className="text-xs text-[var(--text-faint)] mt-1">{note}</p>
    </div>
  );
}

/* Refusal as a dial, and the baseline ladder. */
export function RefusalDialSection({ depth, n }: { depth: Depth; n: number }) {
  const { coverage, baselines, group_shift, macro_f1_b_ci95: ci } = depth;
  const curve = (pts: Depth["coverage"]["lightgbm"]) => pts.map((p) => ({ x: p.coverage * 100, y: p.macro_f1 * 100 }));
  const op = coverage.operating_point;
  const lgbmWins = group_shift.filter((g) => g.lightgbm > g.logreg).length;
  return (
    <Section
      n={n}
      testid="refusal-dial-card"
      title="Refusal Is a Dial, Not a Trick"
      lead={
        <>
          The headline counts only the wallets the model agrees to answer. This curve shows the whole trade-off: answer every
          wallet and macro-F1 is {pct(coverage.lightgbm[0].macro_f1)}; answer fewer, and every answer gets better. The shipped
          τ/δ setting answers {pct(op.coverage)} of B at {pct(op.macro_f1)} (95% bootstrap interval {pct(ci[0])}–{pct(ci[1])}).
        </>
      }
    >
      <div className="w-full h-72" role="img" aria-label="Macro-F1 against share of wallets answered, LightGBM versus logistic regression">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart margin={{ top: 10, right: 20, left: 0, bottom: 18 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis
              type="number"
              dataKey="x"
              domain={[40, 100]}
              reversed
              stroke="var(--text-muted)"
              fontSize={11}
              tickFormatter={(v) => `${v}%`}
              label={{ value: "Share of wallets answered", position: "insideBottom", offset: -10, fill: "var(--text-muted)", fontSize: 11 }}
            />
            <YAxis type="number" domain={[70, 100]} ticks={[70, 80, 90, 100]} stroke="var(--text-faint)" fontSize={11} tickFormatter={(v) => `${v}%`} />
            <Tooltip contentStyle={TOOLTIP_STYLE} formatter={(v: any) => `${Number(v).toFixed(1)}%`} labelFormatter={(v: any) => `${Number(v).toFixed(0)}% answered`} />
            <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: 12 }} />
            <Line data={curve(coverage.lightgbm)} dataKey="y" name="LightGBM (shipped)" stroke="var(--accent)" strokeWidth={2} dot={{ r: 4 }} />
            <Line data={curve(coverage.logreg)} dataKey="y" name="Logistic regression" stroke="var(--text-muted)" strokeWidth={2} strokeDasharray="6 4" dot={{ r: 4, strokeDasharray: "none" }} activeDot={{ r: 6, strokeDasharray: "none" }} />
            <ReferenceDot
              x={op.coverage * 100}
              y={op.macro_f1 * 100}
              r={7}
              fill="var(--accent)"
              stroke="var(--surface)"
              strokeWidth={2}
              label={{ value: "shipped τ/δ", position: "top", fill: "var(--text)", fontSize: 11 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Table testid="baseline-ladder-table">
          <thead>
            <tr>
              <th scope="col">Baseline ladder (population B)</th>
              <th scope="col" className="text-right">Answers</th>
              <th scope="col" className="text-right">Macro-F1</th>
            </tr>
          </thead>
          <tbody>
            {baselines.map((b) => (
              <tr key={b.name}>
                <td className={b.name === "lightgbm_refusal" ? "font-semibold text-[var(--text)]" : "text-[var(--text)]"}>{BASELINE_LABELS[b.name] ?? b.name}</td>
                <td className="text-right font-mono tnum text-[var(--text-muted)]">{pct(b.coverage, 0)}</td>
                <td className="text-right font-mono tnum font-semibold text-[var(--accent)]">{pct(b.macro_f1_b)}</td>
              </tr>
            ))}
          </tbody>
        </Table>
        <div className="space-y-3 text-xs text-[var(--text-muted)]">
          <p>
            <span className="font-semibold text-[var(--text)]">Honest finding:</span> forced to answer every wallet, logistic regression ties LightGBM on B.
            LightGBM earns its place by knowing which of its answers are wrong: its risk-coverage area is{" "}
            <span className="font-mono text-[var(--text)]">{coverage.aurc.lightgbm.toFixed(3)}</span> against{" "}
            <span className="font-mono text-[var(--text)]">{coverage.aurc.logreg.toFixed(3)}</span> (lower is better), so it wins at every refusal level.
          </p>
          <p>
            Holding out one pay cycle at a time inside population A (a shift we can make without touching B), LightGBM beats logistic regression in{" "}
            {lgbmWins} of {group_shift.length} folds:
          </p>
          <Table testid="group-shift-table">
            <thead>
              <tr>
                <th scope="col">Held-out pay cycle</th>
                <th scope="col" className="text-right">LightGBM</th>
                <th scope="col" className="text-right">Log. reg.</th>
              </tr>
            </thead>
            <tbody>
              {group_shift.map((g) => (
                <tr key={g.held_out}>
                  <td className="capitalize text-[var(--text)]">{g.held_out}</td>
                  <td className="text-right font-mono tnum text-[var(--accent)]">{pct(g.lightgbm)}</td>
                  <td className="text-right font-mono tnum text-[var(--text-muted)]">{pct(g.logreg)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </div>
    </Section>
  );
}

/* Where it is right and wrong: per cause, blended wallets, feature-family ablation. */
export function ErrorAnatomySection({ depth, n }: { depth: Depth; n: number }) {
  const clean = depth.blended.find((b) => b.group === "clean");
  const mixed = depth.blended.find((b) => b.group === "blended");
  return (
    <Section
      n={n}
      testid="error-anatomy-card"
      title="Where It Is Right, Where It Is Wrong, and Why"
      lead="Per-cause scores, what refusal does with deliberately mixed-cause wallets, and which signal each cause depends on (drop one feature family, retrain, re-score B)."
    >
      {clean && mixed && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4" data-testid="blended-tiles">
          <Stat
            label="Clean wallets (one cause)"
            value={`${pct(clean.refusal_rate)} refused`}
            note={`${clean.n.toLocaleString()} wallets · ${pct(clean.accuracy_attributed)} accurate when answered`}
          />
          <Stat
            label="Blended wallets (two causes mixed)"
            value={`${pct(mixed.refusal_rate)} refused`}
            strong
            note={`${mixed.n.toLocaleString()} wallets · ${pct(mixed.accuracy_attributed)} accurate when answered. Refusal finds the ambiguous ones without being told which they are.`}
          />
        </div>
      )}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Table testid="per-class-table">
          <thead>
            <tr>
              <th scope="col">Cause</th>
              <th scope="col" className="text-right">F1 answered</th>
              <th scope="col" className="text-right">F1 all</th>
              <th scope="col" className="text-right">Refused</th>
            </tr>
          </thead>
          <tbody>
            {depth.per_class.map((c) => (
              <tr key={c.cause}>
                <td className="text-[var(--text)]">{CAUSE_LABELS[c.cause]}</td>
                <td className="text-right font-mono tnum text-[var(--accent)] font-semibold">{pct(c.f1_attributed)}</td>
                <td className="text-right font-mono tnum text-[var(--text)]">{pct(c.f1_all)}</td>
                <td className="text-right font-mono tnum text-[var(--text-muted)]">{pct(c.refusal_rate)}</td>
              </tr>
            ))}
          </tbody>
        </Table>
        <Table testid="ablation-table">
          <thead>
            <tr>
              <th scope="col">Feature family removed</th>
              <th scope="col">Cause hurt most</th>
              <th scope="col" className="text-right">Its F1 drop</th>
            </tr>
          </thead>
          <tbody>
            {depth.ablation.map((a) => (
              <tr key={a.group}>
                <td className="text-[var(--text)]" title={a.features.join(", ")}>
                  {FAMILY_LABELS[a.group] ?? a.group}
                </td>
                <td className="text-[var(--text)]">{CAUSE_LABELS[a.most_hurt]}</td>
                <td className="text-right font-mono tnum font-semibold text-[var(--danger)]">−{(a.most_hurt_drop * 100).toFixed(1)} pts</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
      <p className="text-xs text-[var(--text-faint)]">
        Each family carries the cause it was designed for (salary rhythm → job exit, failures → supply failure, location → migration, fees → fee shock),
        which is evidence the model reads mechanisms, not simulator quirks. Burst and volume overlap, so removing either alone barely hurts solved-problem.
      </p>
    </Section>
  );
}

/* Calibration: fine in-distribution, overconfident under shift. */
export function CalibrationSection({ depth, n }: { depth: Depth; n: number }) {
  const cal = depth.calibration;
  const pts = (bins: Depth["calibration"]["reliability_a"]) =>
    bins.filter((b) => b.n >= 10).map((b) => ({ x: b.confidence * 100, y: b.accuracy * 100, n: b.n }));
  return (
    <Section
      n={n}
      testid="calibration-card"
      title="Calibration Under Shift"
      lead={
        <>
          On population A the model means what it says (calibration error {cal.ece_a_test.toFixed(3)}). On shifted B it is overconfident
          (error {cal.ece_b.toFixed(3)}): wallets it scores 85% sure are right about two times in three. Re-scaling on A does not help (best temperature{" "}
          {cal.temperature.toFixed(2)}, B error {cal.ece_b_after_temperature.toFixed(3)}), because the cause is the shift, not the training. That is why
          the next section estimates accuracy on unlabeled data instead of trusting confidence.
        </>
      }
    >
      <div className="w-full h-72" role="img" aria-label="Reliability diagram: confidence against observed accuracy for population A test and population B">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart margin={{ top: 10, right: 20, left: 0, bottom: 18 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis
              type="number"
              dataKey="x"
              domain={[20, 100]}
              stroke="var(--text-muted)"
              fontSize={11}
              tickFormatter={(v) => `${v}%`}
              label={{ value: "Model confidence", position: "insideBottom", offset: -10, fill: "var(--text-muted)", fontSize: 11 }}
            />
            <YAxis type="number" domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} stroke="var(--text-faint)" fontSize={11} tickFormatter={(v) => `${v}%`} />
            <Tooltip contentStyle={TOOLTIP_STYLE} formatter={(v: any) => `${Number(v).toFixed(1)}% right`} labelFormatter={(v: any) => `${Number(v).toFixed(0)}% confident`} />
            <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: 12 }} />
            <ReferenceLine segment={[{ x: 20, y: 20 }, { x: 100, y: 100 }]} stroke="var(--border-strong)" strokeDasharray="3 3" />
            <Line data={pts(cal.reliability_a)} dataKey="y" name="Population A-test" stroke="var(--accent)" strokeWidth={2} dot={{ r: 4 }} />
            <Line data={pts(cal.reliability_b)} dataKey="y" name="Population B (shifted)" stroke="var(--text-muted)" strokeWidth={2} strokeDasharray="6 4" dot={{ r: 4, strokeDasharray: "none" }} activeDot={{ r: 6, strokeDasharray: "none" }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="text-xs text-[var(--text-faint)]">Dashed diagonal = perfect calibration. Bins with fewer than 10 wallets are hidden.</p>
    </Section>
  );
}

/* What still works on a real ledger with no cause labels. */
export function LabelFreeSection({ depth, n }: { depth: Depth; n: number }) {
  const lf = depth.label_free;
  const err = lf.cause_mix_max_error;
  return (
    <Section
      n={n}
      testid="label-free-card"
      title="Real-World Readiness: Checks That Need No Labels"
      lead="A real upay ledger has no cause column. These three checks run on unlabeled data, so they work on day one of a pilot. We test them here on B, where we secretly know the truth."
    >
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4" data-testid="label-free-accuracy">
        <Stat label="Model's own confidence" value={pct(lf.accuracy.confidence)} note="What the model would claim on B. Too optimistic." />
        <Stat
          label="Estimated accuracy (no labels)"
          value={pct(lf.accuracy.atc_estimate)}
          strong
          testid="atc-estimate-value"
          note={`ATC method, cut learned on A. On A-test it predicts ${pct(lf.accuracy_a_test.atc_estimate)} vs true ${pct(lf.accuracy_a_test.true)}.`}
        />
        <Stat label="True accuracy on B" value={pct(lf.accuracy.true)} note="Known only because B is simulated." />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="space-y-2">
          <div className="text-xs font-semibold text-[var(--text)]">Cause mix of the dormant base, estimated without labels</div>
          <Table testid="cause-mix-table">
            <thead>
              <tr>
                <th scope="col">Cause</th>
                <th scope="col" className="text-right">Assume A's mix</th>
                <th scope="col" className="text-right">EM estimate</th>
                <th scope="col" className="text-right">True</th>
              </tr>
            </thead>
            <tbody>
              {lf.cause_mix.map((m) => (
                <tr key={m.cause}>
                  <td className="text-[var(--text)]">{CAUSE_LABELS[m.cause]}</td>
                  <td className="text-right font-mono tnum text-[var(--text-muted)]">{pct(m.train)}</td>
                  <td className="text-right font-mono tnum font-semibold text-[var(--accent)]">{pct(m.em)}</td>
                  <td className="text-right font-mono tnum text-[var(--text)]">{pct(m.true)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
          <p className="text-xs text-[var(--text-faint)]">
            Largest error: {pct(err.train)} if you assume the training mix, {pct(err.argmax)} counting top causes, {pct(err.em)} with EM prior adjustment. That
            tells operations how big each remedy budget should be before a single message is sent.
          </p>
        </div>
        <div className="space-y-2">
          <div className="text-xs font-semibold text-[var(--text)]">Drift alarm: which signals moved between A and B</div>
          <Table testid="drift-table">
            <thead>
              <tr>
                <th scope="col">Feature</th>
                <th scope="col" className="text-right">PSI</th>
                <th scope="col" className="text-right">Level</th>
              </tr>
            </thead>
            <tbody>
              {lf.drift.psi.slice(0, 6).map((d) => (
                <tr key={d.feature}>
                  <td>
                    <code className="font-mono text-[var(--text)]">{d.feature}</code>
                  </td>
                  <td className="text-right font-mono tnum text-[var(--text)]">{d.psi.toFixed(2)}</td>
                  <td className="text-right">
                    <Chip tone={d.psi >= 0.25 ? "danger" : d.psi >= 0.1 ? "warning" : "neutral"}>
                      {d.psi >= 0.25 ? "major" : d.psi >= 0.1 ? "moderate" : "stable"}
                    </Chip>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          <p className="text-xs text-[var(--text-faint)]">
            A classifier tells A from B with AUC {lf.drift.domain_auc.toFixed(2)}, so a monitor would flag this population before anyone trusted old accuracy
            numbers. PSI bands 0.1 / 0.25 are a common credit-risk rule of thumb (UNVERIFIED).
          </p>
        </div>
      </div>
    </Section>
  );
}

/* Stress tests: a noise dial and a cause the model has never seen. */
export function StressSection({ depth, n }: { depth: Depth; n: number }) {
  const { noise_dial: dial, unseen_cause: u } = depth.stress;
  const named = Object.entries(u.named_as).sort((a, b) => b[1] - a[1]);
  return (
    <Section
      n={n}
      testid="stress-card"
      title="Stress Tests: When Reality Surprises the Model"
      lead="Fresh populations built in memory, never trained on: B with the noise and cause-mixing turned up step by step, and B with a sixth cause the model has never seen."
    >
      <Table testid="noise-dial-table">
        <thead>
          <tr>
            <th scope="col">Noise level</th>
            <th scope="col" className="text-right">Mixed wallets</th>
            <th scope="col" className="text-right">Macro-F1 answered</th>
            <th scope="col" className="text-right">Refused</th>
            <th scope="col" className="text-right">True accuracy</th>
            <th scope="col" className="text-right">No-label estimate</th>
            <th scope="col" className="text-right">Confidence says</th>
          </tr>
        </thead>
        <tbody>
          {dial.map((d) => (
            <tr key={d.level}>
              <td className="font-semibold text-[var(--text)]">{d.level}</td>
              <td className="text-right font-mono tnum text-[var(--text-muted)]">{pct(d.blended, 0)}</td>
              <td className="text-right font-mono tnum text-[var(--accent)] font-semibold">{pct(d.macro_f1)}</td>
              <td className="text-right font-mono tnum text-[var(--text)]">{pct(d.refusal_rate)}</td>
              <td className="text-right font-mono tnum text-[var(--text)]">{pct(d.accuracy_true)}</td>
              <td className="text-right font-mono tnum text-[var(--text)]">{pct(d.accuracy_atc)}</td>
              <td className="text-right font-mono tnum text-[var(--text-muted)]">{pct(d.confidence)}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      <p className="text-xs text-[var(--text-faint)]">
        As data gets messier, quality falls gradually and refusal rises with it. The no-label estimate falls too but stays optimistic at the noisiest level, so
        it should trigger a review, not replace a labelled pilot.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4" data-testid="unseen-cause">
        <Stat
          label={`Unseen cause: ${u.cause.replace("_", " ")}`}
          value={`${pct(u.refusal_rate_novel)} refused`}
          strong
          testid="unseen-refusal-value"
          note={`${u.n} wallets whose phone was lost or SIM swapped: activity just stops. Known causes in the same population: ${pct(u.refusal_rate_known)} refused.`}
        />
        <div className="md:col-span-2 p-4 rounded-[var(--radius)] bg-[var(--surface-2)] border border-[var(--border)] text-xs text-[var(--text-muted)] space-y-2">
          <div className="font-semibold text-[var(--text)]">Honest limit</div>
          <p>
            Refusal doubles on a cause the model has never seen, but the rest still get a confident label:{" "}
            {named.slice(0, 2).map(([c, s], i) => (
              <span key={c}>
                {i > 0 && ", "}
                <span className="text-[var(--text)]">{causeLabel(c)}</span> {pct(s, 0)}
              </span>
            ))}
            . A model can only refuse what looks ambiguous, not what looks familiar. In a pilot, the drift alarm and a jump in the estimated cause mix are the signals to add a new cause.
          </p>
          <p>Known causes in this population keep macro-F1 {pct(u.macro_f1_known)}.</p>
        </div>
      </div>
    </Section>
  );
}
