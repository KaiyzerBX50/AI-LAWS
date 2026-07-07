"""
One-off build script: parse the uploaded AI Act-Law Tracker.xlsx (2 sheets:
US states + Non-US) into a clean, unified JSON dataset the API loads at runtime.
Run: python build_dataset.py
Output: /app/backend/laws_dataset.json
"""
import json
import re
import openpyxl
from pathlib import Path

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


def slugify(*parts):
    base = "-".join(str(p) for p in parts if p)
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base[:80]


def normalize_status(raw):
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


def extract_year(*texts):
    for t in texts:
        if t is None:
            continue
        m = re.search(r"(19|20)\d{2}", str(t))
        if m:
            return int(m.group(0))
    return 2024


def domain(url):
    if not url:
        return "Source"
    m = re.search(r"https?://([^/]+)", url)
    return m.group(1).replace("www.", "") if m else "Source"


def base_country(juris):
    """Strip subnational / co-signatory suffixes to get a base country."""
    c = juris.split(" / ")[0].strip()
    sub = None
    if " - " in c:
        c, sub = c.split(" - ", 1)
        c = c.strip(); sub = sub.strip()
    return c, sub


def geo_for(country):
    if country in MULTILATERAL_BODIES:
        return []
    if country in GEO_MAP:
        g = GEO_MAP[country]
        return [g] if g else []
    return [country]  # assume name matches Natural Earth


def main():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    entries = []

    # ---- US sheet ----
    us = list(wb["US - AI Law Tracker"].iter_rows(values_only=True))
    for r in us[1:]:
        if not r or not r[1] or not r[2]:
            continue
        num, juris, law, status, coverage, year, category, url, notes = (list(r) + [None] * 9)[:9]
        entries.append({
            "id": slugify("us", juris, law, num),
            "country": "United States of America",
            "jurisdiction": f"{juris} (US)",
            "subnational": juris,
            "region": "United States",
            "geo_names": ["United States of America"],
            "title": str(law).strip(),
            "status": normalize_status(status),
            "status_raw": (status or "").strip(),
            "category": (category or "Other").strip(),
            "type": "Law / bill",
            "year": extract_year(year, status, coverage),
            "effective": str(year) if year else "",
            "authority": juris,
            "summary": (coverage or "").strip() or "AI-related legislation.",
            "key_provisions": [],
            "sources": [{"title": domain(url), "url": url}] if url else [],
            "notes": (notes or "").strip(),
            "group": "United States",
        })

    # ---- Non-US sheet ----
    nus = list(wb["Non US - AILT"].iter_rows(values_only=True))
    for r in nus[1:]:
        if not r or not r[1] or not r[2]:
            continue
        (num, juris, law, status, coverage, region, typ, category,
         binding, effective, authority, url, notes) = (list(r) + [None] * 13)[:13]
        country, sub = base_country(str(juris))
        entries.append({
            "id": slugify("intl", juris, law, num),
            "country": country,
            "jurisdiction": str(juris).strip(),
            "subnational": sub,
            "region": REGION_MAP.get(region, region or "Multilateral"),
            "geo_names": geo_for(country),
            "title": str(law).strip(),
            "status": normalize_status(status),
            "status_raw": (status or "").strip(),
            "category": (category or "AI governance").strip(),
            "type": (typ or "").strip(),
            "binding_level": (binding or "").strip(),
            "year": extract_year(effective, status, binding, coverage),
            "effective": (effective or "").strip(),
            "authority": (authority or country).strip(),
            "summary": (coverage or "").strip() or "AI-related law or policy.",
            "key_provisions": [],
            "sources": [{"title": domain(url), "url": url}] if url else [],
            "notes": (notes or "").strip(),
            "group": "Multilateral" if country in MULTILATERAL_BODIES or region == "Multilateral" else "International",
        })

    OUT.write_text(json.dumps(entries, indent=1, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT}")
    # quick stats
    from collections import Counter
    print("By group:", dict(Counter(e["group"] for e in entries)))
    print("By status:", dict(Counter(e["status"] for e in entries)))
    print("By region:", dict(Counter(e["region"] for e in entries)))
    print("Distinct countries:", len(set(e["country"] for e in entries)))
    print("Distinct categories:", len(set(e["category"] for e in entries)))


if __name__ == "__main__":
    main()
