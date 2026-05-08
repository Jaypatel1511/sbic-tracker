"""
Sector and geographic concentration analysis.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from sbictracker.data.schema import Investment, NAICS_SECTORS


def sector_breakdown(investments: List[Investment]) -> Dict[str, dict]:
    """Return a breakdown of investment dollars by 2-digit NAICS sector.

    Returns
    -------
    Dict mapping sector_code → {'sector_name', 'count', 'invested', 'pct_of_portfolio'}.
    """
    total_invested = sum(inv.investment_amount for inv in investments)
    by_sector: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "invested": 0.0})

    for inv in investments:
        code2 = inv.naics_code[:2]
        by_sector[code2]["count"] += 1
        by_sector[code2]["invested"] += inv.investment_amount

    result = {}
    for code2, data in sorted(by_sector.items(), key=lambda x: -x[1]["invested"]):
        result[code2] = {
            "sector_name": NAICS_SECTORS.get(code2, "Unknown"),
            "count": data["count"],
            "invested": data["invested"],
            "pct_of_portfolio": data["invested"] / total_invested if total_invested > 0 else 0.0,
        }
    return result


def state_breakdown(investments: List[Investment]) -> Dict[str, dict]:
    """Return investment dollars by US state.

    Returns
    -------
    Dict mapping state_code → {'count', 'invested', 'pct_of_portfolio'}.
    """
    total_invested = sum(inv.investment_amount for inv in investments)
    by_state: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "invested": 0.0})

    for inv in investments:
        by_state[inv.state]["count"] += 1
        by_state[inv.state]["invested"] += inv.investment_amount

    return {
        state: {
            "count": data["count"],
            "invested": data["invested"],
            "pct_of_portfolio": data["invested"] / total_invested if total_invested > 0 else 0.0,
        }
        for state, data in sorted(by_state.items(), key=lambda x: -x[1]["invested"])
    }


def top_naics(investments: List[Investment], n: int = 5) -> List[Tuple[str, str, float]]:
    """Return the top-n NAICS sectors by invested dollars.

    Returns
    -------
    List of (naics_2digit, sector_name, invested_dollars) sorted descending.
    """
    breakdown = sector_breakdown(investments)
    ranked = sorted(breakdown.items(), key=lambda x: -x[1]["invested"])
    return [(code, data["sector_name"], data["invested"]) for code, data in ranked[:n]]
