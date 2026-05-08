"""Tests for vintage year analysis and peer quartile ranking."""
import pytest
from sbictracker.fund.cohort import peer_quartile_ranking, vintage_year_analysis


class TestVintageYearAnalysis:
    def test_returns_dict(self, full_investments):
        result = vintage_year_analysis(full_investments)
        assert isinstance(result, dict)

    def test_vintage_years_present(self, full_investments):
        result = vintage_year_analysis(full_investments)
        assert 2015 in result
        assert 2018 in result

    def test_cohort_count(self, full_investments):
        result = vintage_year_analysis(full_investments)
        total_count = sum(v["count"] for v in result.values())
        assert total_count == len(full_investments)

    def test_cohort_metrics_present(self, full_investments):
        result = vintage_year_analysis(full_investments)
        for yr, data in result.items():
            assert "tvpi" in data
            assert "dpi" in data
            assert "called_capital" in data

    def test_single_investment_cohort(self, inv_realized):
        result = vintage_year_analysis([inv_realized])
        assert 2018 in result
        assert result[2018]["count"] == 1
        assert result[2018]["dpi"] == pytest.approx(12_000_000 / 5_000_000)


class TestPeerQuartileRanking:
    def test_top_quartile(self):
        result = peer_quartile_ranking(2.5, [1.0, 1.2, 1.5, 1.8, 2.0])
        assert result["quartile"] == 1

    def test_bottom_quartile(self):
        result = peer_quartile_ranking(0.8, [1.0, 1.2, 1.5, 1.8, 2.0])
        assert result["quartile"] == 4

    def test_peer_count(self):
        peers = [1.0, 1.5, 2.0, 2.5]
        result = peer_quartile_ranking(1.8, peers)
        assert result["peer_count"] == 4

    def test_empty_peers_raises(self):
        with pytest.raises(ValueError):
            peer_quartile_ranking(1.5, [])

    def test_median_present(self):
        result = peer_quartile_ranking(1.5, [1.0, 2.0, 3.0])
        assert "peer_median" in result

    def test_percentile_range(self):
        result = peer_quartile_ranking(1.5, [1.0, 1.2, 1.4, 1.6, 1.8])
        assert 0 <= result["percentile"] <= 100
