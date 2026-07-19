from fastapi import FastAPI, APIRouter, HTTPException, Header, Depends
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import io
import csv
import json
import uuid
import logging
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone

from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

from ai_laws_data import EU_MEMBER_GEO_NAMES, COE_SIGNATORY_GEO_NAMES

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

DATA_AS_OF = "2025"                 # dataset reference period
DATA_LAST_VERIFIED = "2025-12-01"  # default provenance date for seed entries
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "ailaw-admin-2025")

# Seed dataset (built from the uploaded AI Act-Law Tracker.xlsx). Loaded into
# MongoDB on first startup; thereafter Mongo is the source of truth so admin
# edits persist. AI_LAWS is an in-memory mirror used for fast filtering.
with open(ROOT_DIR / "laws_dataset.json", "r", encoding="utf-8") as _f:
    SEED_LAWS = json.load(_f)

# Supplemental curated, publicly-sourced entries that fill gaps not covered by
# the original tracker (US Federal, US City/local, and notable proposed bills).
# Each carries source links + a "verify against primary source" note.
try:
    with open(ROOT_DIR / "seed_supplemental.json", "r", encoding="utf-8") as _f:
        SEED_LAWS = SEED_LAWS + json.load(_f)
except FileNotFoundError:
    pass


def _derive_level(law: dict) -> str:
    """Government level: Federal / State / City / National / International."""
    if law.get("level"):
        return law["level"]
    group = law.get("group")
    if group == "Multilateral":
        return "International"
    if group == "United States":
        return "State" if law.get("subnational") else "Federal"
    return "National"


for _l in SEED_LAWS:
    _l.setdefault("last_verified", DATA_LAST_VERIFIED)
    _l["level"] = _derive_level(_l)

AI_LAWS = list(SEED_LAWS)  # fallback until Mongo load completes on startup

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

app = FastAPI(title="Global AI Law Tracker API")
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


_country_index_cache = None  # invalidated on every reload_laws()


async def reload_laws():
    """Refresh the in-memory AI_LAWS mirror from MongoDB."""
    global AI_LAWS, _country_index_cache
    docs = await db.laws.find({}, {"_id": 0}).to_list(length=100000)
    for d in docs:
        d.setdefault("last_verified", DATA_LAST_VERIFIED)
        d["level"] = _derive_level(d)
    if docs:
        AI_LAWS = docs          # name-rebind is atomic under the asyncio loop
        _country_index_cache = None


DATASET_VERSION = "2025.4"  # bump to force a reseed when laws_dataset.json changes


@app.on_event("startup")
async def seed_and_load():
    meta = await db.meta.find_one({"key": "dataset_version"})
    if not meta or meta.get("value") != DATASET_VERSION:
        await db.laws.delete_many({})
        await db.laws.insert_many([dict(l) for l in SEED_LAWS])
        await db.meta.replace_one(
            {"key": "dataset_version"},
            {"key": "dataset_version", "value": DATASET_VERSION},
            upsert=True,
        )
        logger.info("Seeded %d laws (dataset %s)", len(SEED_LAWS), DATASET_VERSION)
    await reload_laws()
    logger.info("Loaded %d laws into memory", len(AI_LAWS))


