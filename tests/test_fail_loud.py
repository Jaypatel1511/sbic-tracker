"""Fail-loud contract (0.2.0).

Through 0.1.0, ``load_from_sba_url()`` could not return live data by any path —
fake CKAN resource_id, ``except Exception: pass``, unimplemented success
branch — and every caller silently received ``load_sample_licensees()``:
invented companies with invented dollar amounts, presented as SBA program data.
No test drove the function at all.

These drive the real public entry point and pin that it raises a typed error
and never yields sample data.
"""
import pytest

from sbictracker import load_from_sba_url, load_sample_licensees
from sbictracker.exceptions import SBICTrackerError, SBADownloadError
from sbictracker.data import loader


def test_load_from_sba_url_raises():
    with pytest.raises(SBADownloadError):
        load_from_sba_url()


def test_error_is_catchable_at_package_base():
    """A consumer catching the single package base catches this."""
    with pytest.raises(SBICTrackerError):
        load_from_sba_url()


def test_error_message_is_accurate_and_specific():
    """A typed error with a misleading message misdirects as badly as silence.

    The message must say what is actually wrong: not implemented, AND the
    configured endpoint is invalid.
    """
    with pytest.raises(SBADownloadError) as exc:
        load_from_sba_url()
    msg = str(exc.value)
    assert "not implemented" in msg
    assert "data.sba.gov" in msg, "the error must name the configured endpoint"
    assert "404" in msg
    assert "load_sample_licensees" in msg, "point the caller at the honest alternative"


def test_load_from_sba_url_never_returns_sample_data():
    """The 0.1.0 behavior, stated as the thing that must not happen."""
    try:
        result = load_from_sba_url()
    except SBADownloadError:
        return
    pytest.fail(
        f"load_from_sba_url() returned {type(result).__name__} instead of raising; "
        f"equal to sample data: {result == load_sample_licensees()}"
    )


def test_no_network_request_is_attempted(monkeypatch):
    """The endpoint is known-invalid, so nothing should be requested. A stub
    that explodes on any urlopen proves the swallow-and-fall-through body is
    gone rather than merely reordered."""
    import urllib.request

    def _boom(*a, **k):
        raise AssertionError("load_from_sba_url() must not attempt a request")

    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    with pytest.raises(SBADownloadError):
        load_from_sba_url()


def test_no_exception_swallowing_remains_in_loader():
    """`except Exception: pass` was the mechanism. Assert no swallowing handler
    exists in this module's AST — not just that the current code path avoids
    one. Checked structurally rather than by string match so the docstrings
    that *describe* the old bug don't trip it.
    """
    import ast
    import inspect

    tree = ast.parse(inspect.getsource(loader))
    swallowers = [
        h for h in ast.walk(tree)
        if isinstance(h, ast.ExceptHandler)
        and all(isinstance(stmt, (ast.Pass, ast.Expr)) for stmt in h.body)
    ]
    assert not swallowers, (
        f"handler(s) at line(s) {[h.lineno for h in swallowers]} swallow without "
        f"re-raising"
    )


# ── Provenance ───────────────────────────────────────────────────────────────

def test_sample_licensees_are_marked_sample():
    licensees = load_sample_licensees()
    assert len(licensees) == 10
    assert all(l.data_source == "sample" for l in licensees)


def test_sample_investments_are_marked_sample():
    from sbictracker import load_sample_investments

    investments = load_sample_investments()
    assert len(investments) == 20
    assert all(i.data_source == "sample" for i in investments)


def test_user_constructed_records_are_not_marked_sample(inv_realized, licensee_active):
    """A record the caller built is 'user', never falsely stamped 'sample' —
    the marker has to distinguish, not decorate."""
    assert inv_realized.data_source == "user"
    assert licensee_active.data_source == "user"
