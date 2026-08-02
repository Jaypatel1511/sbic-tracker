"""
Sample data loaders for SBIC licensees and investments.

sbic-tracker ships NO live data source. Everything in this module is invented
demo data, and as of 0.2.0 it is reachable only when a caller asks for it by
name — ``load_from_sba_url()`` raises instead of falling through to it, which is
what it did silently through 0.1.0.
"""
from __future__ import annotations

from datetime import date
from typing import List

from sbictracker.exceptions import SBICTrackerError, SBADownloadError
from sbictracker.data.schema import Investment, SBICLicensee


def load_sample_licensees() -> List[SBICLicensee]:
    """Return a set of 10 FICTIONAL SBIC licensees — explicit opt-in demo data.

    WARNING: these are invented fund names, managers, license numbers, dates and
    dollar amounts. They are NOT SBA program data and no SBIC in this list
    exists. Every record is stamped ``data_source == "sample"`` so downstream
    code can tell a demo figure from a real one.

    Legitimate for demos, examples and tests. Being the *silent fallback* from
    ``load_from_sba_url()`` was the bug; that path is gone.
    """
    licensees = [
        SBICLicensee("04/73-0001", "Apex Growth Fund I", "Apex Capital",
                     date(2015, 3, 12), "active", "Standard",
                     150_000_000, 100_000_000, 50_000_000),
        SBICLicensee("07/79-0042", "BlueStar Impact SBIC", "BlueStar Ventures",
                     date(2018, 6, 5), "active", "Impact",
                     80_000_000, 50_000_000, 30_000_000),
        SBICLicensee("09/79-0641", "Cornerstone Clean Energy", "Cornerstone Partners",
                     date(2017, 9, 20), "active", "Energy Saving",
                     60_000_000, 40_000_000, 20_000_000),
        SBICLicensee("02/79-0120", "Delta Mezzanine Fund", "Delta Capital",
                     date(2014, 1, 15), "surrendered", "Standard",
                     200_000_000, 130_000_000, 70_000_000),
        SBICLicensee("03/73-0088", "Eagle Tech SBIC", "Eagle Ventures",
                     date(2019, 11, 3), "active", "Standard",
                     40_000_000, 25_000_000, 15_000_000),
        SBICLicensee("05/79-0200", "Frontier Healthcare Fund", "Frontier Capital",
                     date(2016, 4, 28), "active", "Impact",
                     120_000_000, 80_000_000, 40_000_000),
        SBICLicensee("01/79-0305", "Gateway Manufacturing SBIC", "Gateway Partners",
                     date(2013, 7, 10), "wound_down", "Standard",
                     90_000_000, 60_000_000, 30_000_000),
        SBICLicensee("06/79-0155", "Horizon Software Fund", "Horizon Ventures",
                     date(2020, 2, 18), "active", "Standard",
                     50_000_000, 33_000_000, 17_000_000),
        SBICLicensee("08/79-0099", "Inland Agri SBIC", "Inland Capital",
                     date(2015, 8, 22), "active", "Standard",
                     70_000_000, 46_000_000, 24_000_000),
        SBICLicensee("10/79-0500", "Jupiter Consumer Fund", "Jupiter Equity",
                     date(2021, 5, 9), "active", "Standard",
                     35_000_000, 23_000_000, 12_000_000),
    ]
    for licensee in licensees:
        licensee.data_source = "sample"
    return licensees