def require_admin(x_admin_token: Optional[str] = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")
    return True


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
MATURITY_LABELS = {
    0: "No tracked AI law",
    1: "Emerging signals",
    2: "Developing framework",
    3: "Established regulation",
    4: "Comprehensive / multi-act",
}


_COMPREHENSIVE_KEYWORDS = (
    "broad ai governance", "comprehensive", "framework act", "ai act",
    "treaty", "regulation (eu)", "traiga", "raise act",
)


def _is_comprehensive(laws: List[dict]) -> bool:
    text = " ".join((l.get("category", "") + " " + l.get("title", "")) for l in laws).lower()
    return any(k in text for k in _COMPREHENSIVE_KEYWORDS)


def _enacted_score(enacted: List[dict], laws: List[dict]) -> int:
    if _is_comprehensive(laws) or len(enacted) >= 4:
        return 4
    return 3


def _proposed_score(proposed: List[dict]) -> int:
    if not proposed:
        return 0
    if _is_comprehensive(proposed):
        return 2
    return 1 if len(proposed) == 1 else 2


def compute_maturity(laws: List[dict]) -> int:
    """Score a jurisdiction's AI-regulation maturity from 0 (none) to 4 (comprehensive)."""
    if not laws:
        return 0
    enacted = [l for l in laws if l["status"] == "Enacted"]
    if enacted:
        return _enacted_score(enacted, laws)
    return _proposed_score([l for l in laws if l["status"] in ("Proposed", "Draft")])


def expand_geo_names(law: dict) -> List[str]:
    """Resolve supra-national placeholders to concrete map country names."""
    names = []
    for gn in law.get("geo_names", []):
        if gn == "__EU__":
            names.extend(EU_MEMBER_GEO_NAMES)
        elif gn == "__COE__":
            names.extend(COE_SIGNATORY_GEO_NAMES)
        else:
            names.append(gn)
    return names


def build_country_index():
    """Map geo country name -> list of applicable laws (incl. supra-national).
    Cached; invalidated whenever reload_laws() runs."""
    global _country_index_cache
    if _country_index_cache is not None:
        return _country_index_cache
    country_laws = defaultdict(list)
    for law in AI_LAWS:
        for gn in expand_geo_names(law):
            country_laws[gn].append(law)
    _country_index_cache = country_laws
    return country_laws


# --------------------------------------------------------------------------
# Pydantic models
# --------------------------------------------------------------------------
class ChatRequest(BaseModel):
    session_id: str = Field(default="default")
    message: str


class LawInput(BaseModel):
    country: str = Field(min_length=1)
    jurisdiction: Optional[str] = None
    subnational: Optional[str] = None
    region: str = "Multilateral"
    title: str = Field(min_length=1)
    status: str = "Enacted"
    category: str = "AI governance"
    year: int = Field(default=2025, ge=1900, le=2100)
    summary: str = ""
    authority: Optional[str] = ""
    source_url: Optional[str] = ""
    group: str = "International"

    @field_validator("country", "title")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()


def _geo_names_for(country: str, group: str) -> List[str]:
    if group == "United States":
        return ["United States of America"]
    special = {"European Union": "__EU__", "Council of Europe": "__COE__",
               "United States": "United States of America"}
    if country in special:
        return [special[country]]
    return [country]


def law_from_input(data: LawInput, existing: Optional[dict] = None) -> dict:
    base = dict(existing) if existing else {}
    base.update({
        "country": data.country,
        "jurisdiction": data.jurisdiction or data.country,
        "subnational": data.subnational,
        "region": data.region,
        "title": data.title,
        "status": data.status,
        "status_raw": data.status,
        "category": data.category,
        "year": data.year,
        "summary": data.summary,
        "authority": data.authority or data.country,
        "group": data.group,
        "geo_names": _geo_names_for(data.country, data.group),
        "sources": [{"title": "Source", "url": data.source_url}] if data.source_url else base.get("sources", []),
        "key_provisions": base.get("key_provisions", []),
        "type": base.get("type", "Law / bill"),
        "effective": base.get("effective", str(data.year)),
        "last_verified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    })
    if not base.get("id"):
        base["id"] = f"admin-{uuid.uuid4().hex[:12]}"
    base["level"] = _derive_level(base)
    return base


# --------------------------------------------------------------------------
# Data endpoints
# --------------------------------------------------------------------------
@api_router.get("/")
async def root():
    return {"message": "Global AI Law Tracker API", "laws_tracked": len(AI_LAWS)}


@dataclass
class LawFilterParams:
    """Grouped query params for law filtering (FastAPI dependency).

    Using a dataclass avoids a hand-written multi-argument constructor; FastAPI
    binds each field as an optional query parameter via Depends().
    """
    search: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    group: Optional[str] = None
    level: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    sort: Optional[str] = "newest"


# exact-match filters: (param attribute, law key)
_EXACT_FILTERS = [
    ("region", "region"), ("status", "status"), ("category", "category"),
    ("country", "country"), ("group", "group"), ("level", "level"),
]
# sort key -> (key function, reverse)
_SORTERS = {
    "oldest": (lambda l: (l["year"], l["title"]), False),
    "country": (lambda l: (l["country"], l.get("jurisdiction", "")), False),
    "newest": (lambda l: (l["year"], l["title"]), True),
}


def _match_search(law: dict, search: Optional[str]) -> bool:
    if not search:
        return True
    q = search.lower().strip()
    haystack = " ".join([
        law["title"], law.get("jurisdiction", ""), law["country"],
        law["summary"], law["category"], law["region"],
    ]).lower()
    return q in haystack


def _match_exact(law: dict, f: "LawFilterParams") -> bool:
    for attr, key in _EXACT_FILTERS:
        val = getattr(f, attr)
        if val and val != "all" and law.get(key) != val:
            return False
    return True


def _match_years(law: dict, f: "LawFilterParams") -> bool:
    if f.year_min is not None and law["year"] < f.year_min:
        return False
    if f.year_max is not None and law["year"] > f.year_max:
        return False
    return True


def _matches(law: dict, f: "LawFilterParams") -> bool:
    return (_match_search(law, f.search)
            and _match_exact(law, f)
            and _match_years(law, f))


def _filter_laws(f: "LawFilterParams") -> List[dict]:
    results = [l for l in AI_LAWS if _matches(l, f)]
    key, reverse = _SORTERS.get(f.sort or "newest", _SORTERS["newest"])
    return sorted(results, key=key, reverse=reverse)


@api_router.get("/laws")
async def get_laws(
    f: LawFilterParams = Depends(),
    limit: Optional[int] = 60,
    offset: int = 0,
):
    results = _filter_laws(f)
    total = len(results)
    page = results[offset: offset + limit] if limit is not None else results
    return {"count": total, "returned": len(page), "offset": offset, "laws": page}


@api_router.get("/laws/export")
async def export_laws(f: LawFilterParams = Depends()):
    """Export the currently filtered laws as CSV."""
    def _safe(val):
        # Prevent CSV/formula injection in spreadsheet apps.
        s = "" if val is None else str(val)
        if s and s[0] in ("=", "+", "-", "@"):
            return "'" + s
        return s

    rows = _filter_laws(f)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Jurisdiction", "Title", "Status", "Category", "Region",
                     "Year", "Authority", "Summary", "Source URL"])
    for l in rows:
        src = l["sources"][0]["url"] if l.get("sources") else ""
        writer.writerow([_safe(x) for x in [
            l.get("jurisdiction", l["country"]), l["title"], l["status"],
            l["category"], l["region"], l["year"], l.get("authority", ""),
            l["summary"], src,
        ]])
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ai_law_tracker_export.csv"},
    )


