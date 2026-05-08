"""
SBICPortfolio: add/remove investments, filter by sector/state, summary stats.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from sbictracker.data.schema import Investment, NAICS_SECTORS
from sbictracker.fund.metrics import (
    called_capital,
    distributed_capital,
    dpi,
    nav,
    rvpi,
    total_value,
    tvpi,
)


class SBICPortfolio:
    """Container for a set of SBIC investments with query and summary methods.

    Parameters
    ----------
    name:
        Portfolio or fund name.
    """

    def __init__(self, name: str = "SBIC Portfolio") -> None:
        self.name = name
        self._investments: List[Investment] = []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, investment: Investment) -> None:
        """Add a single investment to the portfolio."""
        self._investments.append(investment)

    def add_many(self, investments: List[Investment]) -> None:
        """Add multiple investments at once."""
        self._investments.extend(investments)

    def remove(self, investee_company: str) -> bool:
        """Remove the first investment matching the company name.

        Returns True if an investment was removed, False if not found.
        """
        for i, inv in enumerate(self._investments):
            if inv.investee_company == investee_company:
                self._investments.pop(i)
                return True
        return False

    # ------------------------------------------------------------------
    # Access
    # ------------------------------------------------------------------

    @property
    def investments(self) -> List[Investment]:
        return list(self._investments)

    def __len__(self) -> int:
        return len(self._investments)

    def get(self, investee_company: str) -> Optional[Investment]:
        """Return the first investment matching the company name, or None."""
        for inv in self._investments:
            if inv.investee_company == investee_company:
                return inv
        return None

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter_by_sector(self, naics_prefix: str) -> List[Investment]:
        """Return investments whose NAICS code starts with naics_prefix."""
        return [inv for inv in self._investments if inv.naics_code.startswith(naics_prefix)]

    def filter_by_state(self, state: str) -> List[Investment]:
        """Return investments in a given US state (2-letter code)."""
        return [inv for inv in self._investments if inv.state.upper() == state.upper()]

    def filter_by_instrument(self, instrument_type: str) -> List[Investment]:
        """Return investments of a specific instrument type."""
        return [inv for inv in self._investments if inv.instrument_type == instrument_type]

    def filter_realized(self) -> List[Investment]:
        return [inv for inv in self._investments if inv.is_realized]

    def filter_unrealized(self) -> List[Investment]:
        return [inv for inv in self._investments if not inv.is_realized]

    # ------------------------------------------------------------------
    # Aggregate metrics
    # ------------------------------------------------------------------

    def summary_stats(self) -> Dict[str, object]:
        """Return a dict of portfolio-level metrics."""
        invs = self._investments
        return {
            "portfolio_name": self.name,
            "investment_count": len(invs),
            "realized_count": len(self.filter_realized()),
            "unrealized_count": len(self.filter_unrealized()),
            "called_capital": called_capital(invs),
            "distributed_capital": distributed_capital(invs),
            "nav": nav(invs),
            "total_value": total_value(invs),
            "tvpi": round(tvpi(invs), 3),
            "dpi": round(dpi(invs), 3),
            "rvpi": round(rvpi(invs), 3),
        }

    def summary(self) -> str:
        s = self.summary_stats()
        lines = [
            f"=== {s['portfolio_name']} ===",
            f"  Investments      : {s['investment_count']} "
            f"({s['realized_count']} realized / {s['unrealized_count']} unrealized)",
            f"  Called capital   : ${s['called_capital']:,.0f}",
            f"  Distributed      : ${s['distributed_capital']:,.0f}",
            f"  NAV (unrealized) : ${s['nav']:,.0f}",
            f"  TVPI             : {s['tvpi']:.2f}x",
            f"  DPI              : {s['dpi']:.2f}x",
            f"  RVPI             : {s['rvpi']:.2f}x",
        ]
        return "\n".join(lines)
