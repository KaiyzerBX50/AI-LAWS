# plan.md

## 1. Objectives
- **Deliver a production-ready worldwide, interactive tracker** for AI-related laws/acts/regulations with a policy-grade UI.
- Provide **two primary exploration modes**: clickable world map + searchable/filterable browse grid.
- Include **law detail views** with accurate summaries, key provisions, and **official source links** (no mock data).
- Provide an **LLM-powered AI Assistant** (Emergent universal key; OpenAI `gpt-5.4`) for grounded Q&A with streaming output and citations.
- Support **Day/Night (light/dark) mode** with persisted user preference.

**Current status:** Objectives for Phase 1 and Phase 2 are fully implemented and validated (backend 19/19 tests; frontend feature suite passes).

---

## 2. Implementation Steps

### Phase 1 — Core POC (LLM Integration in Isolation) ✅ COMPLETE
**Goal:** Prove AI Assistant works reliably before building the full app.
- Implemented a minimal Python POC using `emergentintegrations` + `EMERGENT_LLM_KEY`.
- Model: **OpenAI `gpt-5.4`**.
- System prompt enforces: factual tone, grounding, citations, and graceful “unknowns”.
- Passed a small curated context bundle and validated with **5 test questions**.
- Confirmed **streaming via `stream_message()`** works as required.

**POC exit criteria:** ✅ met
- Consistent answers
- Graceful “unknown”
- Predictable output behavior

Artifacts:
- `/app/backend/poc_test.py`

---

### Phase 2 — V1 App Development (Map + Tracker + Assistant + Theme) ✅ COMPLETE

#### Backend (FastAPI + MongoDB)
**Delivered:** A working API with curated real dataset and streaming chat.
- Curated **real-world dataset**: **26 entries** across **17 jurisdictions**, including:
  - EU AI Act (Reg. 2024/1689), GDPR automated decisions
  - US: EO 14179 (2025), EO 14110 (2023, superseded), NIST AI RMF (2023), Colorado AI Act (2024), California transparency (2024)
  - China: GenAI Measures (2023), Deep Synthesis (2022/2023), Algorithmic Recommendations (2022)
  - UK AI Regulation White Paper approach (2023)
  - Canada AIDA (Bill C-27; lapsed)
  - Brazil PL 2338/2023 (Senate approved Dec 2024; pending)
  - South Korea AI Basic Act
  - Japan AI Promotion Act (2025) + Human-centric AI principles
  - India DPDP Act (2023) + advisories
  - Australia AI Safety Standard + proposed guardrails
  - Singapore Model AI Governance Framework (GenAI)
  - UAE AI Strategy 2031
  - Saudi SDAIA AI ethics principles
  - Israel AI policy approach
  - France CNIL AI guidance
  - Chile AI bill
  - Council of Europe AI Convention treaty
- Supra-national laws are applied to map geographies:
  - **EU laws** spread to **EU-27 members**
  - **Council of Europe treaty** spread to a defined signatory set (incl. EU members + select others)

**API Endpoints delivered:**
- `GET /api/laws` (filters: search, region, status, category, country, year_min/year_max, sort)
- `GET /api/laws/{id}` (detail + related)
- `GET /api/countries` (map-ready: maturity, counts, law IDs)
- `GET /api/countries/{name}` (country detail + de-duped laws)
- `GET /api/stats` (KPI + timeline + region/status breakdown)
- `GET /api/meta` (filter metadata)
- `POST /api/chat` (**SSE streaming**: refs → deltas → done; grounded context injection)
- `GET /api/chat/history/{session_id}` (persisted chat)

Artifacts:
- `/app/backend/server.py`
- `/app/backend/ai_laws_data.py`


#### Frontend (React + shadcn/ui + react-simple-maps + recharts)
**Delivered:** A polished interactive UI aligned with the design guidelines.
- **Persisted theme toggle** (localStorage; class-based dark mode)
- Navigation: **Explore | Browse | Timeline | Compare | Assistant**
- Explore (Map + charts):
  - Interactive world map with **hover tooltips**, zoom controls, and country click → **CountryPanel**
  - Map modes: **Maturity** and **Status** + legend
  - Stats KPI row + charts (timeline cumulative, category distribution, regional status)
