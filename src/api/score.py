"""POST /api/score: live triage of ledger extracts with the same model as seed.json (D55)."""

import hmac
import os
from typing import Annotated

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, Header, HTTPException

from src.api.auth import Actor, current_user, supabase_client
from src.api.schemas import (
    Remedy,
    RuleBaseline,
    ScoreRequest,
    ScoreResponse,
    ScoreResult,
    WalletHistory,
)
from src.model.features import WEEKS, features
from src.model.score import explain, load
from src.rules.baseline import rule_baseline
from src.rules.remedies import REMEDIES

router = APIRouter(prefix="/api")

COLUMNS = ["week", "txn_count", "amount_bdt", "cashin_count", "cashout_ok", "cashout_fail", "app_share",
           "district_changed"]
SILENT = (0, 0.0, 0, 0, 0, None, False)  # a week the ledger did not send


def scorer(
    x_api_key: Annotated[str | None, Header()] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    """upay backends send X-API-Key (SCORE_API_KEY); people send a signed-in analyst/approver bearer token."""
    if x_api_key is not None:
        expected = os.environ.get("SCORE_API_KEY", "")
        if not expected or not hmac.compare_digest(x_api_key, expected):
            raise HTTPException(401, "Invalid API key")
        return "api-key"
    actor: Actor = current_user(supabase_client(), authorization)
    return actor.id


def _weekly(wallets: list[WalletHistory]) -> pd.DataFrame:
    """One row per wallet-week from acquisition to week 51; weeks the ledger left out are silent."""
    rows = []
    for w in wallets:
        given = {r.week: tuple(getattr(r, c) for c in COLUMNS[1:]) for r in w.weeks}
        rows += [(w.wallet_id, wk, *given.get(wk, SILENT)) for wk in range(w.acquired_week, WEEKS)]
    return pd.DataFrame(rows, columns=["wallet_id", *COLUMNS]).astype({"app_share": float, "district_changed": int})


def _early_refusal(w: WalletHistory, weeks_silent: int, reason: str) -> ScoreResult:
    return ScoreResult(wallet_id=w.wallet_id, weeks_silent=weeks_silent, verdict="refused", cause=None, posterior={},
                       contributions=[], refusal_reasons=[reason],
                       rule_baseline=RuleBaseline(**rule_baseline(weeks_silent)), remedy=None)


@router.post("/score", response_model=ScoreResponse)
def score(req: ScoreRequest, _caller: Annotated[str, Depends(scorer)]) -> ScoreResponse:
    # Triage up to 500 wallets: verdict, posterior, reasons, rule baseline and priced remedy per wallet
    try:
        booster, meta = load()
    except FileNotFoundError as exc:
        raise HTTPException(503, "Scoring model not loaded") from exc

    results: dict[str, ScoreResult] = {}
    dormant: list[WalletHistory] = []
    for w in req.wallets:
        active = [r.week for r in w.weeks if r.txn_count > 0]
        if not active:
            results[w.wallet_id] = _early_refusal(
                w, WEEKS - w.acquired_week, "No transaction in the history, so there is no decline shape to read")
            continue
        silent = WEEKS - 1 - max(active)
        if not rule_baseline(silent)["fired"]:  # the 3-week rule lives in src/rules
            results[w.wallet_id] = _early_refusal(
                w, silent, f"Not dormant: last transaction {silent} week(s) ago, under the 3-week dormancy rule")
            continue
        dormant.append(w)

    if dormant:
        header = pd.DataFrame([{"wallet_id": w.wallet_id, "acquired_week": w.acquired_week,
                                "fee_week": w.fee_week, "pay_cycle": w.pay_cycle.value} for w in dormant])
        X = features(header, _weekly(dormant))
        for w, r, silent in zip(dormant, explain(booster, meta["tau"], meta["delta"], X),
                                X["weeks_silent"].astype(np.int64)):
            remedy = REMEDIES[r["cause"]] if r["cause"] else None
            results[w.wallet_id] = ScoreResult(
                wallet_id=w.wallet_id, weeks_silent=int(silent), rule_baseline=RuleBaseline(**rule_baseline(int(silent))),
                remedy=Remedy(**{k: remedy[k] for k in ("remedy_code", "label", "unit_cost_bdt")}) if remedy else None,
                **r)

    return ScoreResponse(model_version=meta["model_version"], tau=meta["tau"], delta=meta["delta"],
                         results=[results[w.wallet_id] for w in req.wallets])
