"""scripts/depth.py: coverage, calibration, label-free checks, stress tests, ablation, decision-aware money (D60-D64)."""

from pathlib import Path

import numpy as np
import pytest

from datagen.generate import main as generate
from scripts.depth import (
    DIAL,
    GROUPS,
    atc,
    aurc,
    coverage_curve,
    depth,
    em_mix,
    fit_temperature,
    psi,
    temperature,
)
from src.model.train import CAUSES


def onehot(idx: list[int], conf: float = 0.9) -> np.ndarray:
    p = np.full((len(idx), len(CAUSES)), (1 - conf) / (len(CAUSES) - 1))
    p[np.arange(len(idx)), idx] = conf
    return p


def test_coverage_curve_answers_most_confident_first():
    proba = np.vstack([onehot([0], 0.99), onehot([1], 0.4)])  # sure and right, unsure and wrong
    rows = coverage_curve(proba, ["job_exit", "job_exit"])
    full, half = rows[0], next(r for r in rows if r["coverage"] == 0.5)
    assert full["accuracy"] == 0.5 and half["accuracy"] == 1.0


def test_aurc_zero_when_always_right_and_lower_when_errors_are_unsure():
    truth = ["job_exit", "migration"]
    assert aurc(onehot([0, 1]), truth) == 0.0
    unsure_wrong = np.vstack([onehot([0], 0.99), onehot([0], 0.4)])
    sure_wrong = np.vstack([onehot([0], 0.4), onehot([0], 0.99)])
    assert aurc(unsure_wrong, truth) < aurc(sure_wrong, truth)


def test_temperature_one_is_identity_and_fit_prefers_cooling_overconfidence():
    proba = onehot([0, 1, 2])
    assert np.allclose(temperature(proba, 1.0), proba)
    y = np.array([0] * 6 + [1] * 4)  # 99% sure of cause 0, right only 60% of the time
    assert fit_temperature(onehot([0] * 10, 0.99), y) > 1.0


def test_atc_matches_validation_accuracy_on_the_same_data():
    proba = np.vstack([onehot([0] * 8, 0.95), onehot([1] * 2, 0.6)])
    y = np.array([0] * 8 + [0] * 2)  # the two unsure ones are wrong: accuracy 0.8
    assert atc(proba, y, proba) == pytest.approx(0.8)


def test_em_mix_recovers_shifted_prior():
    rng = np.random.default_rng(0)
    means = np.eye(len(CAUSES)) * 3  # one Gaussian per cause; the classifier is Bayes-optimal under a uniform prior
    def post(x: np.ndarray, prior: np.ndarray) -> np.ndarray:
        lik = np.exp(-0.5 * ((x[:, None, :] - means[None]) ** 2).sum(-1)) * prior
        return lik / lik.sum(axis=1, keepdims=True)
    uniform = np.full(len(CAUSES), 0.2)
    shifted = np.array([0.5, 0.2, 0.1, 0.1, 0.1])
    y = rng.choice(len(CAUSES), 20000, p=shifted)
    x = means[y] + rng.normal(size=(len(y), len(CAUSES)))
    assert np.abs(em_mix(post(x, uniform), uniform) - shifted).max() < 0.02


def test_psi_zero_for_same_data_and_large_for_shift_including_categorical():
    rng = np.random.default_rng(0)
    a = rng.normal(size=5000)
    assert psi(a, a) == pytest.approx(0.0, abs=1e-9)
    assert psi(a, a + 1) > 0.25
    flags = (rng.random(5000) < 0.1).astype(float)
    assert psi(flags, flags) == pytest.approx(0.0, abs=1e-9)
    assert psi(flags, (rng.random(5000) < 0.5).astype(float)) > 0.25


@pytest.fixture(scope="module")
def rep(tmp_path_factory: pytest.TempPathFactory) -> dict:
    root: Path = tmp_path_factory.mktemp("depth")
    generate(0, root)
    return depth(0, root)


def test_operating_point_sits_on_the_coverage_story(rep: dict):
    cov = rep["coverage"]
    assert cov["lightgbm"][0]["coverage"] == 1.0
    assert 0.5 < cov["operating_point"]["coverage"] < 1.0
    assert cov["operating_point"]["macro_f1"] > cov["lightgbm"][0]["macro_f1"]  # refusing raises quality
    lo, hi = rep["macro_f1_b_ci95"]
    assert lo <= cov["operating_point"]["macro_f1"] <= hi


def test_baseline_ladder_and_lightgbm_ranks_its_errors_better(rep: dict):
    f1 = {b["name"]: b["macro_f1_b"] for b in rep["baselines"]}
    assert f1["majority"] < f1["expert_rule"] < f1["lightgbm_refusal"]
    assert rep["coverage"]["aurc"]["lightgbm"] < rep["coverage"]["aurc"]["logreg"]
    assert {g["held_out"] for g in rep["group_shift"]} == {"weekly", "biweekly", "monthly"}


def test_refusal_targets_ambiguity_and_the_unseen_cause(rep: dict):
    blended = {r["group"]: r for r in rep["blended"]}
    assert blended["blended"]["refusal_rate"] > blended["clean"]["refusal_rate"]
    unseen = rep["stress"]["unseen_cause"]
    assert unseen["n"] > 0 and unseen["refusal_rate_novel"] > unseen["refusal_rate_known"]


def test_noise_dial_lowers_quality_and_raises_refusal(rep: dict):
    dial = rep["stress"]["noise_dial"]
    assert [d["level"] for d in dial] == [d[0] for d in DIAL]
    assert dial[-1]["macro_f1_all"] < dial[0]["macro_f1_all"]
    assert dial[-1]["refusal_rate"] > dial[0]["refusal_rate"]


def test_label_free_checks_beat_naive_answers(rep: dict):
    lf = rep["label_free"]
    acc = lf["accuracy"]
    assert abs(acc["atc_estimate"] - acc["true"]) < abs(acc["confidence"] - acc["true"])
    assert lf["cause_mix_max_error"]["em"] < lf["cause_mix_max_error"]["train"]
    assert lf["drift"]["domain_auc"] > 0.9  # B is visibly a different population
    assert len(lf["drift"]["psi"]) == 20


def test_ablation_covers_every_feature_once(rep: dict):
    assert [a["group"] for a in rep["ablation"]] == list(GROUPS)
    assert sorted(f for a in rep["ablation"] for f in a["features"]) == sorted(
        r["feature"] for r in rep["label_free"]["drift"]["psi"])


def test_money_ev_rows_and_oracle_is_the_ceiling(rep: dict):
    rows = rep["money_ev"]
    assert len(rows) == 12
    for rate in (0.01, 0.04, 0.08):
        value = {r["strategy"]: r["value_bdt"] for r in rows if r["recovery_rate"] == rate}
        assert value["oracle"] >= max(value["rule"], value["model"], value["model_ev"])
        assert value["model_ev"] >= value["model"]
