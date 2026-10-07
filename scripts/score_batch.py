"""Score a ledger extract offline with the same code as POST /api/score, and report throughput (D55).

Input: flat CSV or Parquet, one row per wallet-week (docs/contracts/ingest.md), e.g. web/public/sample-ledger.csv.
Output: .json (full results) or .csv (one row per wallet).
Run: uv run python scripts/score_batch.py --in web/public/sample-ledger.csv --out triage.csv
"""

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.api.schemas import ScoreRequest, ScoreResult
from src.api.score import score

HEADER = ["wallet_id", "acquired_week", "fee_week", "pay_cycle"]
CHUNK = 500  # same cap as one API request


def ledger_wallets(df: pd.DataFrame) -> list[dict]:
    """Flat wallet-week rows -> API wallet objects (what web/src/Score.tsx does in the browser)."""
    wallets: dict[str, dict] = {}
    for rec in df.to_dict("records"):
        w = wallets.get(rec["wallet_id"])
        if w is None:
            w = wallets[rec["wallet_id"]] = {**{k: rec[k] for k in HEADER}, "weeks": []}
        w["weeks"].append({k: None if pd.isna(v) else v for k, v in rec.items() if k not in HEADER})  # NaN -> null
    return list(wallets.values())


def run(src: Path) -> tuple[list[ScoreResult], float]:
    df = pd.read_parquet(src) if src.suffix == ".parquet" else pd.read_csv(src)
    start = time.perf_counter()
    wallets = ledger_wallets(df)
    results: list[ScoreResult] = []
    for i in range(0, len(wallets), CHUNK):
        results += score(ScoreRequest.model_validate({"wallets": wallets[i:i + CHUNK]}), "cli").results
    return results, time.perf_counter() - start


def write(results: list[ScoreResult], out: Path) -> None:
    if out.suffix == ".json":
        out.write_text(json.dumps([r.model_dump(mode="json") for r in results], ensure_ascii=False), encoding="utf-8")
        return
    pd.DataFrame([{
        "wallet_id": r.wallet_id, "verdict": r.verdict, "cause": r.cause.value if r.cause else "",
        "confidence": max(r.posterior.values(), default=0.0), "weeks_silent": r.weeks_silent,
        "remedy_code": r.remedy.remedy_code if r.remedy else "", "unit_cost_bdt": r.remedy.unit_cost_bdt if r.remedy else 0,
        "refusal_reasons": " | ".join(r.refusal_reasons),
    } for r in results]).to_csv(out, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--in", dest="src", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    results, secs = run(args.src)
    write(results, args.out)
    refused = sum(r.verdict == "refused" for r in results)
    print(f"scored {len(results)} wallets ({refused} refused) in {secs:.2f}s = {len(results) / secs:,.0f} wallets/s "
          f"-> {args.out}")
