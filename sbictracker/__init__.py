"""
sbic-tracker — SBIC Investment Portfolio Analyzer
==================================================
Fund-level metrics (IRR, TVPI, DPI, RVPI), licensee tracking,
vintage cohort analysis, and sector/state concentration.
"""
from sbictracker.data.schema import (
    INVESTMENT_INSTRUMENTS,
    LICENSE_STATUSES,
    LICENSE_TYPES,
    NAICS_SECTORS,
    Investment,
    SBICLicensee,
)
from sbictracker.data.loader import (
    load_from_sba_url,
    load_sample_investments,
    load_sample_licensees,
)
from sbictracker.fund.metrics import (
    called_capital,
    distributed_capital,
    dpi,
    irr,
    nav,
    rvpi,
    total_value,
    tvpi,
)
from sbictracker.fund.cohort import (
    peer_quartile_ranking,
    vintage_year_analysis,
)
from sbictracker.portfolio.tracker import SBICPortfolio
from sbictracker.analysis.sector import (
    sector_breakdown,
    state_breakdown,
    top_naics,
)

__version__ = "0.1.0"
__author__ = "Jay Patel"

__all__ = [
    # Data
    "SBICLicensee",
    "Investment",
    "NAICS_SECTORS",
    "LICENSE_TYPES",
    "LICENSE_STATUSES",
    "INVESTMENT_INSTRUMENTS",
    # Loaders
    "load_sample_licensees",
    "load_sample_investments",
    "load_from_sba_url",
    # Fund metrics
    "irr",
    "tvpi",
    "dpi",
    "rvpi",
    "called_capital",
    "distributed_capital",
    "nav",
    "total_value",
    # Cohort
    "vintage_year_analysis",
    "peer_quartile_ranking",
    # Portfolio
    "SBICPortfolio",
    # Analysis
    "sector_breakdown",
    "state_breakdown",
    "top_naics",
]
