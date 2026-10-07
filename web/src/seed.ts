export type Cause =
  | "job_exit"
  | "migration"
  | "solved_problem"
  | "fee_shock"
  | "supply_failure";

export type SeedBundle = {
  meta: {
    generated_at: string; // ISO-8601
    seed: number; // RNG seed used for datagen + training
    model_version: string; // e.g. "lgbm-v1" or "sample"
    tau: number; // refusal: max posterior threshold
    delta: number; // refusal: top-2 margin threshold
    n_wallets_b_total: number; // size of full population B (metrics use all of it)
    honesty_line: string; // A1 sentence, verbatim
  };
  wallets: Wallet[]; // SAMPLE of population B for the UI (<= 400, stratified, includes refusals)
  report: Report;
  remedies: Record<Cause, Remedy>; // copied from src/rules/remedies.py at export time
};

export type Wallet = {
  wallet_id: string; // "W-" + 6 chars [0-9A-Z]
  worker_type: string; // e.g. "garment" | "domestic" | "transport" | "retail"
  pay_cycle: "weekly" | "biweekly" | "monthly";
  weeks_silent: number;
  series: { week: number; txn_count: number; amount_bdt: number }[]; // weekly, since acquisition
  verdict: "attributed" | "refused";
  cause: Cause | null; // null iff refused
  posterior: Record<Cause, number>; // sums to ~1
  contributions: { feature: string; value: number; contribution: number }[]; // top 8, |contribution| desc, toward predicted/top cause
  refusal_reasons: string[]; // [] iff attributed
  rule_baseline: { fired: boolean; action: "message_everyone" | "none" };
};

export type RefusalValidity = {
  refusal_rate_blended: number;
  refusal_rate_clean: number;
  enrichment_ratio: number;
  forced_error_refused: number;
  forced_error_attributed: number;
};

export type PopulationC = {
  macro_f1: number;
  refusal_rate: number;
  n_wallets: number;
};

export type PilotProtocol = {
  alpha: number;
  power: number;
  n_per_arm: number;
  n_arms: number;
  total_wallets: number;
  generic_factor: number;
  benchmark_rate: number;
};

export type CalibrationBin = {
  bin: number;
  mean_confidence: number;
  empirical_accuracy: number;
  n: number;
};

export type PerCauseMetric = {
  cause: Cause;
  precision: number;
  recall: number;
  f1: number;
  support: number;
};

export type Report = {
  ml: {
    macro_f1_a_test: number;
    macro_f1_b: number; // HEADLINE
    gap: number; // a_test - b
    refusal_rate_a: number;
    refusal_rate_b: number;
    ece_b: number; // expected calibration error on B
    shuffled_label_f1_b: number; // control, should be ~0.2
    best_single_feature: string;
    best_single_feature_f1_b: number;
    rule_baseline_f1_b: number;
    refusal_validity?: RefusalValidity;
    verdict_flip_rate?: number;
  };
  population_c?: PopulationC | null;
  pilot?: PilotProtocol | null;
  confusion_b: { labels: Cause[]; matrix: number[][] }; // rows = true, cols = predicted (attributed only)
  calibration_bins?: CalibrationBin[];
  per_cause_f1_b?: PerCauseMetric[];
  fairness: {
    slice: "worker_type" | "pay_cycle";
    group: string;
    n: number;
    macro_f1: number;
    refusal_rate: number;
  }[];
  money: MoneyRow[] | null; // null if src/rules.money not ready at export time
  break_even?: Record<Cause, number | null> | null;
  sweep?: MoneySweepRow[] | null;
  routing_plan?: Record<string, Record<Cause, "targeted" | "blanket" | "none">> | null;
  assumptions: string[]; // every ASSUMED input, one line each
};

export type MoneyRow = {
  recovery_rate: 0.01 | 0.04 | 0.08;
  strategy: "rule" | "model" | "oracle" | "routed";
  wallets_actioned: number;
  users_recovered: number;
  cost_bdt: number;
  value_bdt: number; // users_recovered * ARPU * ramp - cost
};

export type MoneySweepRow = MoneyRow & {
  cost_scale: number;
};

export type Remedy = {
  remedy_code: string;
  label: string;
  unit_cost_bdt: number;
  message_en: string;
  message_bn: string;
};

let cachedSeedPromise: Promise<SeedBundle> | null = null;
let sampleFallbackUsed = false;

export function isSampleFallbackUsed(): boolean {
  return sampleFallbackUsed;
}

export function loadSeed(): Promise<SeedBundle> {
  if (cachedSeedPromise) {
    return cachedSeedPromise;
  }

  cachedSeedPromise = (async () => {
    try {
      const res = await fetch("/seed.json");
      if (res.ok) {
        sampleFallbackUsed = false;
        return (await res.json()) as SeedBundle;
      }
    } catch {
      // Fall through to sample
    }

    const fallbackRes = await fetch("/seed.sample.json");
    if (!fallbackRes.ok) {
      throw new Error("Failed to load both /seed.json and /seed.sample.json");
    }
    sampleFallbackUsed = true;
    return (await fallbackRes.json()) as SeedBundle;
  })();

  return cachedSeedPromise;
}
