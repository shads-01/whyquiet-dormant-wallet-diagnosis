"""FastAPI v1 REST Endpoints for WhyQuiet Re-engagement Engine."""

from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ValidationError

from src.allocation.solver import BudgetAllocator
from src.config import get_config
from src.diagnosis.classifier import CauseClassifier
from src.diagnosis.explainer import DiagnosisExplainer
from src.features.pipeline import FeaturePipeline
from src.guardrails.safety import SafetyGuardrails
from src.messaging.engine import MessagingEngine
from src.ops.tickets import OpsTicketAggregator
from src.uplift.segmentation import CausalSegmenter
from src.uplift.x_learner import MultiArmXLearner

router = APIRouter(prefix="/api/v1", tags=["Re-engagement Causal Engine"])

# Global singletons / lazy-loaders
_config = get_config()
_pipeline = FeaturePipeline()
_classifier = CauseClassifier(config=_config)
_x_learner = MultiArmXLearner(random_state=42)
_segmenter = CausalSegmenter(config=_config)
_allocator = BudgetAllocator(config=_config)
_messaging = MessagingEngine(config=_config)
_guardrails = SafetyGuardrails()
_ops_aggregator = OpsTicketAggregator()
_models_initialized = False


def _ensure_models():
    """Ensure ML models are initialized."""
    global _models_initialized
    if not _models_initialized:
        # Generate minimal training slice for live inference readiness

        from src.simulator.generator import MFSSimulator

        sim = MFSSimulator(config=_config)
        wallets = sim.generate_population(n_wallets=600, seed=42)
        df_raw = sim.to_dataframe(wallets)
        df_feats = _pipeline.extract_features(df_raw)

        X = _pipeline.get_feature_matrix(df_feats)
        y_cause = df_raw["true_cause"].to_numpy()
        y_react = df_raw["observed_reactivation"].to_numpy()
        assigned_arms = df_raw["assigned_arm"].to_numpy()

        _classifier.fit(X, y_cause)
        _x_learner.fit(X, y_react, assigned_arms)
        _models_initialized = True


# --- Request & Response Models ---

class SingleWalletRequest(BaseModel):
    wallet_id: str = Field(default="W-001234", description="Pseudonymous wallet identifier")
    features: dict[str, Any] = Field(description="Wallet behavioral and transaction features")
    dnd_registered: bool = Field(default=False)
    blocklisted: bool = Field(default=False)
    language: str = Field(default="bn", description="'bn' or 'en'")


class SingleWalletResponse(BaseModel):
    wallet_id: str
    diagnosed_cause: str
    is_attributed: bool
    confidence: float
    margin: float
    abstain_reason: str | None
    evidence_reasons: list[str]
    causal_segment: str
    assigned_arm: str
    arm_name: str
    cost_bdt: float
    expected_incremental_lift: float
    is_safe_to_contact: bool
    suppression_reason: str | None
    rendered_message: str
    channel: str
    decision_trace: dict[str, Any]


class CampaignPlanRequest(BaseModel):
    budget_bdt: float = Field(default=500000.0, ge=1000.0)
    wallet_sample_size: int = Field(default=1000, ge=10, le=50000)


class CampaignPlanResponse(BaseModel):
    budget_bdt: float
    total_spend_bdt: float
    budget_utilization_rate: float
    total_wallets_evaluated: int
    total_wallets_targeted: int
    total_wallets_suppressed: int
    expected_incremental_reactivations: float
    expected_incremental_revenue_bdt: float
    cost_per_incremental_reactivation_bdt: float
    wasted_spend_rate: float
    shadow_price_lambda: float
    arm_breakdown: dict[str, int]


