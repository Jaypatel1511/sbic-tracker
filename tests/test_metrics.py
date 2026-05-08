"""Tests for fund-level return metrics."""
import pytest
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


class TestCapitalAccounts:
    def test_called_capital(self, inv_realized, inv_unrealized):
        assert called_capital([inv_realized, inv_unrealized]) == pytest.approx(8_000_000)

    def test_distributed_capital(self, inv_realized, inv_unrealized):
        assert distributed_capital([inv_realized, inv_unrealized]) == pytest.approx(12_000_000)

    def test_nav_unrealized_only(self, inv_unrealized):
        assert nav([inv_unrealized]) == pytest.approx(3_000_000)

    def test_nav_realized_excluded(self, inv_realized):
        assert nav([inv_realized]) == pytest.approx(0)

    def test_nav_with_writeoff(self, inv_written_off):
        assert nav([inv_written_off]) == pytest.approx(0)

    def test_total_value(self, inv_realized, inv_unrealized):
        # realized: 12M + unrealized NAV: 3M = 15M
        assert total_value([inv_realized, inv_unrealized]) == pytest.approx(15_000_000)


class TestMultiples:
    def test_tvpi(self, inv_realized, inv_unrealized):
        # total = 15M, called = 8M → 1.875x
        assert tvpi([inv_realized, inv_unrealized]) == pytest.approx(1.875)

    def test_dpi(self, inv_realized, inv_unrealized):
        # distributed = 12M, called = 8M → 1.5x
        assert dpi([inv_realized, inv_unrealized]) == pytest.approx(1.5)

    def test_rvpi(self, inv_realized, inv_unrealized):
        # NAV = 3M, called = 8M → 0.375x
        assert rvpi([inv_realized, inv_unrealized]) == pytest.approx(0.375)

    def test_tvpi_equals_dpi_plus_rvpi(self, inv_realized, inv_unrealized):
        invs = [inv_realized, inv_unrealized]
        assert tvpi(invs) == pytest.approx(dpi(invs) + rvpi(invs))

    def test_zero_called_capital(self):
        # empty portfolio → 0.0
        assert tvpi([]) == pytest.approx(0.0)

    def test_all_written_off(self, inv_written_off):
        assert tvpi([inv_written_off]) == pytest.approx(0.0)


class TestIRR:
    def test_known_irr(self):
        flows = [-1000, 1100]
        assert irr(flows) == pytest.approx(0.10, abs=1e-6)

    def test_irr_annuity(self):
        rate = 0.08
        n = 5
        payment = 1000 * rate / (1 - (1 + rate) ** -n)
        flows = [-1000] + [payment] * n
        assert irr(flows) == pytest.approx(rate, abs=1e-5)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            irr([])

    def test_no_sign_change_raises(self):
        with pytest.raises(ValueError):
            irr([100, 200, 300])

    def test_positive_irr_good_deal(self, inv_realized, inv_unrealized):
        flows = [-8_000_000, 0, 0, 0, 12_000_000, 3_000_000]
        result = irr(flows)
        assert result > 0
