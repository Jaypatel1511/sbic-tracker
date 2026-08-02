"""
sbic-tracker — SBIC Investment Portfolio Analyzer
==================================================
Fund-level metrics (IRR, TVPI, DPI, RVPI), licensee tracking,
vintage cohort analysis, and sector/state concentration.

UNMAINTAINED (0.2.0). Live SBA data loading is NOT implemented and none is
planned: ``load_from_sba_url()`` raises SBADownloadError. The package returns
sample data only when explicitly requested via ``load_sample_licensees()`` /
``load_sample_investments()``, whose records are stamped
``data_source == "sample"``. The financial functions are real arithmetic and
work on any data you supply; the data layer has no real source. See the README.
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
from sbictracker.exceptions import SBICTrackerError, SBADownloadError

__version__ = "0.2.0"
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
    # Exceptions
    "SBICTrackerError",
    "SBADownloadError",
]
