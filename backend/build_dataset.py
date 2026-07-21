"""
One-off build script: parse the uploaded AI Act-Law Tracker.xlsx (2 sheets:
US states + Non-US) into a clean, unified JSON dataset the API loads at runtime.
Run: python build_dataset.py
Output: /app/backend/laws_dataset.json
"""
import json
import re
from collections import Counter
from pathlib import Path
from typing import List, Optional, Tuple

import openpyxl

SRC = "/tmp/ai_tracker.xlsx"
OUT = Path(__file__).parent / "laws_dataset.json"

# Country/jurisdiction name -> world-atlas (Natural Earth) geo name.
# Special tokens __EU__ / __COE__ expand server-side to member/signatory states.
GEO_MAP = {
    "United States": "United States of America",
    "European Union": "__EU__",
    "Council of Europe": "__COE__",
    "United Kingdom": "United Kingdom",
    "South Korea": "South Korea",
    "United Arab Emirates": "United Arab Emirates",
    "Turkey": "Turkey",
    "Taiwan": "Taiwan",
    "China": "China",
    "Japan": "Japan",
    "India": "India",
    "Brazil": "Brazil",
    "Argentina": "Argentina",
    "Chile": "Chile",
    "Colombia": "Colombia",
    "Peru": "Peru",
    "Egypt": "Egypt",
    "Kenya": "Kenya",
    "Nigeria": "Nigeria",
    "Mauritius": "Mauritius",
    "Indonesia": "Indonesia",
    "Bangladesh": "Bangladesh",
    "Israel": "Israel",
    "Singapore": "Singapore",
    "Saudi Arabia": "Saudi Arabia",
    "Australia": "Australia",
    "New Zealand": "New Zealand",
    "Canada": "Canada",
    "France": "France",
    "Hong Kong": None,  # part of China in 110m; keep in list, no map fill
}

MULTILATERAL_BODIES = {"OECD", "UNESCO", "G7", "ISO/IEC", "ASEAN",
                       "African Union", "Global Partnership on AI"}

REGION_MAP = {
    "North America (non-US)": "North America",
    "Europe / Middle East": "Europe",
    "Asia-Pacific": "Asia-Pacific",
    "Latin America": "Latin America",
    "Middle East": "Middle East",
    "Africa": "Africa",
    "Europe": "Europe",
    "Multilateral": "Multilateral",
}


def slugify(*parts) -> str:
    base = "-".join(str(p) for p in parts if p)
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base[:80]


def normalize_status(raw: Optional[str]) -> str:
    s = (raw or "").lower()
    if "fail" in s or "superseded" in s or "repealed" in s:
        return "Superseded"
    if "draft" in s:
        return "Draft"
    if any(k in s for k in ["propos", "pending", "consultation", "under debate",
                            "introduc", "reintroduc", "presented", "under discussion",
                            "announced", "in development", "bill", "proceed"]):
        return "Proposed"
    if any(k in s for k in ["enacted", "signed", "in force", "adopted", "passed",
                            "published", "released", "active", "opened for signature",
                            "effective", "finalized", "guidance", "phased", "onward"]):
        return "Enacted"
    return "Enacted"


def extract_year(*texts) -> int:
    for t in texts:
        if t is None:  # noqa: E711 - intentional None identity check (PEP 8)
            continue
        m = re.search(r"(19|20)\d{2}", str(t))
        if m:
            return int(m.group(0))
    return 2024


def domain(url: Optional[str]) -> str:
    if not url:
        return "Source"
    m = re.search(r"https?://([^/]+)", url)
    return m.group(1).replace("www.", "") if m else "Source"


def base_country(juris: str) -> Tuple[str, Optional[str]]:
    """Strip subnational / co-signatory suffixes to get a base country."""
    c = juris.split(" / ")[0].strip()
    sub = None
    if " - " in c:
        c, sub = c.split(" - ", 1)
        c = c.strip(); sub = sub.strip()
    return c, sub


