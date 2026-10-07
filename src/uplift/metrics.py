"""Qini Curve and AUUC evaluation utilities for Uplift Models."""

from typing import Any

import numpy as np


def compute_qini_curve(
    y_true: np.ndarray,
    w_treatment: np.ndarray,
    tau_scores: np.ndarray,
    n_bins: int = 50,
) -> dict[str, Any]:
    """Calculate cumulative Qini curve and normalized AUUC.

    Parameters
    ----------
    y_true : np.ndarray
        Observed binary outcome vector (1 = reactivated, 0 = dormant).
    w_treatment : np.ndarray
        Binary treatment indicator (1 = treated, 0 = control).
    tau_scores : np.ndarray
        Predicted uplift score tau(x) used for sorting.
    n_bins : int
        Number of evaluation percentiles.

    Returns
    -------
    dict[str, Any]
        Dictionary with percentiles, cumulative uplift values, Qini curve, and AUUC.
    """
    n = len(y_true)
    if n == 0:
        return {
            "percentiles": [],
            "qini": [],
            "random_qini": [],
            "auuc": 0.0,
            "qini_score": 0.0,
        }

    # Sort descending by predicted tau score
    order = np.argsort(tau_scores)[::-1]
    y_sorted = y_true[order]
    w_sorted = w_treatment[order]

    cum_y_t = np.cumsum(y_sorted * w_sorted)
    cum_y_c = np.cumsum(y_sorted * (1 - w_sorted))

    total_w_t = float(np.sum(w_treatment))
    total_w_c = float(np.sum(1 - w_treatment))

    if total_w_t == 0 or total_w_c == 0:
        return {
            "percentiles": [],
            "qini": [],
            "random_qini": [],
            "auuc": 0.0,
            "qini_score": 0.0,
        }

    bin_indices = np.linspace(0, n - 1, n_bins + 1, dtype=int)
    percentiles = []
    qini_vals = []
    random_qini_vals = []

    # Final overall incremental count
    total_inc = float(cum_y_t[-1] - (cum_y_c[-1] * (total_w_t / total_w_c)))

    for idx in bin_indices:
        pct = float(idx / (n - 1)) if n > 1 else 0.0
        # Qini formula: n_{t,y=1} - n_{c,y=1} * (N_t / N_c)
        q = float(cum_y_t[idx] - (cum_y_c[idx] * (total_w_t / total_w_c)))
        rand_q = float(pct * total_inc)

        percentiles.append(pct)
        qini_vals.append(q)
        random_qini_vals.append(rand_q)

    # Compute AUUC using trapezoidal integration
    auuc = float(np.trapezoid(qini_vals, percentiles))
    rand_auuc = float(np.trapezoid(random_qini_vals, percentiles))
    qini_score = float(auuc - rand_auuc)

    return {
        "percentiles": percentiles,
        "qini": qini_vals,
        "random_qini": random_qini_vals,
        "auuc": auuc,
        "qini_score": qini_score,
    }