@api_router.get("/laws/{law_id}")
async def get_law(law_id: str):
    for law in AI_LAWS:
        if law["id"] == law_id:
            related = [
                {"id": l["id"], "title": l["title"], "country": l["country"], "status": l["status"]}
                for l in AI_LAWS
                if l["id"] != law_id and (l["country"] == law["country"] or l["category"] == law["category"])
            ][:5]
            return {**law, "related": related}
    raise HTTPException(status_code=404, detail="Law not found")


@api_router.get("/countries")
async def get_countries():
    """Map data: per geo country name, maturity + status counts."""
    country_laws = build_country_index()
    out = {}
    for name, laws in country_laws.items():
        counts = {"Enacted": 0, "Proposed": 0, "Draft": 0, "Superseded": 0}
        for l in laws:
            counts[l["status"]] = counts.get(l["status"], 0) + 1
        maturity = compute_maturity(laws)
        out[name] = {
            "name": name,
            "maturity": maturity,
            "maturity_label": MATURITY_LABELS[maturity],
            "total": len(laws),
            "counts": counts,
            "region": laws[0]["region"] if laws else None,
            "law_ids": [l["id"] for l in laws],
        }
    return out


@api_router.get("/countries/{name}")
async def get_country_detail(name: str):
    country_laws = build_country_index()
    laws = country_laws.get(name)
    if not laws:
        raise HTTPException(status_code=404, detail="No tracked laws for this country")
    maturity = compute_maturity(laws)
    seen, unique = set(), []
    for l in sorted(laws, key=lambda x: (x["year"], x["title"]), reverse=True):
        if l["id"] not in seen:
            seen.add(l["id"])
            unique.append(l)
    return {
        "name": name,
        "maturity": maturity,
        "maturity_label": MATURITY_LABELS[maturity],
        "total": len(unique),
        "laws": unique,
    }


