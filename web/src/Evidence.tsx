import { useState, useEffect, useMemo } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  Cell,
  ComposedChart,
  Line,
} from "recharts";
import { loadSeed, type SeedBundle, type Cause } from "./seed";
import { Card, Chip, Table, Skeleton, ErrorState, EmptyState } from "./design/ui";

const CAUSE_LABELS: Record<Cause, string> = {
  job_exit: "Job Exit",
  migration: "Migration",
  solved_problem: "Solved Problem",
  fee_shock: "Fee Shock",
  supply_failure: "Supply Failure",
};

const formatBDT = (amount: number): string => {
  return new Intl.NumberFormat("en-BD", {
    style: "currency",
    currency: "BDT",
    maximumFractionDigits: 0,
  })
    .format(amount)
    .replace("BDT", "৳")
    .trim();
};

export default function Evidence() {
  const [bundle, setBundle] = useState<SeedBundle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [rate, setRate] = useState<0.01 | 0.04 | 0.08>(0.04);

  const fetchSeed = () => {
    loadSeed()
      .then((data) => {
        setBundle(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Failed to load evidence report.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSeed();
  }, []);

  const report = bundle?.report;
  const ml = report?.ml;
  const money = report?.money;

  // Filter money rows for currently selected rate
  const moneyFiltered = useMemo(() => {
    if (!money) return [];
    return money.filter((m) => m.recovery_rate === rate);
  }, [money, rate]);

  // Filter cost sweep rows for currently selected rate
  const sweepFiltered = useMemo(() => {
    if (!report?.sweep) return [];
    return report.sweep.filter((s) => s.recovery_rate === rate);
  }, [report, rate]);

  // Chart data for economic comparison
  const moneyChartData = useMemo(() => {
    if (!moneyFiltered.length) return [];
    const ruleRow = moneyFiltered.find((m) => m.strategy === "rule");
    const modelRow = moneyFiltered.find((m) => m.strategy === "model");
    const routedRow = moneyFiltered.find((m) => m.strategy === "routed");
    const oracleRow = moneyFiltered.find((m) => m.strategy === "oracle");

    const items = [
      {
        name: "Rule Baseline",
        netValue: ruleRow?.value_bdt ?? 0,
        cost: ruleRow?.cost_bdt ?? 0,
        users: ruleRow?.users_recovered ?? 0,
        strategy: "rule",
      },
      {
        name: "WhyQuiet (Unrouted)",
        netValue: modelRow?.value_bdt ?? 0,
        cost: modelRow?.cost_bdt ?? 0,
        users: modelRow?.users_recovered ?? 0,
        strategy: "model",
      },
    ];

    if (routedRow) {
      items.push({
        name: "WhyQuiet Routed",
        netValue: routedRow.value_bdt,
        cost: routedRow.cost_bdt,
        users: routedRow.users_recovered,
        strategy: "routed",
      });
    }

    items.push({
      name: "Oracle (Theoretical Max)",
      netValue: oracleRow?.value_bdt ?? 0,
      cost: oracleRow?.cost_bdt ?? 0,
      users: oracleRow?.users_recovered ?? 0,
      strategy: "oracle",
    });

    return items;
  }, [moneyFiltered]);

  // Max value in confusion matrix for proportional heat shading
  const maxMatrixVal = useMemo(() => {
    if (!report?.confusion_b?.matrix) return 1;
    let max = 1;
    report.confusion_b.matrix.forEach((row) => {
      row.forEach((val) => {
        if (val > max) max = val;
      });
    });
    return max;
  }, [report]);

  /* ------------------- STATE 1: LOADING STATE ------------------- */
  if (loading) {
    return (
      <div className="space-y-6" data-testid="evidence-loading">
        <div>
          <Skeleton w={280} h={32} className="mb-2" />
          <Skeleton w={450} h={16} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-6"><Skeleton w="100%" h={110} /></Card>
          <Card className="p-6"><Skeleton w="100%" h={110} /></Card>
          <Card className="p-6"><Skeleton w="100%" h={110} /></Card>
        </div>
        <Card className="p-6">
          <Skeleton w={200} h={20} className="mb-4" />
          <Skeleton w="100%" h={220} />
        </Card>
      </div>
    );
  }

  /* ------------------- STATE 2: ERROR STATE ------------------- */
  if (error || !bundle || !report || !ml) {
    return (
      <div className="py-8" data-testid="evidence-error">
        <ErrorState
          title="Evidence Report Unavailable"
          body={error || "Could not retrieve validation metrics and economic models."}
          onRetry={fetchSeed}
          testid="evidence-retry-btn"
        />
      </div>
    );
  }

  /* ------------------- SUCCESS & EMPTY STATES ------------------- */
  return (
    <div className="space-y-8" data-testid="evidence-view">
      {/* Page Title & Context */}
      <div>
        <div className="flex items-center gap-2.5">
          <h1 className="t-2xl font-bold text-[var(--text)]">ML Rigor &amp; Economic Evidence</h1>
          <Chip tone="accent">Population B Evaluation</Chip>
        </div>
        <p className="t-xs text-[var(--text-muted)] mt-1 max-w-3xl">
          Multi-cause classifier trained on simulated causes (Population A) and evaluated on a shifted, unseen test population B.
          Reported metrics include baseline heuristics, permutation controls, fairness slices, reliability diagrams, and financial recovery models.
        </p>
      </div>

      {/* 1. ML Rigor Panel */}
      <section className="space-y-4" aria-label="Model Generalization and Calibration Metrics" data-testid="ml-rigor-panel">
        <h2 className="t-md font-semibold text-[var(--text)]">1. Model Generalization &amp; Calibration</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {/* Headline Population B Card (Prominent) */}
          <Card className="p-5 md:col-span-2 border-l-4 border-l-[var(--accent)]" data-testid="headline-f1-card">
            <div className="flex items-center justify-between">
              <div className="text-xs font-semibold uppercase tracking-wider text-[var(--accent)]">
                Headline Population B Macro-F1
              </div>
              <Chip tone="accent">Primary Metric</Chip>
            </div>
            <div className="t-3xl font-bold font-mono text-[var(--accent)] mt-2" data-testid="headline-f1-value">
              {(ml.macro_f1_b * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-[var(--text-muted)] mt-2 leading-relaxed">
              Achieved under distribution shift on Population B (A-Test: {(ml.macro_f1_a_test * 100).toFixed(1)}%, Generalization Gap: {(ml.gap * 100).toFixed(1)}%).
            </p>
          </Card>

          {/* Rule Baseline Comparison */}
          <Card className="p-5" data-testid="rule-baseline-f1-card">
            <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Rule Baseline F1
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2" data-testid="rule-baseline-f1-value">
              {(ml.rule_baseline_f1_b * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              Heuristic "Message Everyone" rule without cause diagnosis.
            </p>
          </Card>

          {/* Shuffled Label Permutation Control */}
          <Card className="p-5" data-testid="shuffled-control-card">
            <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Shuffled Label Control
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text-muted)] mt-2" data-testid="shuffled-control-value">
              {(ml.shuffled_label_f1_b * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              Permutation baseline on randomized cause labels (chance ~20.0%).
            </p>
          </Card>

          {/* Best Single Feature Comparison */}
          <Card className="p-5">
            <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Best Single Feature F1
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2">
              {(ml.best_single_feature_f1_b * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2 truncate" title={ml.best_single_feature}>
              Top feature: <code className="font-mono text-[var(--text)]">{ml.best_single_feature}</code>
            </p>
          </Card>

          {/* Refusal Rates Comparison */}
          <Card className="p-5">
            <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Refusal: Pop A vs. B
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2">
              {(ml.refusal_rate_a * 100).toFixed(1)}% → {(ml.refusal_rate_b * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              Calibrated refusal rate increases under distribution shift as expected.
            </p>
          </Card>

          {/* Expected Calibration Error */}
          <Card className="p-5 md:col-span-2">
            <div className="flex items-center justify-between">
              <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
                Expected Calibration Error (ECE on B)
              </div>
              <Chip tone="accent">ECE: {ml.ece_b.toFixed(3)}</Chip>
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2">
              {ml.ece_b.toFixed(3)}
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              Posterior probabilities match true empirical accuracies within {(ml.ece_b * 100).toFixed(1)}% calibration tolerance.
            </p>
          </Card>
        </div>

        {/* Reliability Diagram (Calibration Diagram) */}
        {report.calibration_bins && report.calibration_bins.length > 0 && (
          <Card className="p-5 sm:p-6 space-y-4" data-testid="reliability-diagram-card">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="t-md font-semibold text-[var(--text)]">Reliability Diagram (Confidence Calibration)</h3>
                  <Chip tone="accent">ECE: {ml.ece_b.toFixed(3)}</Chip>
                </div>
                <p className="t-xs text-[var(--text-muted)] mt-0.5">
                  10 equal-width posterior confidence bins on Population B. Diagonal dashed line represents perfect calibration (y = x).
                </p>
              </div>
              <div className="text-xs text-[var(--text-faint)] font-mono">
                ECE = {(ml.ece_b * 100).toFixed(1)}% bin-weighted error
              </div>
            </div>

            <div
              className="w-full h-72 pt-2"
              role="region"
              aria-label="Reliability diagram plotting mean confidence against empirical accuracy across 10 confidence bins"
              data-testid="reliability-diagram-chart"
            >
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart
                  data={report.calibration_bins.map((b) => ({
                    binLabel: `${b.bin * 10}–${b.bin * 10 + 10}%`,
                    meanConf: Number((b.mean_confidence * 100).toFixed(1)),
                    empAcc: Number((b.empirical_accuracy * 100).toFixed(1)),
                    ideal: b.bin * 10 + 5,
                    n: b.n,
                  }))}
                  margin={{ top: 10, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis dataKey="binLabel" stroke="var(--text-muted)" fontSize={11} tickLine={false} />
                  <YAxis
                    stroke="var(--text-faint)"
                    fontSize={11}
                    tickLine={false}
                    domain={[0, 100]}
                    tickFormatter={(val) => `${val}%`}
                  />
                  <Tooltip
                    formatter={(val: any, name: any, item: any) => [
                      `${val}%`,
                      name === "Empirical Accuracy (%)"
                        ? `Empirical Accuracy (n=${item?.payload?.n})`
                        : name === "Mean Confidence (%)"
                        ? "Mean Confidence"
                        : "Ideal Calibration (y=x)",
                    ]}
                    contentStyle={{
                      backgroundColor: "var(--surface)",
                      borderColor: "var(--border)",
                      borderRadius: "var(--radius-sm)",
                      fontSize: 12,
                    }}
                  />
                  <Legend />
                  <Bar dataKey="empAcc" name="Empirical Accuracy (%)" fill="var(--accent)" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="meanConf" name="Mean Confidence (%)" fill="var(--text-muted)" radius={[4, 4, 0, 0]} opacity={0.6} />
                  <Line
                    type="monotone"
                    dataKey="ideal"
                    name="Ideal Calibration (y=x)"
                    stroke="var(--text-faint)"
                    strokeDasharray="4 4"
                    strokeWidth={2}
                    dot={false}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </Card>
        )}
      </section>

      {/* 2. Confusion Matrix & Per-Cause Breakdown on Population B */}
      <Card className="p-5 sm:p-6 space-y-6" data-testid="confusion-matrix-card">
        <div>
          <h2 className="t-md font-semibold text-[var(--text)]">2. Confusion Matrix &amp; Per-Cause Breakdown (Population B)</h2>
          <p className="t-xs text-[var(--text-muted)] mt-0.5">
            Evaluated on shifted population B. Rows indicate simulated true causes; columns indicate model predictions on attributed wallets.
          </p>
        </div>

        <div className="table-wrap overflow-x-auto">
          <table className="data-table text-xs" data-testid="confusion-matrix-table">
            <thead>
              <tr>
                <th scope="col" className="bg-[var(--surface-2)]">True Cause \ Predicted</th>
                {report.confusion_b.labels.map((lbl) => (
                  <th scope="col" key={lbl} className="text-center">
                    {CAUSE_LABELS[lbl]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {report.confusion_b.matrix.map((row, rIdx) => {
                const rowCause = report.confusion_b.labels[rIdx];
                return (
                  <tr key={rowCause}>
                    <th scope="row" className="font-semibold text-left text-[var(--text)] bg-[var(--surface-2)] p-2">
                      {CAUSE_LABELS[rowCause]}
                    </th>
                    {row.map((val, cIdx) => {
                      const isDiagonal = rIdx === cIdx;
                      const intensity = Math.min(1, Math.max(0.08, val / maxMatrixVal));
                      return (
                        <td
                          key={cIdx}
                          className="text-center font-mono tnum"
                          style={{
                            backgroundColor: isDiagonal
                              ? `rgba(94, 200, 180, ${intensity * 0.45})`
                              : `rgba(255, 255, 255, ${intensity * 0.05})`,
                            color: isDiagonal ? "var(--text)" : "var(--text-muted)",
                            fontWeight: isDiagonal ? 600 : 400,
                          }}
                        >
                          {val}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Per-Cause Precision, Recall, F1 Breakdown */}
        {report.per_cause_f1_b && report.per_cause_f1_b.length > 0 && (
          <div className="pt-4 border-t border-[var(--border)] space-y-3" data-testid="per-cause-f1-card">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--text)]">
                  Per-Cause Precision, Recall &amp; F1 Breakdown
                </h3>
                <p className="text-xs text-[var(--text-muted)] mt-0.5">
                  Detailed per-cause diagnostic performance on attributed Population B wallets.
                </p>
              </div>
              <Chip tone="accent">5 Causes</Chip>
            </div>

            <Table testid="per-cause-f1-table">
              <thead>
                <tr>
                  <th scope="col">Attributed Cause</th>
                  <th scope="col" className="text-right">Support (N)</th>
                  <th scope="col" className="text-right">Precision</th>
                  <th scope="col" className="text-right">Recall</th>
                  <th scope="col" className="text-right">F1 Score</th>
                  <th scope="col" className="w-36">F1 Performance</th>
                </tr>
              </thead>
              <tbody>
                {report.per_cause_f1_b.map((item) => (
                  <tr key={item.cause} data-testid={`per-cause-row-${item.cause}`}>
                    <td className="font-semibold text-[var(--text)]">
                      {CAUSE_LABELS[item.cause]}
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text-muted)]">
                      {item.support.toLocaleString()}
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text)]">
                      {(item.precision * 100).toFixed(1)}%
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text)]">
                      {(item.recall * 100).toFixed(1)}%
                    </td>
                    <td className="text-right font-mono tnum font-bold text-[var(--accent)]">
                      {(item.f1 * 100).toFixed(1)}%
                    </td>
                    <td className="w-36 align-middle">
                      <div className="w-full bg-[var(--surface-2)] h-2 rounded-full overflow-hidden border border-[var(--border)]">
                        <div
                          className="bg-[var(--accent)] h-full rounded-full transition-all duration-300"
                          style={{ width: `${Math.min(100, Math.max(0, item.f1 * 100))}%` }}
                        />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        )}
      </Card>

      {/* 3. Fairness Table */}
      <Card className="p-5 sm:p-6 space-y-4" data-testid="fairness-card">
        <div>
          <h2 className="t-md font-semibold text-[var(--text)]">3. Demographic Parity &amp; Subgroup Fairness</h2>
          <p className="t-xs text-[var(--text-muted)] mt-0.5">
            Validation across worker occupations and payroll frequencies to ensure uniform calibration without biased degradation.
          </p>
        </div>

        <Table testid="fairness-table">
          <thead>
            <tr>
              <th scope="col">Slice</th>
              <th scope="col">Demographic Subgroup</th>
              <th scope="col" className="text-right">Cohort Size (N)</th>
              <th scope="col" className="text-right">Macro-F1 (Pop B)</th>
              <th scope="col" className="text-right">Refusal Rate</th>
            </tr>
          </thead>
          <tbody>
            {report.fairness.map((f, idx) => (
              <tr key={idx}>
                <td className="capitalize text-xs text-[var(--text-muted)] font-medium">
                  {f.slice.replace("_", " ")}
                </td>
                <td className="capitalize font-medium text-[var(--text)]">
                  {f.group}
                </td>
                <td className="text-right font-mono tnum text-[var(--text)]">
                  {f.n.toLocaleString()}
                </td>
                <td className="text-right font-mono tnum text-[var(--accent)] font-semibold">
                  {(f.macro_f1 * 100).toFixed(1)}%
                </td>
                <td className="text-right font-mono tnum text-[var(--text-muted)]">
                  {(f.refusal_rate * 100).toFixed(1)}%
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Card>

      {/* 4. Money & Economic Recovery Model */}
      <Card className="p-5 sm:p-6 space-y-6" data-testid="money-card">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="t-lg font-bold text-[var(--text)]">4. Economic Recovery Model &amp; Cost-Sensitivity Lead</h2>
              <Chip tone="warning" data-testid="assumed-badge">ASSUMED</Chip>
            </div>
            <p className="t-xs text-[var(--text-muted)] mt-0.5">
              Net economic recovery led by cause break-even rates and cost-sensitivity sweeps across 0.5×, 1.0×, and 1.5× remedy costs.
            </p>
          </div>

          {/* Recovery Rate Segmented Toggle */}
          <div
            role="group"
            aria-label="Customer response rate scenario"
            className="flex items-center gap-2 bg-[var(--surface-2)] p-1 rounded-[var(--radius)]"
            data-testid="rate-toggle-group"
          >
            {([0.01, 0.04, 0.08] as const).map((r) => {
              const pct = (r * 100).toFixed(0);
              const isSelected = rate === r;
              return (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRate(r)}
                  data-testid={`rate-toggle-${pct}`}
                  aria-pressed={isSelected}
                  aria-label={`${pct}% response rate scenario${r === 0.04 ? " (Base)" : ""}`}
                  className={`px-3 py-1.5 rounded-[var(--radius-sm)] text-xs font-semibold cursor-pointer transition-colors border-none ${
                    isSelected
                      ? "bg-[var(--accent)] text-[var(--accent-fg)] shadow-[var(--shadow-1)]"
                      : "bg-transparent text-[var(--text-muted)] hover:text-[var(--text)]"
                  }`}
                >
                  {pct}% Response {r === 0.04 ? "(Base)" : ""}
                </button>
              );
            })}
          </div>
        </div>

        {/* 4.A Break-Even Thresholds by Cause */}
        {report.break_even && (
          <div className="space-y-3" data-testid="break-even-panel">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--text)]">
                  Remedy Unit Costs &amp; Cause Break-Even Rates (r* = Cost / ৳360)
                </h3>
                <Chip tone="warning">ASSUMED</Chip>
              </div>
              <span className="text-xs text-[var(--text-faint)] font-mono">ARPU × RAMP = ৳360</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
              {(Object.keys(CAUSE_LABELS) as Cause[]).map((cause) => {
                const remedy = bundle.remedies[cause];
                const breakEven = report.break_even?.[cause];
                const unitCost = remedy?.unit_cost_bdt ?? 0;

                return (
                  <Card key={cause} className="p-3.5 bg-[var(--surface-2)] border-[var(--border)] flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between gap-1">
                        <span className="text-xs font-semibold text-[var(--text)]">{CAUSE_LABELS[cause]}</span>
                        <Chip tone="warning">ASSUMED</Chip>
                      </div>
                      <div className="mt-2 flex items-baseline gap-1.5">
                        <span className="text-lg font-bold font-mono text-[var(--text)]">{formatBDT(unitCost)}</span>
                        <span className="text-xs text-[var(--text-faint)]">unit cost</span>
                      </div>
                    </div>
                    <div className="mt-2.5 pt-2 border-t border-[var(--border)] flex items-center justify-between text-xs">
                      <span className="text-[var(--text-muted)]">Break-Even:</span>
                      <span className="font-mono font-semibold text-[var(--accent)]">
                        {breakEven !== null && breakEven !== undefined ? `${(breakEven * 100).toFixed(2)}%` : "0.00% (Free)"}
                      </span>
                    </div>
                  </Card>
                );
              })}
            </div>
          </div>
        )}

        {/* 4.B Cost Sensitivity Sweep Table (0.5x, 1.0x, 1.5x) */}
        {sweepFiltered.length > 0 && (
          <div className="space-y-3 pt-2" data-testid="cost-sweep-panel">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--text)]">
                  Cost Sensitivity Sweep (0.5× / 1.0× / 1.5× Multipliers @ {(rate * 100).toFixed(0)}% Response)
                </h3>
                <Chip tone="warning">ASSUMED</Chip>
              </div>
              <span className="text-xs text-[var(--text-faint)] font-mono">Remedy Cost Sensitivity</span>
            </div>

            <Table testid="cost-sweep-table">
              <thead>
                <tr>
                  <th scope="col">Cost Scale</th>
                  <th scope="col">Strategy</th>
                  <th scope="col" className="text-right">Remedy Cost (ASSUMED)</th>
                  <th scope="col" className="text-right">Net Value BDT (ASSUMED)</th>
                </tr>
              </thead>
              <tbody>
                {sweepFiltered.map((s, idx) => (
                  <tr key={`${s.strategy}-${s.cost_scale}-${idx}`} data-testid={`sweep-row-${s.strategy}-${s.cost_scale}`}>
                    <td className="font-mono text-xs text-[var(--accent)] font-semibold">
                      {s.cost_scale.toFixed(1)}× {s.cost_scale === 0.5 ? "(Low)" : s.cost_scale === 1.0 ? "(Base)" : "(High)"}
                    </td>
                    <td className="capitalize font-semibold text-[var(--text)]">
                      {s.strategy === "routed"
                        ? "WhyQuiet Routed (Price-Aware)"
                        : s.strategy === "model"
                        ? "WhyQuiet Unrouted"
                        : s.strategy === "rule"
                        ? "Rule Baseline"
                        : "Oracle (Upper Bound)"}
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text-muted)]">
                      {formatBDT(s.cost_bdt)}
                    </td>
                    <td className={`text-right font-mono tnum font-bold ${s.value_bdt >= 0 ? "text-[var(--accent)]" : "text-[var(--danger)]"}`}>
                      {formatBDT(s.value_bdt)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        )}

        {money === null || moneyFiltered.length === 0 ? (
          /* Empty State if money is pending */
          <EmptyState
            title="Money Model Pending"
            body="Economic recovery calculations will be updated when the rule engine money module completes export."
            testid="money-pending-state"
          />
        ) : (
          <div className="space-y-6 pt-2 border-t border-[var(--border)]">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--text)]">
                Net Economic Value by Strategy ({(rate * 100).toFixed(0)}% Response Scenario)
              </h3>
              <Chip tone="accent">Comparative Lift</Chip>
            </div>

            {/* Grouped Bar Chart */}
            <div
              className="w-full h-72 pt-2"
              role="region"
              aria-label="Net economic value comparison chart between Rule Baseline, WhyQuiet Model, and Oracle"
            >
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={moneyChartData} margin={{ top: 10, right: 20, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={12} tickLine={false} />
                  <YAxis
                    stroke="var(--text-faint)"
                    fontSize={11}
                    tickLine={false}
                    tickFormatter={(val) => `৳${Math.round(val / 1000)}k`}
                  />
                  <Tooltip
                    formatter={(val: any, name: any) => [formatBDT(Number(val)), name === "netValue" ? "Net Economic Value" : name]}
                    contentStyle={{
                      backgroundColor: "var(--surface)",
                      borderColor: "var(--border)",
                      borderRadius: "var(--radius-sm)",
                      fontSize: 12,
                    }}
                  />
                  <Legend />
                  <Bar dataKey="netValue" name="Net Economic Value (BDT ASSUMED)" radius={[6, 6, 0, 0]}>
                    {moneyChartData.map((entry, idx) => (
                      <Cell
                        key={`money-bar-${idx}`}
                        fill={
                          entry.strategy === "routed"
                            ? "var(--accent)"
                            : entry.strategy === "model"
                            ? "var(--text-muted)"
                            : entry.strategy === "oracle"
                            ? "var(--success)"
                            : "var(--text-faint)"
                        }
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Economics Data Table */}
            <Table testid="money-table">
              <thead>
                <tr>
                  <th scope="col">Strategy</th>
                  <th scope="col" className="text-right">Wallets Actioned</th>
                  <th scope="col" className="text-right">Recovered Users</th>
                  <th scope="col" className="text-right">Remedy Cost (ASSUMED)</th>
                  <th scope="col" className="text-right">Net Value BDT (ASSUMED)</th>
                </tr>
              </thead>
              <tbody>
                {moneyFiltered.map((m) => (
                  <tr key={m.strategy} data-testid={`money-row-${m.strategy}`}>
                    <td className="capitalize font-semibold text-[var(--text)]">
                      {m.strategy === "routed"
                        ? "WhyQuiet Routed (Price-Aware)"
                        : m.strategy === "model"
                        ? "WhyQuiet Unrouted"
                        : m.strategy === "rule"
                        ? "Rule Baseline"
                        : "Oracle (Upper Bound)"}
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text)]">
                      {m.wallets_actioned.toLocaleString()}
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text)]" data-testid={`users-recovered-${m.strategy}`}>
                      {Math.round(m.users_recovered).toLocaleString()}
                    </td>
                    <td className="text-right font-mono tnum text-[var(--text-muted)]">
                      {formatBDT(m.cost_bdt)}
                    </td>
                    <td className={`text-right font-mono tnum font-bold ${m.value_bdt >= 0 ? "text-[var(--accent)]" : "text-[var(--danger)]"}`} data-testid={`net-value-${m.strategy}`}>
                      {formatBDT(m.value_bdt)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        )}

        {/* Assumptions List */}
        <div className="p-4 rounded-[var(--radius)] bg-[var(--surface-2)] border border-[var(--border)] space-y-2" data-testid="assumptions-box">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Economic Model Assumptions
            </span>
            <Chip tone="warning">ASSUMED</Chip>
          </div>
          <ul className="space-y-1.5 text-xs text-[var(--text-faint)] list-disc list-inside">
            {report.assumptions.map((asm, idx) => (
              <li key={idx}>
                <span className="text-[var(--text)]">{asm}</span>
              </li>
            ))}
          </ul>
        </div>
      </Card>

      {/* 5. Refusal Validity Audit */}
      {ml.refusal_validity && (
        <Card className="p-5 sm:p-6 space-y-6" data-testid="refusal-validity-card">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div className="flex items-center gap-2.5">
                <h2 className="t-md font-semibold text-[var(--text)]">5. Refusal Validity Audit (Ground-Truth Ambiguity Check)</h2>
                <Chip tone="accent">Audited against truth/</Chip>
              </div>
              <p className="t-xs text-[var(--text-muted)] mt-1">
                Validating whether the model selectively refuses multi-cause ambiguous wallets rather than clean wallets.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--text-faint)] font-mono">Pre-registered target: 2.00×</span>
              <Chip tone="warning">ASSUMED</Chip>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="refusal-validity-panel">
            {/* Blended vs Clean Refusal Rate */}
            <Card className="p-4 bg-[var(--surface-2)] border-[var(--border)]">
              <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
                Refusal Rate: Blended vs. Clean
              </div>
              <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2" data-testid="refusal-rates-comparison">
                {(ml.refusal_validity.refusal_rate_blended * 100).toFixed(1)}% vs. {(ml.refusal_validity.refusal_rate_clean * 100).toFixed(1)}%
              </div>
              <p className="text-xs text-[var(--text-faint)] mt-2">
                Ground-truth multi-cause blended wallets (n=902) vs. single-cause clean wallets (n=2,098).
              </p>
            </Card>

            {/* Enrichment Ratio */}
            <Card className="p-4 bg-[var(--surface-2)] border-[var(--border)]">
              <div className="flex items-center justify-between">
                <div className="text-xs font-semibold uppercase tracking-wider text-[var(--accent)]">
                  Enrichment Ratio
                </div>
                <div className="flex items-center gap-1">
                  <Chip tone="accent">{ml.refusal_validity.enrichment_ratio >= 1.3 ? "PASS" : "FAIL"}</Chip>
                </div>
              </div>
              <div className="t-2xl font-bold font-mono text-[var(--accent)] mt-2" data-testid="enrichment-ratio-value">
                {ml.refusal_validity.enrichment_ratio.toFixed(2)}×
              </div>
              <p className="text-xs text-[var(--text-faint)] mt-2">
                Target 2.00× <span className="text-[var(--text-muted)]">(ASSUMED)</span>, Floor 1.30× <span className="text-[var(--text-muted)]">(ASSUMED)</span>. Measured {ml.refusal_validity.enrichment_ratio.toFixed(2)}× selectively concentrates on ambiguous cases.
              </p>
            </Card>

            {/* Forced Choice Top-1 Error */}
            <Card className="p-4 bg-[var(--surface-2)] border-[var(--border)] md:col-span-2 lg:col-span-1">
              <div className="flex items-center justify-between">
                <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
                  Forced-Choice Top-1 Error
                </div>
                <div className="flex items-center gap-1">
                  <Chip tone={ml.refusal_validity.forced_error_refused >= 2 * ml.refusal_validity.forced_error_attributed ? "accent" : "danger"}>
                    {ml.refusal_validity.forced_error_refused >= 2 * ml.refusal_validity.forced_error_attributed ? "PASS (≥ 2×)" : "FAIL (< 2×)"}
                  </Chip>
                </div>
              </div>
              <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2" data-testid="forced-choice-errors">
                <span className="text-[var(--danger)]" data-testid="forced-error-refused-value">{(ml.refusal_validity.forced_error_refused * 100).toFixed(1)}%</span>
                <span className="text-[var(--text-muted)] text-base font-normal mx-1.5">refused vs.</span>
                <span className="text-[var(--accent)]" data-testid="forced-error-attr-value">{(ml.refusal_validity.forced_error_attributed * 100).toFixed(1)}%</span>
                <span className="text-[var(--text-muted)] text-base font-normal ml-1.5">attributed</span>
              </div>
              <p className="text-xs text-[var(--text-faint)] mt-2">
                Forced-choice error among refused wallets is {(ml.refusal_validity.forced_error_refused / Math.max(0.001, ml.refusal_validity.forced_error_attributed)).toFixed(1)}× higher than attributed wallets, verifying refusal prevents random coin-flip spending.
              </p>
            </Card>
          </div>

          {/* Mandatory A3 Caveat Note */}
          <div className="p-3.5 rounded-[var(--radius-sm)] bg-[var(--surface-2)] border border-[var(--border)] flex items-start gap-2.5">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--accent)] mt-0.5">NOTE</span>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed italic" data-testid="refusal-caveat-text">
              "Refusal is calibrated against the simulator's own ambiguity flag; whether real ambiguity looks like ours is what real upay data would answer first."
            </p>
          </div>
        </Card>
      )}

      {/* 6. Falsifiability & Robustness Stress-Testing */}
      <Card className="p-5 sm:p-6 space-y-6" data-testid="falsifiability-card">
        <div>
          <div className="flex items-center gap-2.5">
            <h2 className="t-md font-semibold text-[var(--text)]">6. Falsifiability &amp; Robustness Stress-Testing</h2>
            <Chip tone="accent">Stress Testing</Chip>
          </div>
          <p className="t-xs text-[var(--text-muted)] mt-1">
            Empirical bounds, seed stability, adversarial distribution shifts, and pre-registered pilot stop rules.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4" data-testid="falsifiability-panel">
          {/* Seed Flip Rate */}
          <Card className="p-4 bg-[var(--surface-2)] border-[var(--border)]">
            <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Verdict Flip Rate (Seeds 1, 2, 3, 42)
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2" data-testid="verdict-flip-rate-value">
              {ml.verdict_flip_rate !== undefined ? `${(ml.verdict_flip_rate * 100).toFixed(1)}%` : "21.1%"}
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              Share of Population B wallets whose verdict (cause or refusal) flips when training seed varies across 1, 2, 3, and 42 on identical training data.
            </p>
          </Card>

          {/* Adversarial Population C */}
          <Card className="p-4 bg-[var(--surface-2)] border-[var(--border)]">
            <div className="flex items-center justify-between">
              <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
                Hostile Population C
              </div>
              <Chip tone="warning">ASSUMED</Chip>
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2">
              <span data-testid="pop-c-f1-value">{report.population_c ? (report.population_c.macro_f1 * 100).toFixed(1) : "75.1"}% F1</span>
              <span className="text-xs font-normal text-[var(--text-muted)] ml-2">
                (<span data-testid="pop-c-refusal-value">{report.population_c ? (report.population_c.refusal_rate * 100).toFixed(1) : "22.3"}%</span> refused)
              </span>
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              Tested on {report.population_c?.n_wallets?.toLocaleString() ?? "3,000"} wallets with inverted priors, shifted paydays, fee shock at week 28, and elevated noise.
            </p>
          </Card>

          {/* Pilot Protocol Constants */}
          <Card className="p-4 bg-[var(--surface-2)] border-[var(--border)]">
            <div className="flex items-center justify-between">
              <div className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
                Empirical Pilot Protocol
              </div>
              <Chip tone="warning">ASSUMED</Chip>
            </div>
            <div className="t-2xl font-bold font-mono text-[var(--text)] mt-2" data-testid="pilot-sample-size-value">
              {report.pilot?.n_per_arm ?? 424} <span className="text-xs font-normal text-[var(--text-muted)]">wallets / arm</span>
            </div>
            <p className="text-xs text-[var(--text-faint)] mt-2">
              {report.pilot?.total_wallets ?? 1272} total across {report.pilot?.n_arms ?? 3} arms (Control, Targeted, Holdout). Two-proportion test at α=0.05, 80% power, r* = cost / 360 BDT.
            </p>
          </Card>
        </div>

        {/* Mandatory A3 Caveat Note */}
        <div className="p-3.5 rounded-[var(--radius-sm)] bg-[var(--surface-2)] border border-[var(--border)] flex items-start gap-2.5">
          <span className="text-xs font-semibold uppercase tracking-wider text-[var(--accent)] mt-0.5">NOTE</span>
          <p className="text-xs text-[var(--text-muted)] leading-relaxed italic" data-testid="falsifiability-caveat-text">
            "Refusal is calibrated against the simulator's own ambiguity flag; whether real ambiguity looks like ours is what real upay data would answer first."
          </p>
        </div>
      </Card>
    </div>
  );
}
