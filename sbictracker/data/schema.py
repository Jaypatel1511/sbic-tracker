"""
SBIC data structures, constants, and field definitions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Literal, Optional

# ---------------------------------------------------------------------------
# NAICS sector mapping (2-digit codes → sector names)
# ---------------------------------------------------------------------------
NAICS_SECTORS: Dict[str, str] = {
    "11": "Agriculture, Forestry, Fishing",
    "21": "Mining, Quarrying, Oil & Gas",
    "22": "Utilities",
    "23": "Construction",
    "31": "Manufacturing — Food & Textile",
    "32": "Manufacturing — Paper & Chemical",
    "33": "Manufacturing — Metal & Machinery",
    "42": "Wholesale Trade",
    "44": "Retail Trade — Motor & Furniture",
    "45": "Retail Trade — General",
    "48": "Transportation & Warehousing",
    "51": "Information",
    "52": "Finance & Insurance",
    "53": "Real Estate & Rental",
    "54": "Professional & Technical Services",
    "55": "Management of Companies",
    "56": "Administrative & Support Services",
    "61": "Educational Services",
    "62": "Health Care & Social Assistance",
    "71": "Arts, Entertainment & Recreation",
    "72": "Accommodation & Food Services",
    "81": "Other Services",
    "92": "Public Administration",
}

LICENSE_TYPES: List[str] = ["Standard", "Energy Saving", "Impact"]
LICENSE_STATUSES: List[str] = ["active", "surrendered", "wound_down"]
INVESTMENT_INSTRUMENTS: List[str] = ["debt", "equity", "mezzanine"]

# SBA leverage ratio: SBIC can typically draw 2x private capital in SBA debentures
MAX_SBA_LEVERAGE_RATIO: float = 2.0
SBA_DEBENTURE_RATE_2024: float = 0.0618  # approximate 10-year debenture rate


@dataclass
class SBICLicensee:
    """An SBA-licensed Small Business Investment Company.

    Parameters
    ----------
    license_number:
        SBA-assigned license number (e.g. '09/79-0641').
    fund_name:
        Fund name as registered with the SBA.
    fund_manager:
        Managing firm or GP name.
    license_date:
        Date the SBA granted the license.
    license_status:
        One of 'active', 'surrendered', 'wound_down'.
    license_type:
        'Standard', 'Energy Saving', or 'Impact'.
    total_capital:
        Total fund capital (private + SBA leverage) in dollars.
    sba_leverage:
        SBA debentures / participating securities drawn in dollars.
    private_capital:
        LP / institutional capital committed in dollars.
    """
    license_number: str
    fund_name: str
    fund_manager: str
    license_date: date
    license_status: Literal["active", "surrendered", "wound_down"]
    license_type: Literal["Standard", "Energy Saving", "Impact"]
    total_capital: float
    sba_leverage: float
    private_capital: float

    def __post_init__(self) -> None:
        if self.license_status not in LICENSE_STATUSES:
            raise ValueError(f"license_status must be one of {LICENSE_STATUSES}")
        if self.license_type not in LICENSE_TYPES:
            raise ValueError(f"license_type must be one of {LICENSE_TYPES}")
        if self.sba_leverage < 0 or self.private_capital < 0:
            raise ValueError("sba_leverage and private_capital must be non-negative")

    @property
    def leverage_ratio(self) -> float:
        """SBA leverage as multiple of private capital."""
        return self.sba_leverage / self.private_capital if self.private_capital > 0 else 0.0

    @property
    def vintage_year(self) -> int:
        return self.license_date.year


@dataclass
class Investment:
    """A single SBIC portfolio investment.

    Parameters
    ----------
    investee_company:
        Name of the portfolio company.
    investment_date:
        Date the investment was made.
    investment_amount:
        Original cost basis in dollars.
    naics_code:
        6-digit NAICS code of the portfolio company.
    state:
        2-letter US state code of the portfolio company.
    exit_date:
        Date of exit (None if still held).
    exit_proceeds:
        Total proceeds received at exit (0 if written off or still held).
    write_off_amount:
        Portion of cost basis written off (0 if not written off).
    instrument_type:
        'debt', 'equity', or 'mezzanine'.
    """
    investee_company: str
    investment_date: date
    investment_amount: float
    naics_code: str
    state: str
    exit_date: Optional[date] = None
    exit_proceeds: float = 0.0
    write_off_amount: float = 0.0
    instrument_type: Literal["debt", "equity", "mezzanine"] = "debt"

    def __post_init__(self) -> None:
        if self.instrument_type not in INVESTMENT_INSTRUMENTS:
            raise ValueError(f"instrument_type must be one of {INVESTMENT_INSTRUMENTS}")
        if self.investment_amount <= 0:
            raise ValueError("investment_amount must be positive")
        if self.write_off_amount < 0 or self.write_off_amount > self.investment_amount:
            raise ValueError("write_off_amount must be in [0, investment_amount]")

    @property
    def naics_sector(self) -> str:
        """Return the 2-digit sector label for this investment."""
        code2 = self.naics_code[:2]
        return NAICS_SECTORS.get(code2, "Unknown")

    @property
    def is_realized(self) -> bool:
        return self.exit_date is not None

    @property
    def realized_value(self) -> float:
        return self.exit_proceeds if self.is_realized else 0.0

    @property
    def net_cost_basis(self) -> float:
        """Cost basis net of write-offs."""
        return self.investment_amount - self.write_off_amount

    @property
    def moic(self) -> Optional[float]:
        """Multiple on invested capital (realized only)."""
        if self.is_realized and self.investment_amount > 0:
            return self.exit_proceeds / self.investment_amount
        return None

    @property
    def vintage_year(self) -> int:
        return self.investment_date.year
