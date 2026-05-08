"""
Fund-level return metrics: IRR, TVPI, DPI, RVPI, called/distributed capital, NAV.
"""
from __future__ import annotations

from typing import List, Optional

from sbictracker.data.schema import Investment


# ---------------------------------------------------------------------------
# Capital account helpers
# ---------------------------------------------------------------------------

def called_capital(investments: List[Investment]) -> float:
    """Total invested capital (original cost basis across all investments)."""
    return sum(inv.investment_amount for inv in investments)


def distributed_capital(investments: List[Investment]) -> float:
    """Total exit proceeds received (realized investments only)."""
    return sum(inv.exit_proceeds for inv in investments if inv.is_realized)


def nav(investments: List[Investment]) -> float:
    """Net asset value of unrealized positions at cost net of write-offs."""
    return sum(inv.net_cost_basis for inv in investments if not inv.is_realized)


def total_value(investments: List[Investment]) -> float:
    """Total value = distributed capital + NAV of unrealized positions."""
    return distributed_capital(investments) + nav(investments)


# ---------------------------------------------------------------------------
# Multiple metrics
# ---------------------------------------------------------------------------

def tvpi(investments: List[Investment]) -> float:
    """Total Value to Paid-In capital.

    TVPI = (distributed + NAV) / called capital
    """
    cc = called_capital(investments)
    if cc == 0:
        return 0.0
    return total_value(investments) / cc


def dpi(investments: List[Investment]) -> float:
    """Distributions to Paid-In capital (realized multiple).

    DPI = distributed capital / called capital
    """
    cc = called_capital(investments)
    if cc == 0:
        return 0.0
    return distributed_capital(investments) / cc


def rvpi(investments: List[Investment]) -> float:
    """Residual Value to Paid-In capital (unrealized multiple).

    RVPI = NAV / called capital
    """
    cc = called_capital(investments)
    if cc == 0:
        return 0.0
    return nav(investments) / cc


# ---------------------------------------------------------------------------
# IRR
# ---------------------------------------------------------------------------

def _npv(rate: float, cash_flows: List[float]) -> float:
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))


def _npv_deriv(rate: float, cash_flows: List[float]) -> float:
    return sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))


def irr(
    cash_flows: List[float],
    max_iter: int = 1000,
    tol: float = 1e-8,
    initial_guess: float = 0.10,
) -> float:
    """Compute fund IRR via Newton-Raphson.

    Parameters
    ----------
    cash_flows:
        Annual cash flows from LP perspective: negative = capital called,
        positive = distributions.  Year 0 is the first call.
    initial_guess:
        Starting rate for Newton-Raphson (default 10%).
    """
    if not cash_flows:
        raise ValueError("cash_flows must not be empty")
    has_pos = any(cf > 0 for cf in cash_flows)
    has_neg = any(cf < 0 for cf in cash_flows)
    if not (has_pos and has_neg):
        raise ValueError("cash_flows must contain both positive and negative values")

    rate = initial_guess
    for _ in range(max_iter):
        npv_val = _npv(rate, cash_flows)
        deriv = _npv_deriv(rate, cash_flows)
        if abs(deriv) < 1e-12:
            break
        new_rate = rate - npv_val / deriv
        if abs(new_rate - rate) < tol:
            return new_rate
        rate = new_rate
    return rate