@api_router.get("/stats")
async def get_stats():
    by_status = defaultdict(int)
    by_region = defaultdict(int)
    by_category = defaultdict(int)
    by_year = defaultdict(int)
    by_group = defaultdict(int)
    by_level = defaultdict(int)
    level_status = defaultdict(lambda: {"Enacted": 0, "Proposed": 0, "Draft": 0, "Superseded": 0})
    region_status = defaultdict(lambda: {"Enacted": 0, "Proposed": 0, "Draft": 0, "Superseded": 0})
    jurisdictions = set()

    for l in AI_LAWS:
        by_status[l["status"]] += 1
        by_region[l["region"]] += 1
        by_category[l["category"]] += 1
        by_year[l["year"]] += 1
        by_group[l.get("group", "Other")] += 1
        lvl = l.get("level", "National")
        by_level[lvl] += 1
        if l["status"] in level_status[lvl]:
            level_status[lvl][l["status"]] += 1
        region_status[l["region"]][l["status"]] += 1
        jurisdictions.add(l.get("jurisdiction", l["country"]))

    timeline = [{"year": y, "count": c} for y, c in sorted(by_year.items())]
    cum = 0
    for pt in timeline:
        cum += pt["count"]
        pt["cumulative"] = cum

    # top categories (dataset has 100+ granular categories)
    top_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:8]

    return {
        "total_laws": len(AI_LAWS),
        "total_jurisdictions": len(jurisdictions),
        "enacted": by_status.get("Enacted", 0),
        "proposed": by_status.get("Proposed", 0) + by_status.get("Draft", 0),
        "by_status": dict(by_status),
        "by_region": dict(by_region),
        "by_group": dict(by_group),
        "by_level": dict(by_level),
        "level_status": [{"level": lv, **counts} for lv, counts in level_status.items()],
        "by_category": dict(top_categories),
        "timeline": timeline,
        "region_status": [{"region": r, **counts} for r, counts in region_status.items()],
        "data_as_of": DATA_AS_OF,
    }


@api_router.get("/meta")
async def get_meta():
    regions = sorted({l["region"] for l in AI_LAWS})
    statuses = ["Enacted", "Proposed", "Draft", "Superseded"]
    categories = sorted({l["category"] for l in AI_LAWS})
    countries = sorted({l["country"] for l in AI_LAWS})
    groups = sorted({l.get("group", "Other") for l in AI_LAWS})
    level_order = ["Federal", "State", "City", "National", "International"]
    present_levels = {l.get("level", "National") for l in AI_LAWS}
    levels = [lv for lv in level_order if lv in present_levels]
    years = [l["year"] for l in AI_LAWS]
    return {
        "regions": regions,
        "statuses": statuses,
        "categories": categories,
        "countries": countries,
        "groups": groups,
        "levels": levels,
        "year_min": min(years),
        "year_max": max(years),
        "maturity_labels": MATURITY_LABELS,
        "data_as_of": DATA_AS_OF,
        "last_verified": DATA_LAST_VERIFIED,
    }


