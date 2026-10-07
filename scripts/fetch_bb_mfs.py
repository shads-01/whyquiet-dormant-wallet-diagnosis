"""Fetch Bangladesh Bank MFS monthly statistics and write data/public/bb_mfs_monthly.csv.

Source: https://www.bb.org.bd/en/index.php/financialactivity/mfsdata
Idempotent script using standard library only.
"""

from __future__ import annotations

import csv
import datetime
import html
import http.cookiejar
import logging
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("fetch_bb_mfs")

SOURCE_URL = "https://www.bb.org.bd/en/index.php/financialactivity/mfsdata"
OUTPUT_PATH = Path("data/public/bb_mfs_monthly.csv")

MONTH_MAP = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}


class MFSHTMLTableParser(HTMLParser):
    """Parses plain <table> structure into a 2D matrix of strings."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None
        self._in_cell = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._current_row = []
        elif tag in ("td", "th") and self._current_row is not None:
            self._in_cell = True
            self._current_cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._in_cell and self._current_row is not None:
            self._in_cell = False
            raw_text = "".join(self._current_cell or [])
            # Clean non-breaking spaces and whitespace
            cell_text = html.unescape(raw_text).replace("\xa0", " ").strip()
            self._current_row.append(cell_text)
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None:
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = None

    def handle_data(self, data: str) -> None:
        if self._in_cell and self._current_cell is not None:
            self._current_cell.append(data)


def clean_number(val: str | None) -> float | None:
    """Strip commas and spaces, returning float or None."""
    if val is None:
        return None
    cleaned = val.replace(",", "").replace(" ", "").replace("&nbsp;", "").strip()
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_mfs_html(html_content: str, fetched_at: str) -> list[dict[str, int | str]]:
    """Parse Bangladesh Bank MFS HTML table and extract standardized monthly records.

    Raises ValueError if expected labels are missing (guarding against layout drift).
    """
    parser = MFSHTMLTableParser()
    parser.feed(html_content)
    rows = parser.rows
    if not rows:
        return []

    header = rows[0]
    month_cols: list[tuple[int, str]] = []
    for idx, cell in enumerate(header):
        m = re.search(r"Amount in ([A-Za-z]+)[\s,]+(\d{4})", cell)
        if m:
            mo_name = m.group(1).lower()
            year = m.group(2)
            if mo_name in MONTH_MAP:
                month_cols.append((idx, f"{year}-{MONTH_MAP[mo_name]}"))

    if not month_cols:
        return []

    agents_row: list[str] | None = None
    reg_cust_total_row: list[str] | None = None
    mfs_users_total_row: list[str] | None = None
    active_acc_row: list[str] | None = None
    txn_count_row: list[str] | None = None
    txn_val_row: list[str] | None = None

    in_reg_customers = False

    for r in rows:
        if len(r) < 2:
            continue
        desc = r[1].strip()
        desc_lower = desc.lower()

        if "no. of agents" in desc_lower:
            agents_row = r
        elif "no. of registered customer in lac" in desc_lower:
            in_reg_customers = True
        elif in_reg_customers and desc_lower == "total":
            reg_cust_total_row = r
            in_reg_customers = False
        elif "total no of mfs users in lac" in desc_lower:
            mfs_users_total_row = r
        elif "no. of active accounts in lac" in desc_lower:
            active_acc_row = r
        elif "no. of total transaction" in desc_lower:
            txn_count_row = r
        elif "total transaction in crore bdt" in desc_lower:
            txn_val_row = r

    # Guard against layout drift: assert every expected label exists
    if agents_row is None:
        raise ValueError("Missing required label: 'No. of agents'")
    if reg_cust_total_row is None:
        raise ValueError("Missing required label: 'Total' under 'No. of registered customer in Lac'")
    if mfs_users_total_row is None:
        raise ValueError("Missing required label: 'Total No of MFS users in Lac (Customer + Merchant)'")
    if active_acc_row is None:
        raise ValueError("Missing required label: 'No. of active accounts in Lac*'")
    if txn_count_row is None:
        raise ValueError("Missing required label: 'No. of total transaction'")
    if txn_val_row is None:
        raise ValueError("Missing required label: 'Total transaction in crore BDT'")

    records: list[dict[str, int | str]] = []
    for col_idx, mo_str in month_cols:
        v_agents = clean_number(agents_row[col_idx]) if col_idx < len(agents_row) else None
        v_reg = clean_number(reg_cust_total_row[col_idx]) if col_idx < len(reg_cust_total_row) else None
        v_mfs = clean_number(mfs_users_total_row[col_idx]) if col_idx < len(mfs_users_total_row) else None
        v_act = clean_number(active_acc_row[col_idx]) if col_idx < len(active_acc_row) else None
        v_cnt = clean_number(txn_count_row[col_idx]) if col_idx < len(txn_count_row) else None
        v_val = clean_number(txn_val_row[col_idx]) if col_idx < len(txn_val_row) else None

        records.append({
            "month": mo_str,
            "agents": round(v_agents) if v_agents is not None else "",
            "registered_customers": round(v_reg * 100_000) if v_reg is not None else "",
            "mfs_users_total": round(v_mfs * 100_000) if v_mfs is not None else "",
            "active_accounts": round(v_act * 100_000) if v_act is not None else "",
            "txn_count": round(v_cnt) if v_cnt is not None else "",
            "txn_value_bdt": round(v_val * 10_000_000) if v_val is not None else "",
            "source_url": SOURCE_URL,
            "fetched_at": fetched_at,
        })

    return records


def build_http_opener() -> urllib.request.OpenerDirector:
    """Build a urllib opener with a cookie jar and standard browser headers."""
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [
        (
            "User-Agent",
            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/122.0.0.0 Safari/537.36"
            ),
        ),
        (
            "Accept",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        ),
        ("Accept-Language", "en-US,en;q=0.9"),
    ]
    return opener


def fetch_month_page(
    opener: urllib.request.OpenerDirector,
    year: int,
    month: int,
    timeout: int = 30,
) -> str | None:
    """POST to Bangladesh Bank MFS search form for a specific year and month."""
    mo_str = f"{month:02d}"
    data = urllib.parse.urlencode({
        "select_month": mo_str,
        "select_year": str(year),
        "mfssearch_submit": "Search",
    }).encode("utf-8")

    req = urllib.request.Request(
        SOURCE_URL,
        data=data,
        headers={
            "Origin": "https://www.bb.org.bd",
            "Referer": SOURCE_URL,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        resp = opener.open(req, timeout=timeout)
        content = resp.read().decode("utf-8", errors="ignore")
        return content
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.warning("Error fetching %04d-%02d: %s", year, month, exc)
        return None


def fetch_all_mfs_data(
    start_year: int = 2022,
    end_year: int = 2026,
    delay_seconds: float = 1.5,
) -> tuple[dict[str, dict[str, int | str]], list[str], list[str]]:
    """Fetch monthly MFS data across year range, de-duplicate, and track discrepancies.

    Returns (records_by_month, months_fetched, discrepancies).
    """
    opener = build_http_opener()
    today_iso = datetime.datetime.now(datetime.UTC).date().isoformat()

    # Initial GET to establish session cookies
    logger.info("Initializing session with GET to %s", SOURCE_URL)
    try:
        opener.open(SOURCE_URL, timeout=30).read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.warning("Initial GET failed: %s. Continuing with POST requests.", exc)

    time.sleep(delay_seconds)

    records_by_month: dict[str, dict[str, int | str]] = {}
    discrepancies: list[str] = []
    months_fetched: list[str] = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            mo_key = f"{year}-{month:02d}"
            html_content = fetch_month_page(opener, year, month)

            # Check if retry is needed
            if html_content is None or ("Amount in" not in html_content and "table" not in html_content):
                logger.info("Retrying fetch for %s...", mo_key)
                time.sleep(delay_seconds)
                html_content = fetch_month_page(opener, year, month)

            if not html_content or "Amount in" not in html_content:
                logger.info("No data available for %s", mo_key)
                time.sleep(delay_seconds)
                continue

            try:
                extracted = parse_mfs_html(html_content, today_iso)
            except ValueError as val_err:
                logger.error("Layout drift detected for %s: %s", mo_key, val_err)
                raise

            if not extracted:
                time.sleep(delay_seconds)
                continue

            months_fetched.append(mo_key)
            logger.info("Successfully fetched %s (contained: %s)", mo_key, [e["month"] for e in extracted])

            for item in extracted:
                target_m = str(item["month"])
                if target_m in records_by_month:
                    prev = records_by_month[target_m]
                    # Check if numbers differ
                    diff_fields = [
                        k for k in ("agents", "registered_customers", "active_accounts", "txn_count", "txn_value_bdt")
                        if prev.get(k) != item.get(k)
                    ]
                    if diff_fields:
                        disc_msg = (
                            f"Discrepancy for month {target_m} between earlier report and publication {mo_key}: "
                            f"fields {diff_fields} (earlier: {[prev[f] for f in diff_fields]}, "
                            f"later: {[item[f] for f in diff_fields]}). Keeping later publication."
                        )
                        discrepancies.append(disc_msg)
                        logger.info(disc_msg)
                # Keep later publication
                records_by_month[target_m] = item

            time.sleep(delay_seconds)

    return records_by_month, months_fetched, discrepancies


def save_to_csv(records: dict[str, dict[str, int | str]], output_file: Path) -> None:
    """Save records to CSV sorted chronologically."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "month",
        "agents",
        "registered_customers",
        "mfs_users_total",
        "active_accounts",
        "txn_count",
        "txn_value_bdt",
        "source_url",
        "fetched_at",
    ]

    sorted_months = sorted(records.keys())
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in sorted_months:
            writer.writerow(records[m])

    logger.info("Wrote %d monthly rows to %s", len(sorted_months), output_file)


def main() -> None:
    """Run fetch, parse, and save pipeline."""
    records, fetched, discrepancies = fetch_all_mfs_data()
    if not records:
        logger.error("No MFS records were extracted! Exiting without writing.")
        sys.exit(1)

    save_to_csv(records, OUTPUT_PATH)

    print("\n" + "=" * 60)
    print("FETCH SUMMARY")
    print("=" * 60)
    print(f"Total months in dataset: {len(records)}")
    sorted_months = sorted(records.keys())
    print(f"Date range: {sorted_months[0]} to {sorted_months[-1]}")
    print(f"Publication requests successful: {len(fetched)}")
    print(f"Discrepancies resolved: {len(discrepancies)}")
    for d in discrepancies:
        print(f"  - {d}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