def load_sample_investments() -> List[Investment]:
    """Return a portfolio of 20 FICTIONAL investments — explicit opt-in demo data.

    WARNING: invented portfolio companies with invented dates, NAICS codes and
    dollar amounts. Fund-level IRR / TVPI / DPI computed over this list is
    arithmetic on fiction. Every record is stamped ``data_source == "sample"``.
    """
    investments = [
        Investment("TechStart Inc.", date(2018, 3, 1), 5_000_000,
                   "541512", "CA", date(2022, 6, 1), 12_000_000, 0, "equity"),
        Investment("MediSol LLC", date(2019, 7, 15), 3_000_000,
                   "621111", "TX", None, 0, 0, "debt"),
        Investment("CleanPower Corp", date(2017, 11, 1), 8_000_000,
                   "221114", "CO", date(2021, 12, 31), 14_000_000, 0, "mezzanine"),
        Investment("AgriTech Solutions", date(2020, 2, 1), 2_500_000,
                   "115112", "IA", None, 0, 500_000, "debt"),
        Investment("Retail Express Co.", date(2016, 5, 20), 4_000_000,
                   "452990", "OH", date(2019, 4, 30), 1_200_000, 0, "equity"),
        Investment("BuildRight Contractors", date(2018, 8, 10), 6_000_000,
                   "236115", "FL", None, 0, 0, "debt"),
        Investment("SoftLogic Systems", date(2021, 1, 15), 3_500_000,
                   "511210", "NY", None, 0, 0, "equity"),
        Investment("FoodFresh Distribution", date(2017, 4, 5), 5_500_000,
                   "424400", "IL", date(2020, 9, 15), 8_250_000, 0, "mezzanine"),
        Investment("HealthPath Services", date(2019, 9, 30), 2_000_000,
                   "621999", "GA", None, 0, 2_000_000, "equity"),
        Investment("MetalWorks Inc.", date(2015, 6, 1), 7_000_000,
                   "331110", "MI", date(2020, 1, 31), 10_500_000, 0, "debt"),
        Investment("Sunrise Hotels LLC", date(2018, 12, 1), 4_500_000,
                   "721110", "AZ", None, 0, 0, "debt"),
        Investment("DataBridge Analytics", date(2020, 7, 20), 1_800_000,
                   "518210", "WA", None, 0, 0, "equity"),
        Investment("GreenBuild Materials", date(2016, 3, 14), 3_200_000,
                   "327320", "NC", date(2021, 6, 30), 6_400_000, 0, "mezzanine"),
        Investment("FastFreight Logistics", date(2019, 5, 1), 2_750_000,
                   "484121", "TN", None, 0, 0, "debt"),
        Investment("EduSpark Learning", date(2021, 3, 15), 1_500_000,
                   "611710", "MA", None, 0, 0, "equity"),
        Investment("PowerGrid Solutions", date(2017, 10, 10), 9_000_000,
                   "221122", "TX", date(2022, 3, 31), 18_000_000, 0, "equity"),
        Investment("PharmaBridge Inc.", date(2020, 11, 5), 4_000_000,
                   "325412", "NJ", None, 0, 1_000_000, "debt"),
        Investment("Coastal Fisheries LLC", date(2016, 7, 1), 2_200_000,
                   "114111", "ME", date(2019, 8, 31), 1_100_000, 0, "equity"),
        Investment("ManuTech Robotics", date(2019, 2, 28), 6_500_000,
                   "333249", "OH", None, 0, 0, "mezzanine"),
        Investment("Summit Staffing Co.", date(2018, 4, 16), 1_200_000,
                   "561320", "CO", date(2021, 11, 30), 960_000, 0, "debt"),
    ]
    for investment in investments:
        investment.data_source = "sample"
    return investments


# The CKAN resource_id below is a hand-typed sequential-hex placeholder, not a
# real SBA dataset id. It 404s (verified 2026-07-30). It is retained ONLY so the
# error message can name the endpoint that was configured; nothing requests it.
_CONFIGURED_SBA_ENDPOINT = (
    "https://data.sba.gov/api/3/action/datastore_search"
    "?resource_id=d8e9a5a1-b2c3-4d5e-8f6a-7b8c9d0e1f2a&limit=50"
)


def load_from_sba_url() -> List[SBICLicensee]:
    """Raise SBADownloadError: live SBA loading is not implemented in this package.

    This function has never been able to return live data. Through 0.1.0 it
    attempted the endpoint below, swallowed every failure with
    ``except Exception: pass``, left the success branch unimplemented
    (``return []  # would parse live records here``), and then returned
    ``load_sample_licensees()`` — so every caller silently received invented
    fund names, dates and dollar amounts labelled as SBA program data, and
    computed IRR / TVPI / DPI on top of them.

    0.2.0 raises instead. No request is attempted: the configured endpoint is
    known-invalid, and the response parser does not exist, so there is nothing
    a successful request could produce.

    If you want the demo dataset, call ``load_sample_licensees()`` explicitly —
    its records carry ``data_source == "sample"``.

    Raises
    ------
    SBADownloadError
        Always. sbic-tracker is not maintained; see the README.
    """
    raise SBADownloadError(
        "Live SBA SBIC data loading is not implemented in sbic-tracker. "
        f"The configured endpoint {_CONFIGURED_SBA_ENDPOINT} is invalid — its "
        "CKAN resource_id is a placeholder that returns HTTP 404 — and no "
        "response parser exists, so no request is attempted. This function "
        "raises rather than silently returning load_sample_licensees(), which "
        "is what it did through 0.1.0. Call load_sample_licensees() directly "
        "if you want the demo dataset (records are stamped "
        'data_source == "sample"). sbic-tracker is not currently maintained '
        "and no live SBA source is planned; see the README."
    )
