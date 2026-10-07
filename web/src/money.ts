import type { MoneyInputs } from "./seed";

// Same arithmetic as src/rules/money.py `money_table`; e2e/simulator.spec.ts checks it against the exported rows.
export type Outcome = { actioned: number; recovered: number; cost: number; value: number };

export function simulate(m: MoneyInputs, rate: number): Record<"rule" | "model" | "oracle", Outcome> {
  const k = m.arpu_bdt * m.ramp;
  const make = (actioned: number, recovered: number, unit: number): Outcome => ({
    actioned,
    recovered,
    cost: actioned * unit,
    value: recovered * k - actioned * unit,
  });
  return {
    rule: make(m.n_triaged, m.n_triaged * rate * m.generic_factor, m.msg_cost_bdt),
    model: make(
      m.n_triaged - m.n_refused,
      m.n_correct * rate + m.n_wrong * rate * m.generic_factor,
      m.avg_remedy_cost_bdt,
    ),
    oracle: make(m.n_triaged, m.n_triaged * rate, m.avg_remedy_cost_bdt),
  };
}

// Recovery rate above which the model nets more than the blanket message; null if it never does.
export function breakEven(m: MoneyInputs): number | null {
  const k = m.arpu_bdt * m.ramp;
  const gain = k * (m.n_correct + m.n_wrong * m.generic_factor - m.n_triaged * m.generic_factor);
  const extraCost = (m.n_triaged - m.n_refused) * m.avg_remedy_cost_bdt - m.n_triaged * m.msg_cost_bdt;
  return gain > 0 ? extraCost / gain : null;
}
