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
  };
  confusion_b: { labels: Cause[]; matrix: number[][] }; // rows = true, cols = predicted (attributed only)
  fairness: {
    slice: "worker_type" | "pay_cycle";
    group: string;
    n: number;
    macro_f1: number;
    refusal_rate: number;
  }[];
  money: MoneyRow[] | null; // null if src/rules.money not ready at export time
  money_inputs?: MoneyInputs | null; // counts + constants behind `money`; absent in older bundles
  refusal_sweep?: RefusalPoint[]; // every (tau, delta) the tuner searches, scored on population B; absent in older bundles
  assumptions: string[]; // every ASSUMED input, one line each
  depth?: Depth; // phase 2 evidence from scripts/depth.py (D62-D66); absent in seed.sample.json
};

export type MoneyRow = {
  recovery_rate: 0.01 | 0.04 | 0.08;
  strategy: "rule" | "model" | "model_ev" | "oracle";
  wallets_actioned: number;
  users_recovered: number;
  cost_bdt: number;
  value_bdt: number; // users_recovered * ARPU * ramp - cost
  actions?: Record<string, number>; // money_ev only: wallets per action ("none", "generic" or a cause's remedy)
};

type CoveragePoint = { coverage: number; macro_f1: number; accuracy: number };
type ReliabilityBin = { bin: number; confidence: number; accuracy: number; n: number };

export type Depth = {
  coverage: {
    lightgbm: CoveragePoint[];
    logreg: CoveragePoint[];
    aurc: { lightgbm: number; logreg: number };
    operating_point: { coverage: number; macro_f1: number };
  };
  baselines: { name: string; macro_f1_b: number; coverage: number }[];
  group_shift: { held_out: string; lightgbm: number; logreg: number }[];
  macro_f1_b_ci95: [number, number];
  per_class: { cause: Cause; f1_attributed: number; f1_all: number; refusal_rate: number }[];
  blended: { group: "clean" | "blended"; n: number; refusal_rate: number; accuracy_attributed: number }[];
  calibration: {
    ece_a_test: number;
    ece_b: number;
    temperature: number;
    ece_b_after_temperature: number;
    reliability_a: ReliabilityBin[];
    reliability_b: ReliabilityBin[];
    ece_by_group: { slice: string; group: string; ece: number }[];
  };
  label_free: {
    accuracy: { confidence: number; atc_estimate: number; true: number };
    accuracy_a_test: { atc_estimate: number; true: number };
    cause_mix: { cause: Cause; train: number; argmax: number; em: number; true: number }[];
    cause_mix_max_error: { train: number; argmax: number; em: number };
    drift: { domain_auc: number; psi: { feature: string; psi: number }[] };
  };
  stress: {
    noise_dial: {
      level: string;
      noise: number;
      blended: number;
      macro_f1: number;
      macro_f1_all: number;
      refusal_rate: number;
      accuracy_true: number;
      accuracy_atc: number;
      confidence: number;
    }[];
    unseen_cause: {
      cause: string;
      n: number;
      refusal_rate_novel: number;
      refusal_rate_known: number;
      named_as: Record<string, number>;
      macro_f1_known: number;
    };
  };
  ablation: { group: string; features: string[]; macro_f1_all: number; drop: number; most_hurt: Cause; most_hurt_drop: number }[];
  money_ev: MoneyRow[];
  assumptions: string[];
};

export type MoneyInputs = {
  n_triaged: number;
  n_correct: number;
  n_wrong: number;
  n_refused: number;
  arpu_bdt: number;
  ramp: number;
  generic_factor: number;
  msg_cost_bdt: number;
  avg_remedy_cost_bdt: number;
};

export type RefusalPoint = { tau: number; delta: number; refusal_rate: number; macro_f1: number };

export const CAUSE_LABELS: Record<Cause, string> = {
  job_exit: "Job Exit",
  migration: "Migration",
  solved_problem: "Solved Problem",
  fee_shock: "Fee Shock",
  supply_failure: "Supply Failure",
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
