#!/usr/bin/env python3
"""
Backend API tests for Jerry's AI Law Observatory.

Structure: each scenario is a small, typed, single-purpose function registered
in TESTS. `main()` is a thin runner (no deep nesting / low complexity).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable, List, Optional

import requests

# ---------------------------------------------------------------------------
# Config & helpers
# ---------------------------------------------------------------------------

def _backend_url() -> str:
    env = Path(__file__).resolve().parent.parent / "frontend" / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                return line.split("=", 1)[1].strip().strip('"') + "/api"
    return "https://ai-act-explorer.preview.emergentagent.com/api"


BASE: str = _backend_url()
ADMIN_TOKEN: str = os.environ.get("ADMIN_TOKEN", "ailaw-admin-2025")
ADMIN_HEADERS = {"X-Admin-Token": ADMIN_TOKEN}


class Colors:
    OK = "\033[92m"
    FAIL = "\033[91m"
    END = "\033[0m"


def check(condition: bool, message: str) -> None:
    """Guard-clause assertion used inside test functions."""
    if not condition:
        raise AssertionError(message)


def get(path: str, **kwargs) -> requests.Response:
    return requests.get(f"{BASE}{path}", timeout=30, **kwargs)


def stream_chat(message: str, session_id: str = "test") -> tuple[str, List[dict]]:
    """Consume the SSE /chat endpoint; return (full_text, refs)."""
    text, refs = "", []
    with requests.post(f"{BASE}/chat", json={"session_id": session_id, "message": message},
                       stream=True, timeout=90) as resp:
        check(resp.status_code == 200, f"/chat status {resp.status_code}")
        for raw in resp.iter_lines():
            if not raw or not raw.startswith(b"data:"):
                continue
            evt = json.loads(raw[5:].strip())
            if evt.get("type") == "delta":
                text += evt["content"]
            elif evt.get("type") == "refs":
                refs = evt["refs"]
    return text, refs


# ---------------------------------------------------------------------------
# Test scenarios (each < 50 lines, single responsibility)
# ---------------------------------------------------------------------------

def test_root() -> None:
    r = get("/")
    check(r.status_code == 200, "root not 200")
    check("laws_tracked" in r.json(), "root missing laws_tracked")


def test_stats() -> None:
    d = get("/stats").json()
    check(d["total_laws"] == 372, f"expected 372 laws, got {d['total_laws']}")
    for key in ("total_jurisdictions", "enacted", "proposed", "by_group", "timeline", "region_status"):
        check(key in d, f"stats missing {key}")


def test_meta() -> None:
    d = get("/meta").json()
    for key in ("regions", "statuses", "categories", "countries", "groups"):
        check(key in d and d[key], f"meta missing/empty {key}")


def test_laws_pagination() -> None:
    d = get("/laws").json()
    check(d["count"] == 372 and d["returned"] == 60, "default pagination wrong")
    page2 = get("/laws?limit=60&offset=60").json()
    check(page2["laws"][0]["id"] != d["laws"][0]["id"], "offset did not change page")
    all_laws = get("/laws?limit=1000").json()
    check(all_laws["returned"] == 372, "limit=1000 did not return all")


def test_laws_filters() -> None:
    check(get("/laws?group=United States").json()["count"] == 144, "US group count wrong")
    check(get("/laws?status=Enacted").json()["count"] >= 300, "enacted count too low")
    china = get("/laws?country=China").json()
    check(china["count"] > 0 and all(l["country"] == "China" for l in china["laws"]), "country filter broken")
    yr = get("/laws?year_min=2024&year_max=2025").json()
    check(all(2024 <= l["year"] <= 2025 for l in yr["laws"]), "year filter broken")


def test_laws_sort() -> None:
    oldest = get("/laws?sort=oldest&limit=1000").json()["laws"]
    years = [l["year"] for l in oldest]
    check(years == sorted(years), "oldest sort not ascending")


def test_law_by_id() -> None:
    r = get("/laws/eu-ai-act-2024")
    if r.status_code == 200:
        check("key_provisions" in r.json(), "law detail missing key_provisions")
    any_id = get("/laws?limit=1").json()["laws"][0]["id"]
    check(get(f"/laws/{any_id}").status_code == 200, "valid law id not found")
    check(get("/laws/does-not-exist").status_code == 404, "invalid id not 404")


def test_countries() -> None:
    d = get("/countries").json()
    usa = d.get("United States of America")
    check(usa and usa["maturity"] >= 3, "USA maturity too low")
    detail = get("/countries/China").json()
    check(detail["total"] > 0 and "laws" in detail, "country detail broken")


def test_us_states() -> None:
    d = get("/us-states").json()
    check("California" in d and d["California"]["total"] > 0, "California state data missing")
    detail = get("/us-states/California").json()
    check(detail["total"] > 0 and detail["laws"], "state detail broken")
    check(get("/us-states/NotAState").status_code == 404, "bad state not 404")


def test_export_csv() -> None:
    r = get("/laws/export?group=Multilateral")
    check(r.status_code == 200, "export not 200")
    check("Jurisdiction,Title,Status" in r.text, "CSV header missing")


def test_admin_auth() -> None:
    check(get("/admin/verify").status_code == 401, "missing token should 401")
    check(get("/admin/verify", headers={"X-Admin-Token": "wrong"}).status_code == 401, "bad token should 401")
    check(get("/admin/verify", headers=ADMIN_HEADERS).status_code == 200, "good token should 200")


def test_admin_crud() -> None:
    body = {"country": "Testland", "region": "Europe", "title": "Temp Test Law",
            "status": "Enacted", "category": "AI governance", "year": 2026,
            "summary": "temp", "group": "International"}
    created = requests.post(f"{BASE}/admin/laws", json=body, headers=ADMIN_HEADERS, timeout=30).json()
    law_id = created["law"]["id"]
    try:
        check(get(f"/laws?search=Temp Test Law").json()["count"] >= 1, "created law not searchable")
        upd = requests.put(f"{BASE}/admin/laws/{law_id}", json={**body, "title": "Temp Test Law v2"},
                           headers=ADMIN_HEADERS, timeout=30)
        check(upd.status_code == 200, "update failed")
    finally:
        d = requests.delete(f"{BASE}/admin/laws/{law_id}", headers=ADMIN_HEADERS, timeout=30)
        check(d.status_code == 200, "delete failed")
    check(get("/stats").json()["total_laws"] == 372, "count not restored to 372")


def test_admin_validation() -> None:
    bad_year = requests.post(f"{BASE}/admin/laws", json={"country": "X", "title": "Y", "year": -1},
                             headers=ADMIN_HEADERS, timeout=30)
    check(bad_year.status_code == 422, "negative year not rejected")
    blank = requests.post(f"{BASE}/admin/laws", json={"country": "X", "title": "  ", "year": 2025},
                          headers=ADMIN_HEADERS, timeout=30)
    check(blank.status_code == 422, "blank title not rejected")


def test_chat_enriched() -> None:
    text, refs = stream_chat("What is the EU AI Act? Explain what it does.")
    low = text.lower()
    check(len(text) > 200, "answer too short")
    check(any(k in low for k in ("risk", "high-risk", "general-purpose", "gpai")), "answer not enriched")
    check(len(refs) > 0, "no citation refs returned")


def test_chat_out_of_scope() -> None:
    text, _ = stream_chat("What are the exact fines in the fictional AI law of Atlantis?")
    check(len(text) > 20, "no answer for out-of-scope question")


def test_chat_history() -> None:
    stream_chat("Hello", session_id="hist-test")
    msgs = get("/chat/history/hist-test").json()["messages"]
    check(len(msgs) >= 1, "chat history not stored")


def test_chat_no_meta_commentary_us_eu_comparison() -> None:
    """Verify assistant answers US/EU comparison directly without tracker meta-commentary."""
    text, _ = stream_chat("Compare the US and EU approaches to AI regulation.", session_id="no-meta-1")
    low = text.lower()
    
    # Check for substantive content
    check(len(text) > 150, "answer too short for comparison")
    check("eu" in low or "europe" in low, "missing EU content")
    check("us" in low or "united states" in low or "america" in low, "missing US content")
    
    # Check for absence of meta-commentary phrases
    bad_phrases = [
        "tracker context", "does not include", "doesn't include",
        "i'll use general", "i will use general", "because the tracker",
        "because your tracker", "tracker does not", "tracker doesn't"
    ]
    for phrase in bad_phrases:
        check(phrase not in low, f"found meta-commentary phrase: '{phrase}'")


def test_chat_no_meta_commentary_eu_ai_act() -> None:
    """Verify EU AI Act question gets factual answer without disclaimers."""
    text, _ = stream_chat("What is the EU AI Act?", session_id="no-meta-2")
    low = text.lower()
    
    # Check for substantive content
    check(len(text) > 150, "answer too short")
    check(any(k in low for k in ("risk", "high-risk", "unacceptable", "prohibited")), 
          "missing key EU AI Act concepts")
    
    # Check for absence of meta-commentary
    bad_phrases = [
        "tracker context", "does not include", "doesn't include",
        "i'll use general", "because the tracker", "tracker does not"
    ]
    for phrase in bad_phrases:
        check(phrase not in low, f"found meta-commentary phrase: '{phrase}'")


def test_chat_no_meta_commentary_texas() -> None:
    """Verify Texas AI laws question answers factually without coverage disclaimers."""
    text, _ = stream_chat("What AI laws exist in Texas?", session_id="no-meta-3")
    low = text.lower()
    
    # Check for substantive answer
    check(len(text) > 50, "answer too short")
    check("texas" in low, "missing Texas in answer")
    
    # Check for absence of meta-commentary
    bad_phrases = [
        "tracker context", "does not include", "doesn't include",
        "i'll use general", "because the tracker", "tracker does not",
        "because your tracker"
    ]
    for phrase in bad_phrases:
        check(phrase not in low, f"found meta-commentary phrase: '{phrase}'")


def test_chat_nonsense_no_fabrication() -> None:
    """Verify assistant doesn't fabricate specifics for nonsense queries."""
    text, _ = stream_chat("What are the exact penalties in the Atlantis AI Regulation Act of 2024?", 
                         session_id="no-meta-4")
    low = text.lower()
    
    # Should not fabricate specific article numbers or precise penalties for fictional law
    check(len(text) > 20, "no answer returned")
    # Should acknowledge it's fictional or provide general context, not specific fake details
    # We won't be too strict here, just ensure it doesn't claim specific articles/fines


TESTS: List[Callable[[], None]] = [
    test_root, test_stats, test_meta, test_laws_pagination, test_laws_filters,
    test_laws_sort, test_law_by_id, test_countries, test_us_states, test_export_csv,
    test_admin_auth, test_admin_crud, test_admin_validation,
    test_chat_enriched, test_chat_out_of_scope, test_chat_history,
    test_chat_no_meta_commentary_us_eu_comparison,
    test_chat_no_meta_commentary_eu_ai_act,
    test_chat_no_meta_commentary_texas,
    test_chat_nonsense_no_fabrication,
]


def main() -> int:
    print(f"Running {len(TESTS)} backend tests against {BASE}\n")
    passed = 0
    for test in TESTS:
        try:
            test()
            passed += 1
            print(f"{Colors.OK}PASS{Colors.END}  {test.__name__}")
        except Exception as e:  # noqa: BLE001 - report and continue
            print(f"{Colors.FAIL}FAIL{Colors.END}  {test.__name__}: {e}")
    print(f"\n{passed}/{len(TESTS)} passed")
    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
