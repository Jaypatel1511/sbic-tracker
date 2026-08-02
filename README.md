# sbic-tracker

[![PyPI version](https://badge.fury.io/py/sbic-tracker.svg)](https://badge.fury.io/py/sbic-tracker)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SBIC investment portfolio analyzer for Python.**

Model and analyze Small Business Investment Company (SBIC) portfolios: fund-level IRR, TVPI, DPI, RVPI, vintage-year cohort analysis, peer benchmarking, and sector/state concentration — all built on pure Python with no external dependencies.

---

## ⚠️ Unmaintained — and it has no live data source

**Read this before installing.**

- **This package is not currently maintained.** No live SBA data source is
  planned. It is published with the PyPI classifier
  `Development Status :: 7 - Inactive`.
- **Live SBA data loading is not implemented.** `load_from_sba_url()` raises
  `SBADownloadError`. There is no SBA data in this package and never was.
- **The package returns sample data only when you explicitly ask for it**, via
  `load_sample_licensees()` / `load_sample_investments()`.

### What 0.1.0 did

`load_from_sba_url()` claimed in its own docstring to load live SBA data. It
could not do so by any path: the CKAN `resource_id` in its URL was a hand-typed
placeholder that returns 404, the request was wrapped in
`except Exception: pass`, and the success branch was
`return []  # would parse live records here`. Every caller silently received
`load_sample_licensees()` — invented fund names, invented license dates,
invented dollar amounts — labelled as SBA program data. Fund-level IRR, TVPI and
DPI computed downstream were arithmetic on fiction.

A fabricated *positive* is worse than a fabricated negative: an empty result is
visibly unhelpful, whereas a fully populated portfolio of plausible fake
companies reads as a successful data load.

### What 0.2.0 does

```python
from sbictracker import load_from_sba_url, load_sample_licensees, SBADownloadError

load_from_sba_url()          # raises SBADownloadError, always. No request is made.

licensees = load_sample_licensees()          # demo data, explicitly
licensees[0].data_source                     # "sample"
```

Every `SBICLicensee` and `Investment` now carries a `data_source` marker —
`"sample"` for records from the demo loaders, `"user"` for records you construct
yourself. **Check it before reporting any figure derived from these records.**

### What still works

All of the financial machinery. `irr`, `tvpi`, `dpi`, `rvpi`,
`vintage_year_analysis`, `peer_quartile_ranking`, `sector_breakdown`,
`SBICPortfolio` — these are real, tested arithmetic that operate on whatever
`Investment` records you supply. If you have your own SBIC data, this package
will analyze it correctly. What it will not do is fetch that data for you.

---

## Why sbic-tracker?

SBICs deploy over $6 billion annually into U.S. small businesses through SBA-leveraged funds. Portfolio managers, fund-of-funds analysts, and SBA examiners need consistent, auditable metrics across heterogeneous portfolios. `sbic-tracker` provides typed Python data structures and financial functions that match SBA and LP reporting standards.

## Installation

```bash
pip install sbic-tracker
```

No external dependencies — pure Python 3.9+.

## Quickstart

```python
from datetime import date
from sbictracker import (
    SBICLicensee, Investment,
    SBICPortfolio,
    load_sample_investments, load_sample_licensees,
    irr, tvpi, dpi, rvpi,
    vintage_year_analysis, peer_quartile_ranking,
    sector_breakdown, state_breakdown, top_naics,
)

# Load sample data (or plug in your own).
# These are INVENTED companies with invented dollar amounts — every record is
# stamped data_source == "sample". There is no live SBA loader; see above.
licensees = load_sample_licensees()
investments = load_sample_investments()

# Build a portfolio
portfolio = SBICPortfolio("Apex Growth Fund I")
portfolio.add_many(investments)
print(portfolio.summary())
# === Apex Growth Fund I ===
#   Investments      : 20 (10 realized / 10 unrealized)
#   Called capital   : $78,150,000
#   Distributed      : $85,410,000
#   NAV (unrealized) : $30,550,000
#   TVPI             : 1.48x
#   DPI              : 1.09x
#   RVPI             : 0.39x

# IRR from custom cash flows
fund_flows = [-10_000_000, 0, 500_000, 2_000_000, 8_000_000, 5_000_000]
print(f"Fund IRR: {irr(fund_flows):.2%}")

# Vintage cohort analysis
cohorts = vintage_year_analysis(investments)
for yr, data in sorted(cohorts.items()):
    print(f"  {yr}: {data['count']} investments, TVPI {data['tvpi']:.2f}x")

# Peer quartile ranking
ranking = peer_quartile_ranking(fund_tvpi=1.8, peer_tvpis=[1.2, 1.4, 1.6, 1.9, 2.1])
print(f"Quartile: Q{ranking['quartile']}  ({ranking['percentile']}th percentile)")

# Sector concentration
top = top_naics(investments, n=3)
for code, name, invested in top:
    print(f"  NAICS {code} ({name}): ${invested:,.0f}")
```

## Key Features

| Feature | Detail |
|---|---|
| **IRR** | Newton-Raphson solver for arbitrary annual cash-flow vectors |
| **TVPI / DPI / RVPI** | Industry-standard multiples from first principles |
| **Write-off tracking** | Net cost basis automatically reflects partial/full write-offs |
| **Vintage cohort analysis** | Group and compare by investment year |
| **Peer quartile ranking** | Percentile and Q1–Q4 ranking vs a peer TVPI distribution |
| **SBICPortfolio** | Add/remove investments; filter by sector, state, or instrument type |
| **Sector/state breakdown** | NAICS 2-digit concentration with portfolio % weights |
| **Sample data** | 10 licensees + 20 investments for prototyping — invented, stamped `data_source == "sample"` |
| **Provenance markers** | Every record carries `data_source` (`"sample"` / `"user"`) |
| **~~SBA URL loader~~** | **Not implemented.** `load_from_sba_url()` raises `SBADownloadError`; there is no live SBA source |

## Use Cases

- **Fund managers** — Track called/distributed capital and compute NAV-based multiples for LP reporting.
- **SBA examiners** — Audit licensee leverage ratios and investment-level MOIC across the portfolio.
- **Fund-of-funds analysts** — Compare SBIC fund vintage cohorts and rank against peer TVPIs.
- **Policy researchers** — Analyze SBIC capital deployment by sector, state, and instrument type.
- **Limited partners** — Build DPI/RVPI waterfalls and sensitivity models in Python.

## API Reference

### Data Classes

```python
SBICLicensee(license_number, fund_name, fund_manager, license_date,
             license_status, license_type, total_capital, sba_leverage,
             private_capital, data_source="user")
  .leverage_ratio   # sba_leverage / private_capital
  .vintage_year
  .data_source      # "sample" | "user" — provenance, check before reporting

Investment(investee_company, investment_date, investment_amount, naics_code, state,
           exit_date, exit_proceeds, write_off_amount, instrument_type,
           data_source="user")
  .is_realized       # bool
  .data_source       # "sample" | "user"
  .realized_value    # exit_proceeds if realized, else 0
  .net_cost_basis    # amount - write_off_amount
  .moic              # exit_proceeds / amount (realized only)
  .naics_sector      # human-readable sector name
  .vintage_year
```

### Fund Metrics

```python
irr(cash_flows)                   # Newton-Raphson IRR
tvpi(investments)                 # (distributed + NAV) / called
dpi(investments)                  # distributed / called
rvpi(investments)                 # NAV / called
called_capital(investments)
distributed_capital(investments)
nav(investments)                  # unrealized positions at net cost
total_value(investments)
```

### Portfolio & Analysis

```python
SBICPortfolio(name)
  .add(investment)
  .add_many(investments)
  .remove(investee_company)
  .filter_by_sector(naics_prefix)
  .filter_by_state(state)
  .filter_realized() / .filter_unrealized()
  .summary_stats()
  .summary()

vintage_year_analysis(investments)          # → {year: {count, tvpi, dpi, ...}}
peer_quartile_ranking(fund_tvpi, peer_tvpis) # → {quartile, percentile, peer_median}

sector_breakdown(investments)               # → {naics_2: {sector_name, invested, pct}}
state_breakdown(investments)                # → {state: {count, invested, pct}}
top_naics(investments, n=5)                 # → [(code, name, invested), ...]
```

## License

MIT © Jay Patel
