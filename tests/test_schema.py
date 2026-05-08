"""Tests for SBICLicensee and Investment dataclasses."""
import pytest
from datetime import date
from sbictracker.data.schema import Investment, SBICLicensee


class TestSBICLicensee:
    def test_valid_licensee(self, licensee_active):
        assert licensee_active.fund_name == "Apex Growth Fund I"

    def test_leverage_ratio(self, licensee_active):
        assert licensee_active.leverage_ratio == pytest.approx(2.0)

    def test_vintage_year(self, licensee_active):
        assert licensee_active.vintage_year == 2015

    def test_invalid_status_raises(self):
        with pytest.raises(ValueError):
            SBICLicensee("X", "F", "M", date(2020, 1, 1),
                         "invalid_status", "Standard", 10e6, 6e6, 4e6)

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            SBICLicensee("X", "F", "M", date(2020, 1, 1),
                         "active", "Unknown", 10e6, 6e6, 4e6)

    def test_negative_sba_leverage_raises(self):
        with pytest.raises(ValueError):
            SBICLicensee("X", "F", "M", date(2020, 1, 1),
                         "active", "Standard", 10e6, -1e6, 4e6)


class TestInvestment:
    def test_realized_investment(self, inv_realized):
        assert inv_realized.is_realized is True
        assert inv_realized.realized_value == 12_000_000

    def test_unrealized_investment(self, inv_unrealized):
        assert inv_unrealized.is_realized is False
        assert inv_unrealized.realized_value == 0

    def test_moic_realized(self, inv_realized):
        assert inv_realized.moic == pytest.approx(2.4)

    def test_moic_unrealized(self, inv_unrealized):
        assert inv_unrealized.moic is None

    def test_naics_sector(self, inv_realized):
        # 54 = Professional & Technical Services
        assert "Professional" in inv_realized.naics_sector

    def test_net_cost_basis_no_writeoff(self, inv_unrealized):
        assert inv_unrealized.net_cost_basis == pytest.approx(3_000_000)

    def test_net_cost_basis_with_writeoff(self, inv_written_off):
        assert inv_written_off.net_cost_basis == pytest.approx(0)

    def test_vintage_year(self, inv_realized):
        assert inv_realized.vintage_year == 2018

    def test_invalid_instrument_raises(self):
        with pytest.raises(ValueError):
            Investment("Co", date(2020, 1, 1), 1_000_000,
                       "541512", "CA", instrument_type="convertible_note")

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError):
            Investment("Co", date(2020, 1, 1), 0, "541512", "CA")

    def test_writeoff_exceeds_amount_raises(self):
        with pytest.raises(ValueError):
            Investment("Co", date(2020, 1, 1), 1_000_000, "541512", "CA",
                       write_off_amount=1_500_000)
