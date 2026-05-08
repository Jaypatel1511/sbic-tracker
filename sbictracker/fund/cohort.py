"""
Vintage-year cohort analysis and peer quartile ranking.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from sbictracker.data.schema import Investment
from sbictracker.fund.metrics import called_capital, distributed_capital, dpi, nav, tvpi


def vintage_year_analysis(investments: List[Investment]) -> Dict[int, dict]:
    """Group investments by vintage year and compute per-cohort metrics.

    Parameters
    ----------
    investments:
        Full investment universe.

    Returns
    -------
    Dict mapping vintage_year → metric dict.
    """
    by_vintage: Dict[int, List[Investment]] = defaultdict(list)
    for inv in investments:
        by_vintage[inv.vintage_year].append(inv)

    result = {}
    for yr, cohort in sorted(by_vintage.items()):
        cc = called_capital(cohort)
        dc = distributed_capital(cohort)
        n = nav(cohort)
        result[yr] = {
            "vintage_year": yr,
            "count": len(cohort),
            "called_capital": cc,
            "distributed_capital": dc,
            "nav": n,
            "tvpi": tvpi(cohort),
            "dpi": dpi(cohort),
            "realized_count": sum(1 for i in cohort if i.is_realized),
            "unrealized_count": sum(1 for i in cohort if not i.is_realized),
        }
    return result


def peer_quartile_ranking(
    fund_tvpi: float,
    peer_tvpis: List[float],
) -> Dict[str, object]:
    """Return the percentile rank and quartile of a fund TVPI vs a peer set.

    Parameters
    ----------
    fund_tvpi:
        The fund's TVPI to rank.
    peer_tvpis:
        List of peer fund TVPIs (including or excluding the fund itself).

    Returns
    -------
    Dict with 'percentile', 'quartile' (1=top), and 'peer_count'.
    """
    if not peer_tvpis:
        raise ValueError("peer_tvpis must not be empty")

    sorted_peers = sorted(peer_tvpis)
    n = len(sorted_peers)
    # fraction of peers the fund beats
    beats = sum(1 for p in sorted_peers if fund_tvpi > p)
    percentile = beats / n * 100

    if percentile >= 75:
        quartile = 1
    elif percentile >= 50:
        quartile = 2
    elif percentile >= 25:
        quartile = 3
    else:
        quartile = 4

    return {
        "fund_tvpi": fund_tvpi,
        "percentile": round(percentile, 1),
        "quartile": quartile,
        "peer_count": n,
        "peer_median": sorted_peers[n // 2],
    }
