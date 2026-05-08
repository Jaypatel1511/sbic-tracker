"""Tests for sector and geographic breakdown."""
import pytest
from sbictracker.analysis.sector import sector_breakdown, state_breakdown, top_naics


class TestSectorBreakdown:
    def test_returns_dict(self, full_investments):
        result = sector_breakdown(full_investments)
        assert isinstance(result, dict)

    def test_sector_keys_are_2digit(self, full_investments):
        result = sector_breakdown(full_investments)
        for key in result:
            assert len(key) == 2

    def test_pct_sums_to_one(self, full_investments):
        result = sector_breakdown(full_investments)
        total_pct = sum(v["pct_of_portfolio"] for v in result.values())
        assert total_pct == pytest.approx(1.0)

    def test_invested_totals_match(self, full_investments):
        result = sector_breakdown(full_investments)
        total_from_breakdown = sum(v["invested"] for v in result.values())
        total_from_invs = sum(inv.investment_amount for inv in full_investments)
        assert total_from_breakdown == pytest.approx(total_from_invs)

    def test_sector_name_present(self, full_investments):
        result = sector_breakdown(full_investments)
        for data in result.values():
            assert "sector_name" in data

    def test_single_investment(self, inv_realized):
        result = sector_breakdown([inv_realized])
        assert "54" in result
        assert result["54"]["pct_of_portfolio"] == pytest.approx(1.0)


class TestStateBreakdown:
    def test_returns_dict(self, full_investments):
        result = state_breakdown(full_investments)
        assert isinstance(result, dict)

    def test_pct_sums_to_one(self, full_investments):
        result = state_breakdown(full_investments)
        total_pct = sum(v["pct_of_portfolio"] for v in result.values())
        assert total_pct == pytest.approx(1.0)

    def test_ca_present(self, full_investments):
        result = state_breakdown(full_investments)
        assert "CA" in result

    def test_count_sums_to_total(self, full_investments):
        result = state_breakdown(full_investments)
        total_count = sum(v["count"] for v in result.values())
        assert total_count == len(full_investments)


class TestTopNAICS:
    def test_returns_list(self, full_investments):
        result = top_naics(full_investments, n=5)
        assert isinstance(result, list)

    def test_length_limited(self, full_investments):
        result = top_naics(full_investments, n=3)
        assert len(result) <= 3

    def test_sorted_descending(self, full_investments):
        result = top_naics(full_investments, n=5)
        invested_vals = [r[2] for r in result]
        assert invested_vals == sorted(invested_vals, reverse=True)

    def test_tuple_structure(self, full_investments):
        result = top_naics(full_investments, n=1)
        assert len(result[0]) == 3   # (code, name, amount)

    def test_sector_name_in_result(self, full_investments):
        result = top_naics(full_investments, n=5)
        for _, name, _ in result:
            assert isinstance(name, str)
            assert len(name) > 0
