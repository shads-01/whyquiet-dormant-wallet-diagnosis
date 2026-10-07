"""Unit tests for Bangladesh Bank MFS fetcher and Upay dormant pool scenario model.

All tests run completely offline on saved fixtures (zero network calls).
"""

from __future__ import annotations

import pytest

from scripts.fetch_bb_mfs import clean_number, parse_mfs_html
from scripts.upay_dormant_pool import compute_dormant_pool_scenarios

SAMPLE_MFS_HTML = """
<!DOCTYPE html>
<html>
<head><title>Bangladesh Bank</title></head>
<body>
<p>Mobile Financial Services (MFS) comparative summary statement of January, 2025 and February, 2025</p>
<table>
<tr>
    <th>Serial no.</th>
    <th>Description</th>
    <th>Amount in January, 2025</th>
    <th>Amount in February, 2025</th>
    <th>% Change (January, 2025 to February, 2025)</th>
</tr>
<tr>
    <td>A.</th>
    <td colspan="3">Industry Wise Information</td>
</tr>
<tr><td>1</td><td class='text-left'>No. of Banks currently providing  the Services</td><td>13</td><td>13</td><td></td></tr>
<tr><td>2</td><td class='text-left'>&nbsp;No. of agents</td><td>1841979</td><td>1856190</td><td>0.77%</td></tr>
<tr><td>3</td><td class='text-left'>No. of registered customer in Lac</td><td></td><td></td><td></td></tr>
<tr><td></td><td class='text-left'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Male</td><td>1372.60</td><td>1378.80</td><td>0.45%</td></tr>
<tr><td></td><td class='text-left'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Female</td><td>1005.03</td><td>1010.20</td><td>0.51%</td></tr>
<tr><td></td><td class='text-left'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total</td><td>2380.83</td><td>2392.40</td><td>0.49%</td></tr>
<tr><td>4</td><td class='text-left'>No of merchant in Lac</td><td></td><td></td><td></td></tr>
<tr><td></td><td class='text-left'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Regular Merchant</td><td>3.59</td><td>3.63</td><td>1.11%</td></tr>
<tr><td></td><td class='text-left'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRA</td><td>8.60</td><td>8.64</td><td>0.47%</td></tr>
<tr><td></td><td class='text-left'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Total</td><td>12.20</td><td>12.26</td><td>0.49%</td></tr>
<tr><td>5</td><td class='text-left'>Total No of MFS users in Lac (Customer + Merchant)</td><td>2393.03</td><td>2404.66</td><td>0.49%</td></tr>
<tr><td>6</td><td class='text-left'>No. of active accounts in Lac*</td><td>893.84</td><td>871.54</td><td>-2.49%</td></tr>
<tr><td>7</td><td class='text-left'>No. of total transaction</td><td>721866474.00</td><td>671340910.00</td><td>-7%</td></tr>
<tr><td>8</td><td class='text-left'>Total transaction in crore BDT</td><td>171664.12</td><td>164726.30</td><td>-4.04%</td></tr>
</table>
</body>
</html>
"""


def test_clean_number():
    assert clean_number("1,841,979") == 1841979.0
    assert clean_number(" 2,380.83 ") == 2380.83
    assert clean_number("") is None
    assert clean_number(None) is None
    assert clean_number("&nbsp;123.45&nbsp;") == 123.45


def test_parse_mfs_html_fixture():
    records = parse_mfs_html(SAMPLE_MFS_HTML, fetched_at="2026-10-07")
    assert len(records) == 2

    jan = records[0]
    assert jan["month"] == "2025-01"
    assert jan["agents"] == 1841979
    assert jan["registered_customers"] == 238083000  # 2380.83 lac * 100,000
    assert jan["mfs_users_total"] == 239303000  # 2393.03 lac * 100,000
    assert jan["active_accounts"] == 89384000  # 893.84 lac * 100,000
    assert jan["txn_count"] == 721866474
    assert jan["txn_value_bdt"] == 1716641200000  # 171664.12 crore * 10,000,000

    feb = records[1]
    assert feb["month"] == "2025-02"
    assert feb["agents"] == 1856190
    assert feb["registered_customers"] == 239240000
    assert feb["mfs_users_total"] == 240466000
    assert feb["active_accounts"] == 87154000
    assert feb["txn_count"] == 671340910
    assert feb["txn_value_bdt"] == 1647263000000


def test_parse_mfs_html_layout_drift_guard():
    # Missing 'No. of agents'
    broken_html = SAMPLE_MFS_HTML.replace("No. of agents", "Missing Label Name")
    with pytest.raises(ValueError, match="Missing required label: 'No. of agents'"):
        parse_mfs_html(broken_html, fetched_at="2026-10-07")


def test_compute_dormant_pool_scenarios():
    record = {
        "month": "2025-02",
        "registered_customers": 239240000,
        "active_accounts": 87154000,
        "agents": 1856190,
        "mfs_users_total": 240466000,
        "txn_count": 671340910,
        "txn_value_bdt": 1647263000000,
    }
    payload = compute_dormant_pool_scenarios(record, upay_customers=7_000_000)

    meta = payload["metadata"]
    assert meta["latest_bb_month"] == "2025-02"
    expected_inactive_share = 1.0 - (87154000 / 239240000)
    assert pytest.approx(meta["industry_inactive_share"], 0.0001) == expected_inactive_share

    scenarios = payload["scenarios"]
    assert len(scenarios) == 3

    # Scenario 1: 50%
    assert scenarios[0]["scenario"] == "Conservative (50%)"
    assert scenarios[0]["dormant_wallets"] == 3_500_000
    assert not scenarios[0]["is_central"]

    # Scenario 2: Industry Central
    assert scenarios[1]["is_central"]
    assert scenarios[1]["dormant_wallets"] == round(7_000_000 * expected_inactive_share)

    # Scenario 3: 75%
    assert scenarios[2]["scenario"] == "Aggressive (75%)"
    assert scenarios[2]["dormant_wallets"] == 5_250_000
    assert not scenarios[2]["is_central"]