def geo_for(country: str) -> List[str]:
    if country in MULTILATERAL_BODIES:
        return []
    if country in GEO_MAP:
        g = GEO_MAP[country]
        return [g] if g else []
    return [country]  # assume name matches Natural Earth


def source_list(url: Optional[str]) -> List[dict]:
    return [{"title": domain(url), "url": url}] if url else []


def _clean(value, default: str = "") -> str:
    """Trim a cell to a string, falling back to a default when empty/None."""
    s = ("" if value is None else str(value)).strip()  # noqa: E711 - intentional None identity check (PEP 8)
    return s or default


def parse_us_row(r: tuple) -> Optional[dict]:
    """Convert a row from the 'US - AI Law Tracker' sheet into a law entry."""
    if not r or not r[1] or not r[2]:
        return None
    num, juris, law, status, coverage, year, category, url, notes = (list(r) + [None] * 9)[:9]
    return {
        "id": slugify("us", juris, law, num),
        "country": "United States of America",
        "jurisdiction": f"{juris} (US)",
        "subnational": juris,
        "region": "United States",
        "geo_names": ["United States of America"],
        "title": _clean(law),
        "status": normalize_status(status),
        "status_raw": _clean(status),
        "category": _clean(category, "Other"),
        "type": "Law / bill",
        "year": extract_year(year, status, coverage),
        "effective": str(year) if year else "",
        "authority": juris,
        "summary": _clean(coverage, "AI-related legislation."),
        "key_provisions": [],
        "sources": source_list(url),
        "notes": _clean(notes),
        "group": "United States",
    }


def parse_nonus_row(r: tuple) -> Optional[dict]:
    """Convert a row from the 'Non US - AILT' sheet into a law entry."""
    if not r or not r[1] or not r[2]:
        return None
    (num, juris, law, status, coverage, region, typ, category,
     binding, effective, authority, url, notes) = (list(r) + [None] * 13)[:13]
    country, sub = base_country(str(juris))
    is_multilateral = country in MULTILATERAL_BODIES or region == "Multilateral"
    return {
        "id": slugify("intl", juris, law, num),
        "country": country,
        "jurisdiction": _clean(juris),
        "subnational": sub,
        "region": REGION_MAP.get(region, region or "Multilateral"),
        "geo_names": geo_for(country),
        "title": _clean(law),
        "status": normalize_status(status),
        "status_raw": _clean(status),
        "category": _clean(category, "AI governance"),
        "type": _clean(typ),
        "binding_level": _clean(binding),
        "year": extract_year(effective, status, binding, coverage),
        "effective": _clean(effective),
        "authority": _clean(authority, country),
        "summary": _clean(coverage, "AI-related law or policy."),
        "key_provisions": [],
        "sources": source_list(url),
        "notes": _clean(notes),
        "group": "Multilateral" if is_multilateral else "International",
    }


def print_stats(entries: List[dict]) -> None:
    print("By group:", dict(Counter(e["group"] for e in entries)))
    print("By status:", dict(Counter(e["status"] for e in entries)))
    print("By region:", dict(Counter(e["region"] for e in entries)))
    print("Distinct countries:", len(set(e["country"] for e in entries)))
    print("Distinct categories:", len(set(e["category"] for e in entries)))


def load_sheet(wb, name: str, parser) -> List[dict]:
    rows = list(wb[name].iter_rows(values_only=True))[1:]  # skip header
    return [entry for r in rows if (entry := parser(r)) is not None]  # noqa: E711 - intentional None identity check (PEP 8)


def main() -> None:
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    entries: List[dict] = []
    entries += load_sheet(wb, "US - AI Law Tracker", parse_us_row)
    entries += load_sheet(wb, "Non US - AILT", parse_nonus_row)

    OUT.write_text(json.dumps(entries, indent=1, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT}")
    print_stats(entries)


if __name__ == "__main__":
    main()
