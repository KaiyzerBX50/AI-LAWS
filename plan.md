# plan.md

## 1. Objectives
- Build a worldwide, interactive tracker for AI-related laws/acts/regulations with a professional UI.
- Provide two exploration modes: clickable world map + searchable/filterable list.
- Include detail views with accurate summaries + source links (no mock data).
- Add an LLM-powered AI Assistant (Emergent key) to answer questions and summarize regulations.
- Support smooth Day/Night mode with persisted preference.

## 2. Implementation Steps

### Phase 1 — Core POC (LLM Integration in Isolation)
**Goal:** Prove AI Assistant works reliably before building the full app.
- Web-research best practices for: emergentintegrations LLM usage, prompt patterns for policy Q&A, and safe citation behavior.
- Create a minimal Python test script:
  - Call Emergent LLM (pick a stable default model).
  - Provide a system prompt: “You are an AI policy assistant; be factual; if unsure say so; prefer citing provided sources.”
  - Pass a small curated context bundle (3–5 laws) and ask 5 test questions.
  - Validate: response structure, latency, errors, token limits.
- Iterate prompt + response formatting until stable.
- Define the backend contract for chat endpoint (request/response JSON schema).

**POC exit criteria:** consistent answers, graceful “unknown,” and predictable JSON output.

---

### Phase 2 — V1 App Development (Map + Tracker + Assistant + Theme)
**Backend (FastAPI + MongoDB)**
- Data model: `Country`, `LawEntry` (country, region, title, status, category, year, summary, key_provisions[], sources[]).
- Seed database with a curated, real dataset (initial coverage: EU, US, UK, China, Canada, Brazil, Japan, South Korea, India, Australia, Singapore, UAE + a few more).
- API endpoints (MVP):
  - `GET /laws` (query params: search, region, status, category, year, country)
  - `GET /laws/{id}`
  - `GET /countries` (for map + filters)
  - `GET /stats` (counts by status/region/category)
  - `POST /chat` (uses proven POC prompt + optionally injects relevant laws from DB)
- Basic input validation, pagination for list endpoint.

**Frontend (React + shadcn/ui + react-simple-maps + recharts)**
- App shell with persisted theme toggle (localStorage) + accessible contrast.
- Primary navigation: Map | List | Timeline | Compare | Assistant.
- Map view:
  - World map with countries clickable.
  - Color scale by “regulation maturity” derived from statuses present (e.g., enacted vs proposed).
  - On click: drawer/modal with country overview + its laws.
- List view:
  - Search bar + filters (region/status/category/year) + sortable cards.
  - Card opens detail modal/page (summary, key provisions, sources).
- Timeline view (MVP):
  - Global timeline by year (counts) + optional country filter.
- Compare view (MVP):
  - Select 2–3 countries, show side-by-side: key laws, statuses, notable provisions.
- AI Assistant view:
  - Chat UI with “suggested questions.”
  - Responses include: answer + “Relevant laws used” (links to entries).
- Stats dashboard (MVP):
  - Total laws, countries covered, enacted vs proposed counts, top regions.

**End of Phase 2:** run 1 full end-to-end testing pass (core flows + cross-browser sanity).

**Phase 2 user stories (at least 5)**
1. As a user, I can click a country on the world map and immediately see its AI-related laws.
2. As a user, I can toggle Day/Night mode and my choice persists after refresh.
3. As a user, I can search and filter laws by region, status, category, and year.
4. As a user, I can open a law detail view to read key provisions and verify sources.
5. As a user, I can ask the AI Assistant a question and get a grounded summary with relevant law references.
6. As a user, I can view a timeline of AI regulations to understand how they evolved over time.
7. As a user, I can compare 2–3 countries side by side to understand differences quickly.

---

### Phase 3 — Enhancements (Quality + Coverage + UX)
- Expand curated dataset coverage (more countries, more sectoral rules, updated statuses) + add “last verified” date.
- Improve AI Assistant grounding:
  - Retrieve relevant laws via keyword + country filter, inject as context.
  - Add “cannot verify” guardrails and explicit source-linking.
- Add export/share:
  - Copy link to filtered views, export filtered results to CSV.
- UI polish:
  - Better map legend, empty states, loading skeletons, and mobile responsiveness.
- Performance:
  - Caching for `/laws` queries; index MongoDB fields.

**End of Phase 3:** run 1 full end-to-end testing pass.

**Phase 3 user stories (at least 5)**
1. As a user, I can share a link that preserves my current filters and selected country.
2. As a user, I can export filtered law results to CSV for offline analysis.
3. As a user, I can see when an entry was last verified so I can trust freshness.
4. As a user, I can ask country-specific questions and the assistant focuses on that jurisdiction.
5. As a user, I get clear empty/loading states so the app feels fast and reliable.

---

### Phase 4+ — Optional (Admin + Auth)
- Add admin-only authentication to manage/curate entries (create/edit/update sources) after user approval.
- Add audit trail for edits + moderation workflow.

**Phase 4 user stories (at least 5)**
1. As an admin, I can add a new law with sources so the database stays current.
2. As an admin, I can update a law’s status (draft → proposed → enacted) with a timestamp.
3. As an admin, I can flag entries as “needs review” to maintain quality.
4. As an admin, I can bulk import laws from a CSV template.
5. As a user, I can trust that displayed entries have a clear provenance and update history.

## 3. Next Actions
1. Implement Phase 1 Python POC with Emergent LLM and lock the `/chat` JSON schema.
2. Curate and format the initial seed dataset (minimum: ~25–40 entries across target jurisdictions).
3. Build FastAPI endpoints + Mongo indexes + seed script.
4. Build React UI: theme toggle, map view, list+filters, detail view, assistant chat.
5. Run end-to-end testing; fix before expanding scope.

## 4. Success Criteria
- LLM POC consistently returns usable, structured answers with graceful failure modes.
- V1 app supports map click → laws list → detail view without dead ends.
- Filters/search respond correctly and quickly (reasonable pagination).
- Day/Night mode is smooth, accessible, and persists.
- AI Assistant answers include relevant law references and do not hallucinate when uncertain.
- No mock entries: all laws have accurate summaries and source links.