@api_router.get("/us-states")
async def get_us_states():
    """Per-US-state law counts + maturity for the US sub-map."""
    state_laws = defaultdict(list)
    for l in AI_LAWS:
        if l.get("group") == "United States" and l.get("subnational"):
            state_laws[l["subnational"]].append(l)
    out = {}
    for name, laws in state_laws.items():
        counts = {"Enacted": 0, "Proposed": 0, "Draft": 0, "Superseded": 0}
        for l in laws:
            counts[l["status"]] = counts.get(l["status"], 0) + 1
        out[name] = {
            "name": name,
            "total": len(laws),
            "counts": counts,
            "maturity": compute_maturity(laws),
        }
    return out


@api_router.get("/us-states/{name}")
async def get_us_state_detail(name: str):
    laws = [l for l in AI_LAWS if l.get("group") == "United States" and l.get("subnational") == name]
    if not laws:
        raise HTTPException(status_code=404, detail="No tracked laws for this state")
    laws = sorted(laws, key=lambda x: (x["year"], x["title"]), reverse=True)
    return {"name": name, "total": len(laws), "maturity": compute_maturity(laws), "laws": laws}


# --------------------------------------------------------------------------
# Admin CRUD (token-protected)
# --------------------------------------------------------------------------
@api_router.get("/admin/verify")
async def admin_verify(_: bool = Depends(require_admin)):
    return {"ok": True}


@api_router.post("/admin/laws")
async def admin_create_law(data: LawInput, _: bool = Depends(require_admin)):
    try:
        law = law_from_input(data)
        await db.laws.insert_one(dict(law))
        await reload_laws()
        return {"ok": True, "law": {k: v for k, v in law.items() if k != "_id"}}
    except Exception:
        logger.exception("Admin create failed")
        raise HTTPException(status_code=500, detail="Failed to create law")


