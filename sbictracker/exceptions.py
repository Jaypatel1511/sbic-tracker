"""
Typed exception hierarchy for sbic-tracker (added 0.2.0).

Through 0.1.0, ``load_from_sba_url()`` could not return live SBA data by ANY
path — the CKAN ``resource_id`` in its URL was a hand-typed placeholder that
404s, the request body was wrapped in ``except Exception: pass``, and the
success branch was an unimplemented ``return []``. Every caller therefore
received ``load_sample_licensees()``: invented fund names with invented dates,
NAICS codes and dollar amounts, presented as SBA program data, with fund-level
IRR / TVPI / DPI computed on top of it.

A fabricated *positive* is more dangerous than a fabricated negative: an empty
result is visibly unhelpful, while a fully populated portfolio of plausible
fake companies reads as a successful load. These exceptions replace that
silence.

    SBICTrackerError
    └─ SBADownloadError   # live SBA acquisition failed or is not implemented

Downstream code can catch at either level: ``except SBICTrackerError`` for
anything this package raises, or the specific leaf.

EVERY exception class defined in this package subclasses SBICTrackerError.
The package's other 9 raise sites are stdlib ValueError argument validation and
are deliberately NOT in this tree — they signal a caller's programming error
rather than a data-acquisition failure, and none is reachable from a load:

    data/schema.py:85,87,89      SBICLicensee.__post_init__ field validation
    data/schema.py:138,140,142   Investment.__post_init__ field validation
    fund/metrics.py:101,105      irr() cash-flow argument checks
    fund/cohort.py:66            peer_quartile_ranking() empty-peer check
"""


class SBICTrackerError(Exception):
    """Base class for every error raised by sbic-tracker."""


class SBADownloadError(SBICTrackerError):
    """Live SBA SBIC licensee data could not be obtained.

    In 0.2.0 this is raised unconditionally by ``load_from_sba_url()``: live SBA
    loading is not implemented and the configured endpoint is invalid. It is
    raised INSTEAD OF returning sample data, which is what 0.1.0 did silently.
    Use ``load_sample_licensees()`` if you explicitly want the demo set."""


__all__ = [
    "SBICTrackerError",
    "SBADownloadError",
]
