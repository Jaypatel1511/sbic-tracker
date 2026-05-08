"""Shared fixtures for sbic-tracker tests."""
import pytest
from datetime import date
from sbictracker.data.schema import Investment, SBICLicensee
from sbictracker.data.loader import load_sample_investments, load_sample_licensees
from sbictracker.portfolio.tracker import SBICPortfolio


@pytest.fixture
def licensee_active():
    return SBICLicensee(
        license_number="04/73-0001",
        fund_name="Apex Growth Fund I",
        fund_manager="Apex Capital",
        license_date=date(2015, 3, 12),
        license_status="active",
        license_type="Standard",
        total_capital=150_000_000,
        sba_leverage=100_000_000,
        private_capital=50_000_000,
    )


@pytest.fixture
def inv_realized():
    """Investment with a profitable exit."""
    return Investment(
        investee_company="TechStart Inc.",
        investment_date=date(2018, 3, 1),
        investment_amount=5_000_000,
        naics_code="541512",
        state="CA",
        exit_date=date(2022, 6, 1),
        exit_proceeds=12_000_000,
        write_off_amount=0,
        instrument_type="equity",
    )


@pytest.fixture
def inv_unrealized():
    """Unrealized investment, no write-off."""
    return Investment(
        investee_company="MediSol LLC",
        investment_date=date(2019, 7, 15),
        investment_amount=3_000_000,
        naics_code="621111",
        state="TX",
        instrument_type="debt",
    )


@pytest.fixture
def inv_written_off():
    """Unrealized investment with partial write-off."""
    return Investment(
        investee_company="FailCo LLC",
        investment_date=date(2020, 1, 1),
        investment_amount=2_000_000,
        naics_code="452990",
        state="OH",
        write_off_amount=2_000_000,
        instrument_type="equity",
    )


@pytest.fixture
def sample_portfolio(inv_realized, inv_unrealized):
    p = SBICPortfolio("Test Fund")
    p.add(inv_realized)
    p.add(inv_unrealized)
    return p


@pytest.fixture
def full_investments():
    return load_sample_investments()


@pytest.fixture
def full_licensees():
    return load_sample_licensees()
