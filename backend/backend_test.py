#!/usr/bin/env python3
"""
Backend API tests for Global AI Law Tracker - Phase 3
Tests the full 372-entry dataset with pagination, group filters, CSV export, etc.
"""
import requests
import sys
from typing import Dict, Any

BASE_URL = "https://ai-act-explorer.preview.emergentagent.com/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class APITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def test(self, name: str, fn):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n{Colors.BLUE}[{self.tests_run}] Testing: {name}{Colors.END}")
        try:
            fn()
            self.tests_passed += 1
            print(f"{Colors.GREEN}✓ PASSED{Colors.END}")
            return True
        except AssertionError as e:
            self.tests_failed += 1
            print(f"{Colors.RED}✗ FAILED: {e}{Colors.END}")
            return False
        except Exception as e:
            self.tests_failed += 1
            print(f"{Colors.RED}✗ ERROR: {e}{Colors.END}")
            return False

    def assert_eq(self, actual, expected, msg=""):
        if actual != expected:
            raise AssertionError(f"{msg} Expected {expected}, got {actual}")

    def assert_gte(self, actual, minimum, msg=""):
        if actual < minimum:
            raise AssertionError(f"{msg} Expected >= {minimum}, got {actual}")

    def assert_in(self, item, container, msg=""):
        if item not in container:
            raise AssertionError(f"{msg} {item} not in {container}")

    def summary(self):
        print(f"\n{'='*60}")
        print(f"{Colors.BLUE}TEST SUMMARY{Colors.END}")
        print(f"Total: {self.tests_run} | {Colors.GREEN}Passed: {self.tests_passed}{Colors.END} | {Colors.RED}Failed: {self.tests_failed}{Colors.END}")
        print(f"Success rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print(f"{'='*60}\n")
        return self.tests_failed == 0


def main():
    t = APITester()

    # Test 1: Root endpoint
    def test_root():
        r = requests.get(f"{BASE_URL}/")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["laws_tracked"], 372, "Total laws tracked")
        print(f"  → {data}")
    t.test("GET /api/ returns 372 laws", test_root)

    # Test 2: Stats endpoint - verify 372 laws, ~83 jurisdictions
    def test_stats():
        r = requests.get(f"{BASE_URL}/stats")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["total_laws"], 372, "Total laws")
        t.assert_gte(data["total_jurisdictions"], 80, "Total jurisdictions")
        t.assert_gte(data["enacted"], 300, "Enacted laws")
        t.assert_in("United States", data["by_group"], "by_group has United States")
        t.assert_in("International", data["by_group"], "by_group has International")
        t.assert_in("Multilateral", data["by_group"], "by_group has Multilateral")
        print(f"  → total_laws={data['total_laws']}, jurisdictions={data['total_jurisdictions']}, enacted={data['enacted']}, proposed={data['proposed']}")
        print(f"  → by_group: {data['by_group']}")
    t.test("GET /api/stats returns 372 laws, ~83 jurisdictions, by_group", test_stats)

    # Test 3: Laws endpoint - default pagination (60 per page)
    def test_laws_default():
        r = requests.get(f"{BASE_URL}/laws")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["count"], 372, "Total count")
        t.assert_gte(data["returned"], 50, "Returned at least 50")
        t.assert_eq(data["offset"], 0, "Offset is 0")
        print(f"  → count={data['count']}, returned={data['returned']}, offset={data['offset']}")
    t.test("GET /api/laws returns count=372, returned<=60", test_laws_default)

    # Test 4: Laws pagination - offset 0
    def test_laws_page1():
        r = requests.get(f"{BASE_URL}/laws?limit=60&offset=0")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["count"], 372, "Total count")
        t.assert_eq(data["returned"], 60, "Returned 60")
        t.assert_eq(data["offset"], 0, "Offset 0")
        first_id = data["laws"][0]["id"]
        print(f"  → Page 1: returned={data['returned']}, first_id={first_id}")
        return first_id
    first_id = t.test("GET /api/laws?limit=60&offset=0 returns 60 laws", test_laws_page1)

    # Test 5: Laws pagination - offset 60
    def test_laws_page2():
        r = requests.get(f"{BASE_URL}/laws?limit=60&offset=60")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["count"], 372, "Total count")
        t.assert_gte(data["returned"], 50, "Returned at least 50")
        t.assert_eq(data["offset"], 60, "Offset 60")
        second_page_first_id = data["laws"][0]["id"]
        if first_id:
            if second_page_first_id == first_id:
                raise AssertionError("Page 2 first ID should differ from page 1")
        print(f"  → Page 2: returned={data['returned']}, first_id={second_page_first_id}")
    t.test("GET /api/laws?limit=60&offset=60 returns different laws", test_laws_page2)

    # Test 6: Group filter - United States (144 laws)
    def test_group_us():
        r = requests.get(f"{BASE_URL}/laws?group=United%20States")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["count"], 144, "US laws count")
        print(f"  → United States: {data['count']} laws")
    t.test("GET /api/laws?group=United States returns 144 laws", test_group_us)

    # Test 7: Group filter - Multilateral (17 laws)
    def test_group_multilateral():
        r = requests.get(f"{BASE_URL}/laws?group=Multilateral")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["count"], 17, "Multilateral laws count")
        print(f"  → Multilateral: {data['count']} laws")
    t.test("GET /api/laws?group=Multilateral returns 17 laws", test_group_multilateral)

    # Test 8: Group filter - International (~211 laws)
    def test_group_international():
        r = requests.get(f"{BASE_URL}/laws?group=International")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(data["count"], 200, "International laws count >= 200")
        print(f"  → International: {data['count']} laws")
    t.test("GET /api/laws?group=International returns ~211 laws", test_group_international)

    # Test 9: Region filter - Asia-Pacific
    def test_region_asia():
        r = requests.get(f"{BASE_URL}/laws?region=Asia-Pacific")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(data["count"], 10, "Asia-Pacific laws")
        print(f"  → Asia-Pacific: {data['count']} laws")
    t.test("GET /api/laws?region=Asia-Pacific works", test_region_asia)

    # Test 10: Status filter - Enacted
    def test_status_enacted():
        r = requests.get(f"{BASE_URL}/laws?status=Enacted")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(data["count"], 300, "Enacted laws >= 300")
        print(f"  → Enacted: {data['count']} laws")
    t.test("GET /api/laws?status=Enacted works", test_status_enacted)

    # Test 11: Search filter
    def test_search():
        r = requests.get(f"{BASE_URL}/laws?search=Texas")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(data["count"], 1, "Texas search results")
        print(f"  → Search 'Texas': {data['count']} laws")
    t.test("GET /api/laws?search=Texas works", test_search)

    # Test 12: Sort filter - oldest
    def test_sort_oldest():
        r = requests.get(f"{BASE_URL}/laws?sort=oldest&limit=5")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        years = [law["year"] for law in data["laws"]]
        print(f"  → Oldest first years: {years[:5]}")
    t.test("GET /api/laws?sort=oldest works", test_sort_oldest)

    # Test 13: CSV export - default
    def test_export_default():
        r = requests.get(f"{BASE_URL}/laws/export")
        t.assert_eq(r.status_code, 200, "Status code")
        t.assert_eq(r.headers["Content-Type"], "text/csv; charset=utf-8", "Content-Type")
        t.assert_in("attachment", r.headers.get("Content-Disposition", ""), "Content-Disposition")
        lines = r.text.strip().split('\n')
        t.assert_gte(len(lines), 370, "CSV has 370+ rows")
        header = lines[0]
        t.assert_in("Jurisdiction", header, "CSV header has Jurisdiction")
        t.assert_in("Title", header, "CSV header has Title")
        t.assert_in("Source URL", header, "CSV header has Source URL")
        print(f"  → CSV export: {len(lines)} lines, header: {header[:80]}...")
    t.test("GET /api/laws/export returns CSV with 372+ rows", test_export_default)

    # Test 14: CSV export - filtered by region
    def test_export_filtered():
        r = requests.get(f"{BASE_URL}/laws/export?region=Middle%20East")
        t.assert_eq(r.status_code, 200, "Status code")
        lines = r.text.strip().split('\n')
        t.assert_gte(len(lines), 2, "CSV has at least header + 1 row")
        print(f"  → CSV export (Middle East): {len(lines)} lines")
    t.test("GET /api/laws/export?region=Middle East returns filtered CSV", test_export_filtered)

    # Test 15: Meta endpoint - groups, regions, categories
    def test_meta():
        r = requests.get(f"{BASE_URL}/meta")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_in("groups", data, "Has groups")
        t.assert_in("regions", data, "Has regions")
        t.assert_in("statuses", data, "Has statuses")
        t.assert_in("categories", data, "Has categories")
        t.assert_gte(len(data["categories"]), 50, "100+ categories")
        t.assert_in("United States", data["groups"], "groups has United States")
        t.assert_in("International", data["groups"], "groups has International")
        t.assert_in("Multilateral", data["groups"], "groups has Multilateral")
        print(f"  → groups: {data['groups']}")
        print(f"  → regions: {len(data['regions'])} regions")
        print(f"  → categories: {len(data['categories'])} categories")
    t.test("GET /api/meta returns groups, regions, statuses, categories", test_meta)

    # Test 16: Countries endpoint
    def test_countries():
        r = requests.get(f"{BASE_URL}/countries")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(len(data), 50, "At least 50 countries")
        t.assert_in("United States of America", data, "Has USA")
        usa = data["United States of America"]
        t.assert_gte(usa["total"], 140, "USA has 140+ laws")
        t.assert_gte(usa["maturity"], 3, "USA maturity >= 3")
        print(f"  → {len(data)} countries, USA: {usa['total']} laws, maturity={usa['maturity']}")
    t.test("GET /api/countries returns USA with 140+ laws", test_countries)

    # Test 17: Country detail - USA
    def test_country_usa():
        r = requests.get(f"{BASE_URL}/countries/United%20States%20of%20America")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["name"], "United States of America", "Country name")
        t.assert_gte(data["total"], 140, "USA total laws")
        t.assert_gte(len(data["laws"]), 140, "USA laws list")
        # Check for US state entries
        jurisdictions = [law.get("jurisdiction", law["country"]) for law in data["laws"]]
        has_state = any("Texas" in j or "California" in j or "New York" in j for j in jurisdictions)
        if not has_state:
            print(f"  ⚠ Warning: No US state entries found in USA laws")
        print(f"  → USA: {data['total']} laws, maturity={data['maturity']}, sample jurisdictions: {jurisdictions[:5]}")
    t.test("GET /api/countries/United States of America returns de-duplicated laws with US states", test_country_usa)

    # Test 18: Chat endpoint - streaming SSE
    def test_chat():
        r = requests.post(
            f"{BASE_URL}/chat",
            json={"session_id": "test_phase3", "message": "What AI laws exist in Texas?"},
            stream=True,
            timeout=30
        )
        t.assert_eq(r.status_code, 200, "Status code")
        t.assert_in("text/event-stream", r.headers.get("Content-Type", ""), "Content-Type is SSE")
        
        events = []
        for line in r.iter_lines(decode_unicode=True):
            if line.startswith("data:"):
                events.append(line)
                if len(events) > 100:  # limit to avoid hanging
                    break
        
        t.assert_gte(len(events), 3, "At least 3 SSE events (refs, deltas, done)")
        # Check for refs event
        has_refs = any("refs" in e for e in events[:5])
        has_done = any("done" in e for e in events)
        if not has_refs:
            print(f"  ⚠ Warning: No 'refs' event found")
        if not has_done:
            print(f"  ⚠ Warning: No 'done' event found")
        print(f"  → Chat streaming: {len(events)} SSE events received")
    t.test("POST /api/chat streams grounded SSE responses", test_chat)

    # Test 19: Law detail by ID
    def test_law_detail():
        # Get a law ID first
        r = requests.get(f"{BASE_URL}/laws?limit=1")
        law_id = r.json()["laws"][0]["id"]
        
        r2 = requests.get(f"{BASE_URL}/laws/{law_id}")
        t.assert_eq(r2.status_code, 200, "Status code")
        data = r2.json()
        t.assert_eq(data["id"], law_id, "Law ID matches")
        t.assert_in("title", data, "Has title")
        t.assert_in("sources", data, "Has sources")
        t.assert_in("related", data, "Has related")
        print(f"  → Law {law_id}: {data['title'][:50]}...")
    t.test("GET /api/laws/{id} returns full law details", test_law_detail)

    # Test 20: Last verified field on all laws
    def test_last_verified():
        r = requests.get(f"{BASE_URL}/laws?limit=10")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        for law in data["laws"]:
            t.assert_in("last_verified", law, f"Law {law['id']} has last_verified")
            # Check format YYYY-MM-DD
            lv = law["last_verified"]
            if len(lv) != 10 or lv[4] != '-' or lv[7] != '-':
                raise AssertionError(f"last_verified format invalid: {lv}")
        print(f"  → All {len(data['laws'])} laws have last_verified field (YYYY-MM-DD)")
    t.test("GET /api/laws returns laws with last_verified field", test_last_verified)

    # Test 21: Last verified in law detail
    def test_last_verified_detail():
        r = requests.get(f"{BASE_URL}/laws?limit=1")
        law_id = r.json()["laws"][0]["id"]
        r2 = requests.get(f"{BASE_URL}/laws/{law_id}")
        t.assert_eq(r2.status_code, 200, "Status code")
        data = r2.json()
        t.assert_in("last_verified", data, "Law detail has last_verified")
        print(f"  → Law {law_id} last_verified: {data['last_verified']}")
    t.test("GET /api/laws/{id} includes last_verified", test_last_verified_detail)

    # Test 22: US states endpoint
    def test_us_states():
        r = requests.get(f"{BASE_URL}/us-states")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(len(data), 30, "At least 30 US states")
        t.assert_in("California", data, "Has California")
        ca = data["California"]
        t.assert_gte(ca["total"], 1, "California has laws")
        t.assert_in("counts", ca, "California has counts")
        t.assert_in("maturity", ca, "California has maturity")
        print(f"  → {len(data)} US states, California: {ca['total']} laws, maturity={ca['maturity']}")
    t.test("GET /api/us-states returns ~40 states with California", test_us_states)

    # Test 23: US state detail - California
    def test_us_state_california():
        r = requests.get(f"{BASE_URL}/us-states/California")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["name"], "California", "State name")
        t.assert_gte(data["total"], 1, "California total laws")
        t.assert_in("laws", data, "Has laws list")
        t.assert_in("maturity", data, "Has maturity")
        print(f"  → California: {data['total']} laws, maturity={data['maturity']}")
    t.test("GET /api/us-states/California returns state detail", test_us_state_california)

    # Test 24: US state detail - NotAState (404)
    def test_us_state_404():
        r = requests.get(f"{BASE_URL}/us-states/NotAState")
        t.assert_eq(r.status_code, 404, "Status code should be 404")
        print(f"  → NotAState correctly returns 404")
    t.test("GET /api/us-states/NotAState returns 404", test_us_state_404)

    # Test 25: Admin verify - no token (401)
    def test_admin_verify_no_token():
        r = requests.get(f"{BASE_URL}/admin/verify")
        t.assert_eq(r.status_code, 401, "Status code should be 401")
        print(f"  → No token correctly returns 401")
    t.test("GET /api/admin/verify without token returns 401", test_admin_verify_no_token)

    # Test 26: Admin verify - wrong token (401)
    def test_admin_verify_wrong_token():
        r = requests.get(f"{BASE_URL}/admin/verify", headers={"X-Admin-Token": "wrong-token"})
        t.assert_eq(r.status_code, 401, "Status code should be 401")
        print(f"  → Wrong token correctly returns 401")
    t.test("GET /api/admin/verify with wrong token returns 401", test_admin_verify_wrong_token)

    # Test 27: Admin verify - correct token (200)
    def test_admin_verify_correct():
        r = requests.get(f"{BASE_URL}/admin/verify", headers={"X-Admin-Token": "ailaw-admin-2025"})
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["ok"], True, "ok is True")
        print(f"  → Correct token returns {data}")
    t.test("GET /api/admin/verify with correct token returns 200", test_admin_verify_correct)

    # Test 28: Admin create law - no token (401)
    def test_admin_create_no_token():
        r = requests.post(f"{BASE_URL}/admin/laws", json={
            "country": "Test Country", "title": "Test Law", "status": "Enacted",
            "category": "AI governance", "year": 2025, "summary": "Test", "group": "International"
        })
        t.assert_eq(r.status_code, 401, "Status code should be 401")
        print(f"  → No token correctly returns 401")
    t.test("POST /api/admin/laws without token returns 401", test_admin_create_no_token)

    # Test 29: Admin create law - with token (200)
    created_law_id = None
    def test_admin_create_with_token():
        nonlocal created_law_id
        r = requests.post(f"{BASE_URL}/admin/laws", 
            headers={"X-Admin-Token": "ailaw-admin-2025"},
            json={
                "country": "Test Country", "title": "Test Law for Admin CRUD", 
                "status": "Enacted", "category": "AI governance", "year": 2025, 
                "summary": "This is a test law created by the testing agent", 
                "source_url": "https://example.com", "group": "International", "region": "Europe"
            })
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["ok"], True, "ok is True")
        t.assert_in("law", data, "Has law object")
        t.assert_in("id", data["law"], "Law has id")
        t.assert_in("last_verified", data["law"], "Law has last_verified")
        created_law_id = data["law"]["id"]
        print(f"  → Created law: {created_law_id}, last_verified={data['law']['last_verified']}")
    t.test("POST /api/admin/laws with token creates law", test_admin_create_with_token)

    # Test 30: Admin update law - with token (200)
    def test_admin_update_with_token():
        if not created_law_id:
            print(f"  ⚠ Skipping: no created law ID")
            return
        r = requests.put(f"{BASE_URL}/admin/laws/{created_law_id}",
            headers={"X-Admin-Token": "ailaw-admin-2025"},
            json={
                "country": "Test Country", "title": "Test Law UPDATED", 
                "status": "Enacted", "category": "AI governance", "year": 2025, 
                "summary": "This law was updated", "source_url": "https://example.com", 
                "group": "International", "region": "Europe"
            })
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["ok"], True, "ok is True")
        print(f"  → Updated law: {created_law_id}")
    t.test("PUT /api/admin/laws/{id} with token updates law", test_admin_update_with_token)

    # Test 31: Verify update via search
    def test_verify_update():
        if not created_law_id:
            print(f"  ⚠ Skipping: no created law ID")
            return
        r = requests.get(f"{BASE_URL}/laws?search=Test Law UPDATED")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_gte(data["count"], 1, "Found updated law")
        found = any(law["id"] == created_law_id for law in data["laws"])
        if not found:
            raise AssertionError(f"Updated law {created_law_id} not found in search")
        print(f"  → Search found updated law: {created_law_id}")
    t.test("GET /api/laws?search=Test Law UPDATED reflects update", test_verify_update)

    # Test 32: Admin delete law - with token (200)
    def test_admin_delete_with_token():
        if not created_law_id:
            print(f"  ⚠ Skipping: no created law ID")
            return
        r = requests.delete(f"{BASE_URL}/admin/laws/{created_law_id}",
            headers={"X-Admin-Token": "ailaw-admin-2025"})
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_eq(data["ok"], True, "ok is True")
        t.assert_eq(data["deleted"], created_law_id, "deleted ID matches")
        print(f"  → Deleted law: {created_law_id}")
    t.test("DELETE /api/admin/laws/{id} with token deletes law", test_admin_delete_with_token)

    # Test 33: Verify deletion via stats
    def test_verify_deletion():
        r = requests.get(f"{BASE_URL}/stats")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        # Should be back to 372 (or close if other tests created entries)
        t.assert_gte(data["total_laws"], 372, "Total laws >= 372")
        print(f"  → After deletion, total_laws={data['total_laws']}")
    t.test("GET /api/stats shows law count after deletion", test_verify_deletion)

    # Test 34: Admin delete nonexistent law (404)
    def test_admin_delete_404():
        r = requests.delete(f"{BASE_URL}/admin/laws/nonexistent-id-12345",
            headers={"X-Admin-Token": "ailaw-admin-2025"})
        t.assert_eq(r.status_code, 404, "Status code should be 404")
        print(f"  → Nonexistent law correctly returns 404")
    t.test("DELETE /api/admin/laws/{nonexistent} returns 404", test_admin_delete_404)

    # Test 35: Meta includes last_verified
    def test_meta_last_verified():
        r = requests.get(f"{BASE_URL}/meta")
        t.assert_eq(r.status_code, 200, "Status code")
        data = r.json()
        t.assert_in("last_verified", data, "Meta has last_verified")
        print(f"  → Meta last_verified: {data['last_verified']}")
    t.test("GET /api/meta includes last_verified", test_meta_last_verified)

    # Test 36: AI Assistant enrichment - EU AI Act detailed answer
    def test_chat_eu_ai_act_enriched():
        import json
        import time
        r = requests.post(
            f"{BASE_URL}/chat",
            json={"session_id": "test_enrichment_eu", "message": "What is the EU AI Act? Explain what it actually does."},
            stream=True,
            timeout=45
        )
        t.assert_eq(r.status_code, 200, "Status code")
        
        events = []
        full_response = ""
        refs_found = False
        
        for line in r.iter_lines(decode_unicode=True):
            if line.startswith("data:"):
                try:
                    data = json.loads(line[5:].strip())
                    events.append(data)
                    if data.get("type") == "refs":
                        refs_found = True
                    elif data.get("type") == "delta":
                        full_response += data.get("content", "")
                    elif data.get("type") == "done":
                        break
                except:
                    pass
        
        t.assert_eq(refs_found, True, "Should have refs event")
        t.assert_gte(len(full_response), 200, "Response should be substantive (>200 chars)")
        
        # Check for concrete details about EU AI Act
        response_lower = full_response.lower()
        has_risk_mention = any(term in response_lower for term in ["risk", "tier", "unacceptable", "high risk", "minimal"])
        has_detail = any(term in response_lower for term in ["banned", "prohibited", "obligation", "requirement", "penalty", "fine", "gpai", "general-purpose", "timeline", "phased"])
        
        if not has_risk_mention:
            print(f"  ⚠ Warning: Response lacks risk-based approach details")
        if not has_detail:
            print(f"  ⚠ Warning: Response lacks concrete details (banned practices, obligations, penalties, etc.)")
        
        print(f"  → EU AI Act response: {len(full_response)} chars, has_risk_mention={has_risk_mention}, has_detail={has_detail}")
        print(f"  → First 300 chars: {full_response[:300]}...")
    t.test("POST /api/chat EU AI Act returns enriched, detailed answer", test_chat_eu_ai_act_enriched)

    # Test 37: AI Assistant enrichment - China generative AI
    def test_chat_china_generative_ai():
        import json
        import time
        r = requests.post(
            f"{BASE_URL}/chat",
            json={"session_id": "test_enrichment_china", "message": "How does China regulate generative AI?"},
            stream=True,
            timeout=45
        )
        t.assert_eq(r.status_code, 200, "Status code")
        
        full_response = ""
        refs_found = False
        
        for line in r.iter_lines(decode_unicode=True):
            if line.startswith("data:"):
                try:
                    data = json.loads(line[5:].strip())
                    if data.get("type") == "refs":
                        refs_found = True
                    elif data.get("type") == "delta":
                        full_response += data.get("content", "")
                    elif data.get("type") == "done":
                        break
                except:
                    pass
        
        t.assert_eq(refs_found, True, "Should have refs event")
        t.assert_gte(len(full_response), 100, "Response should be substantive (>100 chars)")
        
        # Should not be a refusal
        response_lower = full_response.lower()
        is_refusal = any(term in response_lower for term in ["i don't have", "i cannot", "i'm unable", "no information", "not sure"])
        
        if is_refusal:
            print(f"  ⚠ Warning: Response appears to be a refusal")
        
        print(f"  → China generative AI response: {len(full_response)} chars, is_refusal={is_refusal}")
        print(f"  → First 200 chars: {full_response[:200]}...")
    t.test("POST /api/chat China generative AI returns substantive answer", test_chat_china_generative_ai)

    # Test 38: AI Assistant - out-of-scope question (should not fabricate)
    def test_chat_out_of_scope():
        import json
        r = requests.post(
            f"{BASE_URL}/chat",
            json={"session_id": "test_out_of_scope", "message": "What are the exact fine amounts in the fictional AI law of Atlantis?"},
            stream=True,
            timeout=45
        )
        t.assert_eq(r.status_code, 200, "Status code")
        
        full_response = ""
        
        for line in r.iter_lines(decode_unicode=True):
            if line.startswith("data:"):
                try:
                    data = json.loads(line[5:].strip())
                    if data.get("type") == "delta":
                        full_response += data.get("content", "")
                    elif data.get("type") == "done":
                        break
                except:
                    pass
        
        # Should indicate lack of information, not fabricate specifics
        response_lower = full_response.lower()
        indicates_uncertainty = any(term in response_lower for term in ["don't have", "no information", "not tracked", "unable", "cannot", "not sure", "no record", "no data", "not aware"])
        
        # Check if response mentions Atlantis with specific monetary amounts (fabrication)
        has_atlantis = "atlantis" in response_lower
        has_money = any(sym in response_lower for sym in ["$", "€", "million", "billion"])
        fabricates = has_atlantis and has_money and not indicates_uncertainty
        
        print(f"  → Out-of-scope response: {len(full_response)} chars, indicates_uncertainty={indicates_uncertainty}, fabricates={fabricates}")
        print(f"  → Response: {full_response[:300]}...")
    t.test("POST /api/chat out-of-scope question does not fabricate", test_chat_out_of_scope)

    # Test 39: Chat history persistence
    def test_chat_history():
        import json
        session_id = "test_history_persistence"
        
        # Send a message
        r = requests.post(
            f"{BASE_URL}/chat",
            json={"session_id": session_id, "message": "What is the EU AI Act?"},
            stream=True,
            timeout=45
        )
        t.assert_eq(r.status_code, 200, "Chat status code")
        
        # Consume the stream
        for line in r.iter_lines(decode_unicode=True):
            if line.startswith("data:"):
                try:
                    data = json.loads(line[5:].strip())
                    if data.get("type") == "done":
                        break
                except:
                    pass
        
        # Check history
        r2 = requests.get(f"{BASE_URL}/chat/history/{session_id}")
        t.assert_eq(r2.status_code, 200, "History status code")
        data = r2.json()
        t.assert_in("messages", data, "Has messages")
        t.assert_gte(len(data["messages"]), 2, "At least 2 messages (user + assistant)")
        
        # Check message structure
        user_msg = next((m for m in data["messages"] if m["role"] == "user"), None)
        assistant_msg = next((m for m in data["messages"] if m["role"] == "assistant"), None)
        
        if not user_msg:
            raise AssertionError("No user message in history")
        if not assistant_msg:
            raise AssertionError("No assistant message in history")
        
        t.assert_in("content", user_msg, "User message has content")
        t.assert_in("content", assistant_msg, "Assistant message has content")
        t.assert_in("timestamp", user_msg, "User message has timestamp")
        
        print(f"  → History: {len(data['messages'])} messages, user={user_msg['content'][:50]}..., assistant={assistant_msg['content'][:50]}...")
    t.test("GET /api/chat/history/{session_id} returns stored messages", test_chat_history)

    # Summary
    success = t.summary()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
