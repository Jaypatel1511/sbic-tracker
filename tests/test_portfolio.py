"""Tests for SBICPortfolio tracker."""
import pytest
from sbictracker.portfolio.tracker import SBICPortfolio
from sbictracker.data.loader import load_sample_investments


class TestSBICPortfolio:
    def test_add_investment(self, inv_realized):
        p = SBICPortfolio()
        p.add(inv_realized)
        assert len(p) == 1

    def test_add_many(self, inv_realized, inv_unrealized):
        p = SBICPortfolio()
        p.add_many([inv_realized, inv_unrealized])
        assert len(p) == 2

    def test_remove_existing(self, sample_portfolio):
        removed = sample_portfolio.remove("TechStart Inc.")
        assert removed is True
        assert len(sample_portfolio) == 1

    def test_remove_nonexistent(self, sample_portfolio):
        removed = sample_portfolio.remove("Nonexistent Corp")
        assert removed is False

    def test_get_investment(self, sample_portfolio):
        inv = sample_portfolio.get("TechStart Inc.")
        assert inv is not None
        assert inv.investment_amount == 5_000_000

    def test_get_missing(self, sample_portfolio):
        assert sample_portfolio.get("Ghost Co.") is None

    def test_filter_by_state(self, sample_portfolio):
        ca_investments = sample_portfolio.filter_by_state("CA")
        assert len(ca_investments) == 1
        assert ca_investments[0].investee_company == "TechStart Inc."

    def test_filter_by_sector(self, sample_portfolio):
        tech = sample_portfolio.filter_by_sector("54")
        assert len(tech) == 1

    def test_filter_by_instrument(self, sample_portfolio):
        equity_invs = sample_portfolio.filter_by_instrument("equity")
        assert len(equity_invs) == 1

    def test_filter_realized(self, sample_portfolio):
        realized = sample_portfolio.filter_realized()
        assert len(realized) == 1

    def test_filter_unrealized(self, sample_portfolio):
        unrealized = sample_portfolio.filter_unrealized()
        assert len(unrealized) == 1

    def test_summary_stats_keys(self, sample_portfolio):
        stats = sample_portfolio.summary_stats()
        for key in ["tvpi", "dpi", "rvpi", "called_capital", "nav"]:
            assert key in stats

    def test_summary_string(self, sample_portfolio):
        summary = sample_portfolio.summary()
        assert "Test Fund" in summary
        assert "TVPI" in summary

    def test_full_sample_portfolio(self):
        p = SBICPortfolio("Full Sample")
        p.add_many(load_sample_investments())
        assert len(p) == 20
        stats = p.summary_stats()
        assert stats["tvpi"] > 0
