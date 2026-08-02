# Changelog

All notable changes to sbic-tracker are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **If you used 0.1.0, read the 0.1.0 entry before trusting anything it told
> you.** 0.1.0 served invented portfolio companies as SBA program data, and
> computed fund-level IRR / TVPI / DPI on top of them. Any conclusion drawn
> from it needs rechecking.

---

## [0.2.0] — unreleased

Prepared but **not published**. Version 0.2.0 is set in `pyproject.toml` and
`setup.py`; no tag has been pushed and no artifact uploaded. `dist/` still
holds 0.1.0 artifacts and is cleaned before any build.

A "fail loud" release, and the last functional change planned. The package is
now marked **`Development Status :: 7 - Inactive`**: there is no live SBA data
source and none is planned. What 0.2.0 fixes is that it no longer pretends to
have one.

### Removed

- **The silent fabrication path in `load_from_sba_url()`.** It could never
  return live data by any route: the CKAN `resource_id` was a hand-typed
  placeholder that 404s, the request body was wrapped in
  `except Exception: pass`, and the success branch was literally
  `return []  # would parse live records here`. Every caller silently received
  `load_sample_licensees()` instead. The swallow and the stub branch are gone.
- **The example notebook.** 8 of its 10 code cells raised, against an API this
  package never had — `LICENSE_TYPES.keys()` on a list; `SBICPortfolio.count()`
  / `.total_invested` / `.filter_state` / `.filter_sector` (the real names are
  `__len__`, `summary_stats`, `filter_by_state`, `filter_by_sector`);
  `irr(investments)` where `irr` takes `List[float]`; and
  `vintage_year_analysis` / `sector_breakdown` / `state_breakdown` treated as
  returning DataFrames when they return `dict`.

  Deleted rather than repaired, deliberately. This package is Inactive with no
  live data source planned; repairing it meant rewriting all ten cells against
  an API it never targeted, and the README Quickstart already covers every
  working feature and is now verified executable. Nothing referenced the file.
  (Contrast oz-tracker, whose notebook was rewritten instead: that package is
  maintained, restoration is planned, and most of its cells already worked.)

### Changed — BREAKING

- **`load_from_sba_url()` raises `SBADownloadError` unconditionally.** No
  request is attempted. The message names the invalid endpoint and points at
  `load_sample_licensees()` for callers who want the demo data explicitly.
- The package is marked unmaintained in the `pyproject.toml` / `setup.py`
  descriptions, the README, and the `Development Status :: 7 - Inactive`
  classifier.

### Added

- Typed exceptions: `SBICTrackerError` (base) and `SBADownloadError`.
- **Provenance markers.** Every `SBICLicensee` and `Investment` carries
  `data_source` — `"sample"` from the demo loaders, `"user"` for
  caller-constructed records. There is no longer a way to hold one of these
  objects and not know where it came from.
- `load_sample_licensees()` / `load_sample_investments()` remain, as explicitly
  named sample sources rather than an invisible fallback.

### Fixed

- **The README shipped a fabricated output block.** The documented
  `portfolio.summary()` output had all seven figures wrong: it claimed
  10 realized / 10 unrealized, $78,150,000 called, $85,410,000 distributed,
  $30,550,000 NAV, 1.48x TVPI, 1.09x DPI, 0.39x RVPI. The shipped sample data
  actually produces 9 / 11, $83,150,000, $72,410,000, $34,550,000, 1.29x,
  0.87x, 0.42x. A release whose thesis is "this package no longer prints
  invented numbers" cannot ship a README that prints invented numbers. Replaced
  with real executed output, asserted against the installed wheel rather than
  pasted.
- Every other README claim was then swept by execution rather than by reading:
  the Quickstart runs verbatim end to end; "10 licensees + 20 investments"
  checks out; `dependencies = []` checks out; every record is stamped
  `data_source`; and all 14 documented exports, 9 `SBICPortfolio` methods, 7
  `Investment` properties, 3 `SBICLicensee` properties and 4 module-level
  fund-metric functions exist as documented.
- **The sdist shipped a suite that cannot run.** setuptools' default `test*.py`
  glob omitted `tests/conftest.py`, so the extracted sdist produced 26 passed /
  57 errors. Fixed via `MANIFEST.in`; the extracted sdist now runs 83/83.
- The wheel no longer carries a top-level `tests` package.

### Testing

- 83 tests, up from 74 at 0.1.0, and 83 again with sockets blocked (the blocker
  independently proven to block a real request).
- `tests/test_fail_loud.py` drives the real entry point and asserts the typed
  raise, the message content, that **no request is attempted**, that no
  swallowing handler remains — checked structurally via AST, not by reading —
  and that provenance markers are present.

### Known issues, unchanged in 0.2.0

- **There is no live SBA data path, and none is planned.** Everything this
  package returns comes from the sample loaders and is labelled as such.

---

## [0.1.0] — 2026-05-08

Initial release. **Do not use.** Recorded here because a user who drew
conclusions from it needs to know what it actually did.

- `load_from_sba_url()` presented **invented portfolio companies with invented
  dollar amounts as SBA program data.** It could not reach a live source by any
  path — placeholder `resource_id`, `except Exception: pass` around the
  request, and a stub success branch returning `[]` — so every caller silently
  got `load_sample_licensees()` with nothing to distinguish it from real data.
- Fund-level **IRR, TVPI and DPI were computed on top of those invented
  records** and returned as ordinary results.
- The README's documented `portfolio.summary()` output was fabricated: all
  seven headline figures differed from what the shipped code produces.
- The example notebook did not run — 8 of its 10 code cells raised against an
  API the package never had.
- 74 tests, passing. They did not exercise the fabrication path.

[0.2.0]: https://github.com/Jaypatel1511/sbic-tracker
[0.1.0]: https://github.com/Jaypatel1511/sbic-tracker
