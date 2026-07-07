#!/usr/bin/env python3
"""
Comprehensive backend API tests for Global AI Law Tracker
Tests all endpoints with various scenarios
"""
import requests
import sys
import json
from datetime import datetime

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
        self.failures = []

    def test(self, name, func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n{Colors.BLUE}🔍 Test {self.tests_run}: {name}{Colors.END}")
        try:
            func()
            self.tests_passed += 1
            print(f"{Colors.GREEN}✅ PASSED{Colors.END}")
            return True
        except AssertionError as e:
            self.tests_failed += 1
            self.failures.append({"test": name, "error": str(e)})
            print(f"{Colors.RED}❌ FAILED: {e}{Colors.END}")
            return False
        except Exception as e:
            self.tests_failed += 1
            self.failures.append({"test": name, "error": f"Exception: {str(e)}"})
            print(f"{Colors.RED}❌ ERROR: {e}{Colors.END}")
            return False

    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"{Colors.BLUE}TEST SUMMARY{Colors.END}")
        print(f"{'='*60}")
        print(f"Total tests: {self.tests_run}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.END}")
        
        if self.failures:
            print(f"\n{Colors.RED}FAILED TESTS:{Colors.END}")
            for i, failure in enumerate(self.failures, 1):
                print(f"{i}. {failure['test']}")
                print(f"   Error: {failure['error']}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\nSuccess rate: {success_rate:.1f}%")
        return self.tests_failed == 0