@api_router.put("/admin/laws/{law_id}")
async def admin_update_law(law_id: str, data: LawInput, _: bool = Depends(require_admin)):
    existing = await db.laws.find_one({"id": law_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Law not found")
    try:
        law = law_from_input(data, existing)
        law["id"] = law_id
        await db.laws.replace_one({"id": law_id}, dict(law))
        await reload_laws()
        return {"ok": True, "law": {k: v for k, v in law.items() if k != "_id"}}
    except Exception:
        logger.exception("Admin update failed")
        raise HTTPException(status_code=500, detail="Failed to update law")


@api_router.delete("/admin/laws/{law_id}")
async def admin_delete_law(law_id: str, _: bool = Depends(require_admin)):
    try:
        res = await db.laws.delete_one({"id": law_id})
    except Exception:
        logger.exception("Admin delete failed")
        raise HTTPException(status_code=500, detail="Failed to delete law")
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Law not found")
    await reload_laws()
    return {"ok": True, "deleted": law_id}


# --------------------------------------------------------------------------
# AI Assistant (grounded, streaming)
# --------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are the AI Policy Assistant for 'Jerry's AI Law Observatory', a worldwide "
    "tracker of AI laws, acts, treaties and governance frameworks.\n\n"
    "Answer the user's question directly and factually. You have deep knowledge of "
    "global AI regulation — use it fully. A CONTEXT of tracked laws (numbered) is "
    "provided as helpful reference; draw on it when relevant, but also rely on your own "
    "well-established knowledge to give complete, accurate answers.\n\n"
    "Rules:\n"
    "- Just answer the question. Do NOT preface answers with meta-commentary about what "
    "the tracker does or does not contain (never say things like 'because the tracker "
    "context does not include X, I'll use general background'). Simply provide the facts.\n"
    "- Give real, concrete detail — e.g., for the EU AI Act explain its risk tiers "
    "(unacceptable, high, limited, minimal), key obligations, general-purpose AI rules, "
    "penalties and phased timeline; for comparisons, state each jurisdiction's actual "
    "approach.\n"
    "- You may cite tracked entries inline like [1], [2] when you use them, but citations "
    "are optional and should never replace a substantive answer.\n"
    "- Be accurate: don't invent precise article numbers, figures or dates you're unsure "
    "of. If you genuinely don't know something specific, briefly say so and still give "
    "the best factual overview you can — without blaming the tracker.\n"
    "- Prefer a short intro, then bullet points for key provisions, and a one-line "
    "takeaway when useful. Neutral, professional, knowledgeable tone."
)


def select_relevant_laws(query: str, limit: int = 8) -> List[dict]:
    q = query.lower()
    terms = [t for t in ''.join(c if c.isalnum() else ' ' for c in q).split() if len(t) > 2]
    scored = []
    for law in AI_LAWS:
        haystack = " ".join([
            law["country"], law["title"], law["summary"],
            law["category"], law["region"], law["status"],
        ]).lower()
        score = sum(haystack.count(t) for t in terms)
        if law["country"].lower() in q:
            score += 5
        scored.append((score, law))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [law for s, law in scored if s > 0][:limit]
    if not top:
        top = AI_LAWS[:limit]
    return top


def build_context(laws: List[dict]):
    lines, refs = [], []
    for i, law in enumerate(laws, 1):
        parts = [
            f"[{i}] {law.get('jurisdiction') or law['country']} — {law['title']}",
            f"Status: {law['status']} ({law['year']}) | Category: {law['category']} | "
            f"Region: {law['region']}",
        ]
        if law.get("authority"):
            parts.append(f"Authority: {law['authority']}")
        parts.append(f"Summary: {law['summary']}")
        if law.get("key_provisions"):
            parts.append("Key provisions: " + "; ".join(law["key_provisions"]))
        if law.get("sources"):
            parts.append(f"Source: {law['sources'][0].get('url', '')}")
        lines.append("\n".join(parts))
        refs.append({
            "index": i, "id": law["id"], "title": law["title"],
            "country": law.get("jurisdiction") or law["country"],
            "status": law["status"], "year": law["year"],
        })
    return "\n\n".join(lines), refs


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


async def _store_message(session_id: str, role: str, content: str) -> None:
    try:
        await db.chat_messages.insert_one({
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    except Exception:
        logger.exception("Failed to persist %s message", role)


async def _recent_history_text(session_id: str) -> str:
    history = await db.chat_messages.find(
        {"session_id": session_id}, {"_id": 0}
    ).sort("timestamp", -1).to_list(6)
    history = list(reversed(history))
    if len(history) <= 1:
        return ""
    prev = history[:-1][-4:]
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in prev)


def _build_prompt(message: str, context: str, history_text: str) -> str:
    return (
        f"CONTEXT (tracked AI laws):\n{context}\n\n"
        + (f"RECENT CONVERSATION:\n{history_text}\n\n" if history_text else "")
        + f"USER QUESTION: {message}"
    )


async def _stream_answer(session_id: str, prompt: str, refs: list):
    yield _sse({"type": "refs", "refs": refs})
    collected = []
    try:
        chat_client = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=SYSTEM_PROMPT,
        ).with_model("openai", "gpt-5.4")
        async for event in chat_client.stream_message(UserMessage(text=prompt)):
            if isinstance(event, TextDelta):
                collected.append(event.content)
                yield _sse({"type": "delta", "content": event.content})
            elif isinstance(event, StreamDone):
                break
    except Exception:
        logger.exception("Chat streaming error")
        yield _sse({"type": "error", "message": "The assistant is temporarily unavailable. Please try again."})

    answer = "".join(collected)
    if answer:
        await _store_message(session_id, "assistant", answer)
    yield _sse({"type": "done"})


@api_router.post("/chat")
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")

    context, refs = build_context(select_relevant_laws(req.message))
    await _store_message(req.session_id, "user", req.message)
    history_text = await _recent_history_text(req.session_id)
    prompt = _build_prompt(req.message, context, history_text)

    return StreamingResponse(
        _stream_answer(req.session_id, prompt, refs),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"},
    )


@api_router.get("/chat/history/{session_id}")
async def chat_history(session_id: str):
    msgs = await db.chat_messages.find(
        {"session_id": session_id}, {"_id": 0}
    ).sort("timestamp", 1).to_list(200)
    return {"messages": msgs}


# --------------------------------------------------------------------------
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