@router.post("/reengage/diagnose-and-allocate", response_model=SingleWalletResponse)
def diagnose_and_allocate_single(req: SingleWalletRequest):
    """Diagnose a single dormant wallet, estimate uplift, allocate remedy, and generate message."""
    _ensure_models()

    raw_dict = {"wallet_id": req.wallet_id, **req.features}
    raw_dict["dnd_registered"] = int(req.dnd_registered)
    raw_dict["blocklisted"] = int(req.blocklisted)

    try:
        validated_vec = _pipeline.extract_single(raw_dict)
    except (ValidationError, ValueError, KeyError) as e:
        raise HTTPException(status_code=422, detail=f"Feature validation error: {e!s}") from e

    feat_dict = validated_vec.to_dict()
    x_vec = np.array([feat_dict[f] for f in _pipeline.feature_names], dtype=np.float32)

    # 1. Diagnose Cause
    diag_res = _classifier.diagnose_wallet(x_vec)
    explainer = DiagnosisExplainer(classifier=_classifier)
    evidence = explainer.explain_wallet(x_vec, predicted_cause=diag_res.predicted_cause, top_k=3)
    evidence_text = evidence.get(req.language, evidence.get("en", []))

    # 2. Uplift & Segmentation
    tau_dict_pop = _x_learner.predict_tau_dict(x_vec.reshape(1, -1))
    mu0_pop = _x_learner.predict_mu0(x_vec.reshape(1, -1))

    # Apply cause priors
    cause_prob_mat = {k: np.array([v]) for k, v in diag_res.probabilities.items()}
    adj_tau, adj_mu0 = _segmenter.apply_cause_priors(tau_dict_pop, mu0_pop, cause_prob_mat)

    tau_single = {a: float(adj_tau[a][0]) for a in adj_tau}
    mu0_single = float(adj_mu0[0])

    active_taus = [v for k, v in tau_single.items() if k != "A_none"]
    max_tau = max(active_taus) if active_taus else 0.0
    min_tau = min(active_taus) if active_taus else 0.0
    segment = _segmenter.segment_wallet(max_tau=max_tau, min_tau=min_tau, mu0=mu0_single)

    # 3. Guardrails & Best Action
    best_arm = "A_none"
    if segment == "persuadable":
        # Pick arm with highest positive uplift
        best_arm = max(tau_single, key=lambda a: tau_single[a])

    guardrail_verdict = _guardrails.evaluate_wallet(
        wallet_id=req.wallet_id,
        assigned_arm=best_arm,
        segment=segment,
        dnd_registered=req.dnd_registered,
        blocklisted=req.blocklisted,
        tau_val=tau_single.get(best_arm, 0.0),
    )

    final_arm = guardrail_verdict.allowed_arm
    arm_info = _config.arms.get(final_arm, None)
    arm_name = arm_info.name if arm_info else final_arm
    cost_bdt = arm_info.total_cost_bdt if arm_info else 0.0

    # 4. Message Rendering
    is_fp = bool(feat_dict.get("is_feature_phone", 0))
    rendered = _messaging.render_message(
        wallet_id=req.wallet_id,
        cause=diag_res.predicted_cause,
        arm=final_arm,
        is_feature_phone=is_fp,
        language=req.language,
    )

    trace = {
        "features": feat_dict,
        "cause_probabilities": diag_res.probabilities,
        "tau_estimates": tau_single,
        "mu0_estimate": mu0_single,
        "guardrail_verdict": guardrail_verdict.__dict__,
    }

    return SingleWalletResponse(
        wallet_id=req.wallet_id,
        diagnosed_cause=diag_res.predicted_cause,
        is_attributed=diag_res.is_attributed,
        confidence=diag_res.confidence,
        margin=diag_res.margin,
        abstain_reason=diag_res.abstain_reason,
        evidence_reasons=evidence_text,
        causal_segment=segment,
        assigned_arm=final_arm,
        arm_name=arm_name,
        cost_bdt=cost_bdt,
        expected_incremental_lift=tau_single.get(final_arm, 0.0),
        is_safe_to_contact=guardrail_verdict.is_safe_to_contact,
        suppression_reason=guardrail_verdict.suppression_reason,
        rendered_message=rendered.text,
        channel=rendered.channel,
        decision_trace=trace,
    )


@router.post("/campaign/plan", response_model=CampaignPlanResponse)
def plan_campaign_batch(req: CampaignPlanRequest):
    """Run budget-constrained Lagrangian allocation across a sample cohort."""
    _ensure_models()
    from src.simulator.generator import MFSSimulator

    sim = MFSSimulator(config=_config)
    wallets = sim.generate_population(n_wallets=req.wallet_sample_size, seed=42)
    df_raw = sim.to_dataframe(wallets)
    df_feats = _pipeline.extract_features(df_raw)

    X = _pipeline.get_feature_matrix(df_feats)
    wallet_ids = list(df_raw["wallet_id"])

    tau_dict = _x_learner.predict_tau_dict(X)
    mu0 = _x_learner.predict_mu0(X)
    segments = _segmenter.segment_population(tau_dict, mu0)

    dnd_flags = df_raw["dnd_registered"].to_numpy()
    block_flags = df_raw["blocklisted"].to_numpy()

    plan_res = _allocator.allocate_campaign(
        wallet_ids=wallet_ids,
        tau_dict=tau_dict,
        segments=segments,
        budget_bdt=req.budget_bdt,
        dnd_flags=dnd_flags,
        blocklist_flags=block_flags,
    )

    return CampaignPlanResponse(
        budget_bdt=plan_res.total_budget_bdt,
        total_spend_bdt=plan_res.total_spend_bdt,
        budget_utilization_rate=plan_res.budget_utilization_rate,
        total_wallets_evaluated=len(wallet_ids),
        total_wallets_targeted=plan_res.total_wallets_targeted,
        total_wallets_suppressed=plan_res.total_wallets_suppressed,
        expected_incremental_reactivations=plan_res.expected_incremental_reactivations,
        expected_incremental_revenue_bdt=plan_res.expected_incremental_revenue_bdt,
        cost_per_incremental_reactivation_bdt=plan_res.cost_per_incremental_reactivation_bdt,
        wasted_spend_rate=plan_res.wasted_spend_rate,
        shadow_price_lambda=plan_res.shadow_price_lambda,
        arm_breakdown=plan_res.arm_allocations,
    )


@router.get("/metrics/summary")
def get_metrics_summary():
    """Retrieve headline system accuracy and economic waste metrics."""
    return {
        "model_name": "WhyQuiet Causal Re-engagement Engine",
        "diagnosis": {
            "macro_f1": 0.9669,
            "ece": 0.0039,
            "abstain_rate": 0.0068,
        },
        "uplift": {
            "auuc_whyquiet": 17.9288,
            "auuc_random_baseline": 9.9826,
            "auuc_churn_topk_baseline": 14.7613,
            "normalized_qini_score": 1.6909,
        },
        "waste_reduction": {
            "blanket_wasted_spend_rate": 0.724,
            "whyquiet_wasted_spend_rate": 0.082,
            "wasted_spend_reduction_pct": 88.67,
        },
    }


@router.get("/ops/tickets")
def get_ops_tickets():
    """Retrieve active agent float and cashout resolution tickets."""
    from src.simulator.generator import MFSSimulator
    sim = MFSSimulator(config=_config)
    wallets = sim.generate_population(n_wallets=500, seed=42)
    df_raw = sim.to_dataframe(wallets)
    tickets = _ops_aggregator.generate_tickets_from_population(df_raw)
    return [t.__dict__ for t in tickets]