def main():
    tester = APITester()
    
    # Test 1: GET /api/stats
    def test_stats():
        r = requests.get(f"{BASE_URL}/stats", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["total_laws"] == 26, f"Expected 26 laws, got {data['total_laws']}"
        assert "total_jurisdictions" in data, "Missing total_jurisdictions"
        assert "enacted" in data, "Missing enacted count"
        assert "proposed" in data, "Missing proposed count"
        assert "timeline" in data and isinstance(data["timeline"], list), "Missing or invalid timeline"
        assert "by_status" in data, "Missing by_status"
        assert "by_region" in data, "Missing by_region"
        assert "by_category" in data, "Missing by_category"
        assert "region_status" in data, "Missing region_status"
        # Check timeline structure
        if data["timeline"]:
            assert "year" in data["timeline"][0], "Timeline missing year"
            assert "count" in data["timeline"][0], "Timeline missing count"
            assert "cumulative" in data["timeline"][0], "Timeline missing cumulative"
        print(f"   Stats: {data['total_laws']} laws, {data['total_jurisdictions']} jurisdictions")
    
    tester.test("GET /api/stats returns correct structure", test_stats)
    
    # Test 2: GET /api/laws (no filters)
    def test_laws_all():
        r = requests.get(f"{BASE_URL}/laws", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert "count" in data, "Missing count field"
        assert "laws" in data, "Missing laws field"
        assert data["count"] == 26, f"Expected 26 laws, got {data['count']}"
        assert len(data["laws"]) == 26, f"Expected 26 laws in array, got {len(data['laws'])}"
        print(f"   Retrieved {data['count']} laws")
    
    tester.test("GET /api/laws returns all laws", test_laws_all)
    
    # Test 3: GET /api/laws with search filter
    def test_laws_search():
        r = requests.get(f"{BASE_URL}/laws", params={"search": "EU"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["count"] > 0, "Search for 'EU' should return results"
        # Check that results contain EU-related laws
        has_eu = any("EU" in law["title"] or "EU" in law["country"] for law in data["laws"])
        assert has_eu, "Search results should contain EU-related laws"
        print(f"   Search 'EU' returned {data['count']} results")
    
    tester.test("GET /api/laws with search filter", test_laws_search)
    
    # Test 4: GET /api/laws with region filter
    def test_laws_region():
        r = requests.get(f"{BASE_URL}/laws", params={"region": "Asia"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["count"] > 0, "Asia region should have laws"
        # Verify all results are from Asia
        for law in data["laws"]:
            assert law["region"] == "Asia", f"Law {law['id']} has wrong region: {law['region']}"
        print(f"   Asia region has {data['count']} laws")
    
    tester.test("GET /api/laws with region=Asia filter", test_laws_region)
    
    # Test 5: GET /api/laws with status filter
    def test_laws_status():
        r = requests.get(f"{BASE_URL}/laws", params={"status": "Enacted"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["count"] > 0, "Should have enacted laws"
        for law in data["laws"]:
            assert law["status"] == "Enacted", f"Law {law['id']} has wrong status: {law['status']}"
        print(f"   {data['count']} enacted laws")
    
    tester.test("GET /api/laws with status=Enacted filter", test_laws_status)
    
    # Test 6: GET /api/laws with category filter
    def test_laws_category():
        r = requests.get(f"{BASE_URL}/laws", params={"category": "Comprehensive"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["count"] > 0, "Should have comprehensive laws"
        for law in data["laws"]:
            assert law["category"] == "Comprehensive", f"Law {law['id']} has wrong category"
        print(f"   {data['count']} comprehensive laws")
    
    tester.test("GET /api/laws with category filter", test_laws_category)
    
    # Test 7: GET /api/laws with country filter
    def test_laws_country():
        r = requests.get(f"{BASE_URL}/laws", params={"country": "China"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["count"] > 0, "China should have laws"
        for law in data["laws"]:
            assert law["country"] == "China", f"Law {law['id']} has wrong country"
        print(f"   China has {data['count']} laws")
    
    tester.test("GET /api/laws with country filter", test_laws_country)
    
    # Test 8: GET /api/laws with year filters
    def test_laws_year():
        r = requests.get(f"{BASE_URL}/laws", params={"year_min": 2023, "year_max": 2024}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["count"] > 0, "Should have laws from 2023-2024"
        for law in data["laws"]:
            assert 2023 <= law["year"] <= 2024, f"Law {law['id']} year {law['year']} out of range"
        print(f"   {data['count']} laws from 2023-2024")
    
    tester.test("GET /api/laws with year_min and year_max", test_laws_year)
    
    # Test 9: GET /api/laws with sort=oldest
    def test_laws_sort_oldest():
        r = requests.get(f"{BASE_URL}/laws", params={"sort": "oldest"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        years = [law["year"] for law in data["laws"]]
        assert years == sorted(years), "Laws should be sorted by year ascending"
        print(f"   Oldest law: {data['laws'][0]['year']}, newest: {data['laws'][-1]['year']}")
    
    tester.test("GET /api/laws with sort=oldest", test_laws_sort_oldest)
    
    # Test 10: GET /api/laws with sort=country
    def test_laws_sort_country():
        r = requests.get(f"{BASE_URL}/laws", params={"sort": "country"}, timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        countries = [law["country"] for law in data["laws"]]
        assert countries == sorted(countries), "Laws should be sorted by country"
        print(f"   First country: {data['laws'][0]['country']}")
    
    tester.test("GET /api/laws with sort=country", test_laws_sort_country)
    
    # Test 11: GET /api/laws/{id} with valid ID
    def test_law_by_id():
        r = requests.get(f"{BASE_URL}/laws/eu-ai-act-2024", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["id"] == "eu-ai-act-2024", "Wrong law ID"
        assert "title" in data, "Missing title"
        assert "summary" in data, "Missing summary"
        assert "key_provisions" in data, "Missing key_provisions"
        assert "sources" in data, "Missing sources"
        assert "related" in data, "Missing related laws"
        assert isinstance(data["key_provisions"], list), "key_provisions should be a list"
        assert isinstance(data["sources"], list), "sources should be a list"
        assert isinstance(data["related"], list), "related should be a list"
        print(f"   Law: {data['title']}")
        print(f"   Key provisions: {len(data['key_provisions'])}, Sources: {len(data['sources'])}, Related: {len(data['related'])}")
    
    tester.test("GET /api/laws/eu-ai-act-2024 returns full law details", test_law_by_id)
    
    # Test 12: GET /api/laws/{id} with invalid ID
    def test_law_invalid_id():
        r = requests.get(f"{BASE_URL}/laws/invalid-law-id-12345", timeout=10)
        assert r.status_code == 404, f"Expected 404 for invalid ID, got {r.status_code}"
        print(f"   Correctly returned 404 for invalid ID")
    
    tester.test("GET /api/laws/{id} returns 404 for invalid ID", test_law_invalid_id)
    
    # Test 13: GET /api/countries
    def test_countries():
        r = requests.get(f"{BASE_URL}/countries", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert isinstance(data, dict), "Countries should be a dict/map"
        assert len(data) > 0, "Should have countries"
        
        # Check specific countries
        assert "United States of America" in data, "Missing USA"
        assert "France" in data, "Missing France"
        assert "China" in data, "Missing China"
        
        # Check structure of a country entry
        usa = data["United States of America"]
        assert "maturity" in usa, "Missing maturity"
        assert "maturity_label" in usa, "Missing maturity_label"
        assert "counts" in usa, "Missing counts"
        assert "law_ids" in usa, "Missing law_ids"
        assert 0 <= usa["maturity"] <= 4, f"Invalid maturity: {usa['maturity']}"
        
        # Check France includes EU AI Act
        france = data["France"]
        assert "eu-ai-act-2024" in france["law_ids"], "France should include EU AI Act"
        
        print(f"   {len(data)} countries with data")
        print(f"   USA maturity: {usa['maturity']} ({usa['maturity_label']})")
        print(f"   France has {len(france['law_ids'])} laws (includes EU laws)")
    
    tester.test("GET /api/countries returns country map with maturity", test_countries)
    
    # Test 14: GET /api/countries/{name} - France
    def test_country_france():
        r = requests.get(f"{BASE_URL}/countries/France", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["name"] == "France", "Wrong country name"
        assert "maturity" in data, "Missing maturity"
        assert "maturity_label" in data, "Missing maturity_label"
        assert "total" in data, "Missing total"
        assert "laws" in data, "Missing laws array"
        
        # Check for de-duplication (EU laws should appear once)
        law_ids = [law["id"] for law in data["laws"]]
        assert len(law_ids) == len(set(law_ids)), "Laws should be de-duplicated"
        
        # France should have EU AI Act and GDPR
        assert "eu-ai-act-2024" in law_ids, "France should have EU AI Act"
        
        print(f"   France: {data['total']} unique laws, maturity {data['maturity']}")
    
    tester.test("GET /api/countries/France returns de-duplicated laws", test_country_france)
    
    # Test 15: GET /api/countries/{name} - China
    def test_country_china():
        r = requests.get(f"{BASE_URL}/countries/China", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert data["name"] == "China", "Wrong country name"
        assert data["total"] >= 3, "China should have at least 3 laws"
        
        # Check for specific Chinese laws
        law_ids = [law["id"] for law in data["laws"]]
        assert "cn-genai-2023" in law_ids, "China should have GenAI law"
        
        print(f"   China: {data['total']} laws")
    
    tester.test("GET /api/countries/China returns country details", test_country_china)
    
    # Test 16: GET /api/countries/{name} - Invalid country
    def test_country_invalid():
        r = requests.get(f"{BASE_URL}/countries/InvalidCountryName123", timeout=10)
        assert r.status_code == 404, f"Expected 404 for invalid country, got {r.status_code}"
        print(f"   Correctly returned 404 for invalid country")
    
    tester.test("GET /api/countries/{name} returns 404 for invalid country", test_country_invalid)
    
    # Test 17: GET /api/meta
    def test_meta():
        r = requests.get(f"{BASE_URL}/meta", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert "regions" in data, "Missing regions"
        assert "statuses" in data, "Missing statuses"
        assert "categories" in data, "Missing categories"
        assert "countries" in data, "Missing countries"
        assert "year_min" in data, "Missing year_min"
        assert "year_max" in data, "Missing year_max"
        
        assert isinstance(data["regions"], list), "Regions should be a list"
        assert isinstance(data["statuses"], list), "Statuses should be a list"
        assert isinstance(data["categories"], list), "Categories should be a list"
        assert isinstance(data["countries"], list), "Countries should be a list"
        
        assert len(data["regions"]) > 0, "Should have regions"
        assert len(data["statuses"]) > 0, "Should have statuses"
        assert len(data["categories"]) > 0, "Should have categories"
        assert len(data["countries"]) > 0, "Should have countries"
        
        print(f"   Regions: {len(data['regions'])}, Statuses: {len(data['statuses'])}")
        print(f"   Categories: {len(data['categories'])}, Countries: {len(data['countries'])}")
        print(f"   Year range: {data['year_min']} - {data['year_max']}")
    
    tester.test("GET /api/meta returns filter metadata", test_meta)
    
    # Test 18: POST /api/chat - SSE streaming
    def test_chat_streaming():
        session_id = f"test-{datetime.now().timestamp()}"
        payload = {
            "session_id": session_id,
            "message": "How does the EU regulate AI?"
        }
        
        r = requests.post(f"{BASE_URL}/chat", json=payload, stream=True, timeout=30)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert "text/event-stream" in r.headers.get("content-type", ""), "Should be SSE stream"
        
        events = []
        refs_received = False
        deltas_received = 0
        done_received = False
        
        # Read SSE stream
        for line in r.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            try:
                data = json.loads(line[5:].strip())
                events.append(data)
                if data.get("type") == "refs":
                    refs_received = True
                    assert isinstance(data.get("refs"), list), "refs should be a list"
                elif data.get("type") == "delta":
                    deltas_received += 1
                    assert "content" in data, "delta should have content"
                elif data.get("type") == "done":
                    done_received = True
                    break
            except json.JSONDecodeError:
                continue
        
        assert refs_received, "Should receive refs event"
        assert deltas_received > 0, "Should receive delta events"
        assert done_received, "Should receive done event"
        
        print(f"   Session: {session_id}")
        print(f"   Received {deltas_received} delta events")
        print(f"   Stream completed successfully")
        
        return session_id
    
    session_id = None
    if tester.test("POST /api/chat streams SSE response", test_chat_streaming):
        # Get the session_id from the test
        try:
            session_id = test_chat_streaming()
        except:
            pass
    
    # Test 19: GET /api/chat/history/{session_id}
    def test_chat_history():
        # Use a known session or create a new one
        test_session = f"test-history-{datetime.now().timestamp()}"
        
        # First send a message
        payload = {"session_id": test_session, "message": "Test question"}
        r = requests.post(f"{BASE_URL}/chat", json=payload, stream=True, timeout=30)
        # Consume the stream
        for _ in r.iter_lines():
            pass
        
        # Now get history
        r = requests.get(f"{BASE_URL}/chat/history/{test_session}", timeout=10)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        data = r.json()
        assert "messages" in data, "Missing messages field"
        assert isinstance(data["messages"], list), "messages should be a list"
        assert len(data["messages"]) >= 2, "Should have at least user and assistant messages"
        
        # Check message structure
        user_msg = next((m for m in data["messages"] if m["role"] == "user"), None)
        assert user_msg is not None, "Should have user message"
        assert "content" in user_msg, "Message should have content"
        assert "timestamp" in user_msg, "Message should have timestamp"
        
        print(f"   Retrieved {len(data['messages'])} messages from history")
    
    tester.test("GET /api/chat/history/{session_id} returns chat history", test_chat_history)
    
    # Print summary
    success = tester.summary()
    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.END}")
        sys.exit(1)