- Browse:
  - Search + filters (region/status/category/sort)
  - Card grid with law cards and detail dialog
- Timeline:
  - Chronological grouping by year; click opens law detail
- Compare:
  - Select up to **3 countries**; side-by-side summaries
- Assistant:
  - Streaming chat UI with suggested prompts
  - Displays citation chips (refs) for the laws used

A11y polish:
- Added `DialogDescription` and `SheetDescription` to address low-severity accessibility warnings.

Artifacts:
- `/app/frontend/src/App.js`
- `/app/frontend/src/index.css` (design tokens + fonts)
- `/app/frontend/src/components/*`
- `/app/frontend/src/lib/api.js` (SSE chat stream)
- `/app/frontend/src/constants/testIds/tracker.js`


#### End of Phase 2 Testing ✅ COMPLETE
- `testing_agent_v3` iteration_1: **100% pass**
  - Backend: **19/19** tests passed
  - Frontend: all feature flows verified

**Phase 2 user stories:** ✅ all covered
1. Click country on map → see AI-related laws
2. Toggle Day/Night mode + persists
3. Search + filter by region/status/category (+ sorting)
4. Open law detail view with provisions + sources
5. Ask AI assistant and get grounded responses with references
6. Timeline view by year
7. Compare 2–3 countries

---

### Phase 3 — Enhancements (Quality + Coverage + UX) ⏳ NEXT
**Goal:** Expand coverage, improve data lifecycle, and add sharing/export.
- Expand curated dataset coverage:
  - Add more jurisdictions and sectoral rules
  - Add `last_verified` date per entry and a “freshness” badge per law
- Improve Assistant grounding:
  - Add optional country/region focus controls in the assistant UI
  - Stronger “cannot verify” guardrails + tighter citation formatting
- Export/share:
  - Shareable URLs that preserve filters and selected country
  - Export filtered results to CSV
- UX/Performance polish:
  - Better mobile layout for compare and timeline
  - Add skeleton loaders for all async panels
  - Add caching for `/laws` responses and MongoDB indexes (if migrating from in-code seed → DB)

**End of Phase 3:** run 1 full end-to-end testing pass.

**Phase 3 user stories (at least 5)**
1. As a user, I can share a link that preserves filters and selected country.
2. As a user, I can export filtered law results to CSV.
3. As a user, I can see when an entry was last verified.
4. As a user, I can ask country-specific questions and the assistant focuses on that jurisdiction.
5. As a user, I get improved empty/loading states and a smoother mobile UX.

---

### Phase 4+ — Optional (Admin + Auth) (Future)
**Goal:** Add maintainability features for long-term curation.
- Add admin-only authentication to manage entries (create/edit/update sources)
- Add audit trail for edits + moderation workflow
- Bulk CSV import and validation

**Phase 4 user stories (at least 5)**
1. As an admin, I can add a new law with sources.
2. As an admin, I can update a law’s status with timestamps.
3. As an admin, I can flag entries as needs review.
4. As an admin, I can bulk import via CSV template.
5. As a user, I can trust entries with provenance and update history.

---

## 3. Next Actions
1. Collect user feedback on desired Phase 3 priorities (share links vs CSV export vs broader coverage).
2. Add `last_verified` fields + UI freshness indicators.
3. Implement shareable URL state (filters + selected country + tab).
4. Add CSV export endpoint and frontend download flow.
5. Expand curated dataset (increase jurisdiction coverage) and rerun end-to-end tests.

---

## 4. Success Criteria
✅ Completed (Phase 1–2)
- LLM integration returns usable, grounded, streaming answers with graceful failure modes.
- V1 app supports map click → laws list → detail view without dead ends.
- Filters/search respond quickly and correctly.
- Day/Night mode is smooth, accessible, and persists.
- AI Assistant answers include relevant law references and avoid hallucination.
- No mock entries: all laws include summaries and official source links.

⏳ Next (Phase 3)
- Shareable, reproducible views (URL state)
- CSV export works across any filter set
- `last_verified` improves trust and dataset maintenance
- Expanded global coverage without degrading UX/performance
