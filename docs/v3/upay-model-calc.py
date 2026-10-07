# Derivation check for docs/v3/upay-model.md
# Run: python docs/v3/upay-model-calc.py
# Every number in the doc that is presented as derived should appear here.

# --- bKash FY2024 audited (legacy.bracbank.com/.../december-31-2024.pdf) ---
comm, air, trust = 47_348_509_688, 1_163_864_848, 8_780_951_978
gross, vat, rev = 57_293_326_514, 6_711_270_107, 50_582_056_407
cos, gp, opex, commexp, profit = 32_697_675_477, 17_884_380_930, 10_472_064_526, 3_996_902_095, 3_157_732_847
assert comm + air + trust == gross and gross - vat == rev
assert rev - cos == gp and gp - opex - commexp == 3_415_414_309

# --- bKash FY2025 (bonikbarta, from bKash financial statements) ---
rev25, cos25, np25 = 65.65e9, 41.48e9, 6.61e9
active, reg, emoney = 47e6, 82e6, 110.04e9
arpu = rev25 / active
dormant = reg - active

# --- Bangladesh Bank MFS industry ---
oct_txn, oct_val = 678.63e6, 1.58e12
p2p_t, p2p_v = 134.26e6, 476.93e9
ci_t, ci_v = 142.55e6, 413.17e9
co_t, co_v = 174.56e6, 372.23e9

def pct(a, b): return a / b * 100
def cr(n): return n / 1e7

if __name__ == "__main__":
    print("FY2024 revenue mix (of gross):")
    for n, v in [("commission", comm), ("airtime", air), ("trust/float", trust)]:
        print(f"  {n:12s} {pct(v, gross):6.2f}%   {pct(v, rev):6.2f}% of net")
    print(f"cost of services / revenue FY24 {pct(cos, rev):.2f}%  FY25 {pct(cos25, rev25):.2f}%")
    print(f"net margin FY24 {pct(profit, rev):.2f}%  FY25 {pct(np25, rev25):.2f}%")
    print(f"FY24 float yield on end-24 trust bal {pct(trust, 94_072_835_312):.2f}%")
    print(f"ARPU {arpu:,.0f}/yr  {arpu/12:,.0f}/mo | active rate {pct(active, reg):.1f}% | dormant {dormant/1e6:.0f}m")
    print(f"1% of FY25 revenue = Tk {cr(rev25*0.01):.0f} crore")
    print(f"avg ticket: Oct25 Tk {oct_val/oct_txn:,.0f} | P2P {p2p_v/p2p_t:,.0f} | cash-in {ci_v/ci_t:,.0f} | cash-out {co_v/co_t:,.0f}")
    print(f"cash-in+cash-out = {pct(ci_v+co_v, oct_val):.1f}% of Oct25 value")
    print(f"reactivation: 1% dormant = {dormant*0.01/1e3:.0f}k users -> Tk {cr(dormant*0.01*arpu):.0f} cr full ARPU, Tk {cr(dormant*0.01*arpu*0.5):.0f} cr at 50%")
    lift_pp = pct(active, reg) * 0.01
    lift_users = reg * lift_pp / 100
    print(f"1% rel. lift in active rate = +{lift_pp:.2f}pp -> {lift_users/1e3:.0f}k users -> Tk {cr(lift_users*arpu):.0f} cr")
    co_ticket = co_v / co_t
    # CORRECTION (2026-10-03): the old line used 18.50*1e6, i.e. assumed every cash-out is
    # exactly Tk 1,000. The Oct-2025 average cash-out ticket is Tk 2,132, so gross revenue
    # per million cash-outs is ~2.13x higher. Also: a 1% RELATIVE cut in cost-to-serve is
    # 0.632% of revenue, not 1% of revenue.
    for label, rate in [("bKash agent 1.850%", 0.0185), ("upay AGENT 1.400%", 0.0140), ("upay UCB ATM 0.800%", 0.0080)]:
        print(f"1m extra cash-outs @{label} @Tk{co_ticket:,.0f} avg ticket "
              f"= Tk {co_ticket*rate*1e6/1e7:.2f} crore gross")
    print(f"upay agent vs bKash agent: 1.40% is {(1-0.0140/0.0185)*100:.0f}% cheaper "
          f"(NOT 43% - that compared upay's 0.80% ATM rate to bKash's 1.85% AGENT rate)")
    print(f"1% RELATIVE cut in cost-to-serve = {cos25*0.01/rev25*100:.3f}% of revenue "
          f"= Tk {cos25*0.01/1e7:.1f} crore (NOT Tk 66 cr, which is 1% of revenue)")
    assert abs(cos25 / rev25 - 0.6318) < 1e-3
    assert abs(co_ticket - 2132) < 2
    assert abs(co_ticket * 0.0185 * 1e6 / 1e7 - 3.94) < 0.01
    assert abs(co_ticket * 0.0140 * 1e6 / 1e7 - 2.99) < 0.01
    assert abs((1 - 0.0140 / 0.0185) * 100 - 24) < 1
    assert abs(cos25 * 0.01 / 1e7 - 41.5) < 0.1
    print(f"rev per agent bKash Tk {rev25/350_000:,.0f}/yr; upay 130k agents at that rate = Tk {cr(rev25/350_000*130_000):.0f} cr")
