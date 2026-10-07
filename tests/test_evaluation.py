"""Unit tests for EvaluationRunner in WhyQuiet."""

import tempfile
from pathlib import Path

from src.config import get_config
from src.evaluation.runner import EvaluationRunner


def test_evaluation_runner_pipeline():
    """Verify that EvaluationRunner runs cleanly and exports metrics on small cohort."""
    config = get_config()
    with tempfile.TemporaryDirectory() as tmp_dir:
        runner = EvaluationRunner(config=config, results_dir=Path(tmp_dir))
        df_comp = runner.run_full_evaluation(n_wallets=150, budget_bdt=1500.0)

        assert not df_comp.empty
        assert "Strategy" in df_comp.columns
        assert "Incremental reactivations" in df_comp.columns
        assert (Path(tmp_dir) / "strategy_comparison.csv").exists()
        assert (Path(tmp_dir) / "confusion_matrix.png").exists()
        assert (Path(tmp_dir) / "qini_curves.png").exists()
        assert (Path(tmp_dir) / "calibration_curve.png").exists()
        assert (Path(tmp_dir) / "budget_adherence.png").exists()
        assert (Path(tmp_dir) / "noise_robustness.png").exists()
