from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import io
import csv
import json
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
from collections import defaultdict
from datetime import datetime, timezone

from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

from ai_laws_data import EU_MEMBER_GEO_NAMES, COE_SIGNATORY_GEO_NAMES

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Load the full curated dataset (built from the uploaded AI Act-Law Tracker.xlsx)
with open(ROOT_DIR / "laws_dataset.json", "r", encoding="utf-8") as _f:
    AI_LAWS = json.load(_f)

DATA_AS_OF = "2025"  # dataset reference period

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


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
VOLUNTARY_CATEGORIES = {
    "Voluntary Framework", "National Strategy", "Advisory",
    "Framework", "Innovation / Soft-law", "Data Privacy / Guidance",
}

MATURITY_LABELS = {
    0: "No tracked AI law",
    1: "Emerging signals",
    2: "Developing framework",
    3: "Established regulation",
    4: "Comprehensive / multi-act",
}


def compute_maturity(laws: List[dict]) -> int:
    if not laws:
        return 0
    enacted = [l for l in laws if l["status"] == "Enacted"]
    proposed = [l for l in laws if l["status"] in ("Proposed", "Draft")]
    text = " ".join((l.get("category", "") + " " + l.get("title", "")) for l in laws).lower()
    comprehensive = any(k in text for k in [
        "broad ai governance", "comprehensive", "framework act", "ai act",
        "treaty", "regulation (eu)", "traiga", "raise act",
    ])
    if enacted and comprehensive:
        return 4
    if len(enacted) >= 4:
        return 4
    if len(enacted) >= 1:
        return 3
    if any("comprehensive" in (l.get("category", "") + l.get("title", "")).lower() for l in proposed):
        return 2
    if proposed:
        return 1 if len(proposed) == 1 else 2
    return 0


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
    """Map geo country name -> list of applicable laws (incl. supra-national)."""
    country_laws = defaultdict(list)
    for law in AI_LAWS:
        for gn in expand_geo_names(law):
            country_laws[gn].append(law)
    return country_laws


# --------------------------------------------------------------------------
# Pydantic models
# --------------------------------------------------------------------------
class ChatRequest(BaseModel):
    session_id: str = Field(default="default")
    message: str


# --------------------------------------------------------------------------
# Data endpoints
# --------------------------------------------------------------------------
@api_router.get("/")
async def root():
    return {"message": "Global AI Law Tracker API", "laws_tracked": len(AI_LAWS)}


@api_router.get("/laws")
async def get_laws(
    search: Optional[str] = None,
    region: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    group: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    sort: Optional[str] = "newest",
    limit: Optional[int] = 60,
    offset: Optional[int] = 0,
):
    results = _filter_laws(search, region, status, category, country, group, year_min, year_max, sort)
    total = len(results)
    if limit is not None:
        page = results[offset: offset + limit]
    else:
        page = results
    return {"count": total, "returned": len(page), "offset": offset, "laws": page}


def _filter_laws(search, region, status, category, country, group, year_min, year_max, sort):
    results = list(AI_LAWS)
    if search:
        q = search.lower().strip()
        results = [
            l for l in results
            if q in l["title"].lower()
            or q in l.get("jurisdiction", "").lower()
            or q in l["country"].lower()
            or q in l["summary"].lower()
            or q in l["category"].lower()
            or q in l["region"].lower()
        ]
    if region and region != "all":
        results = [l for l in results if l["region"] == region]
    if status and status != "all":
        results = [l for l in results if l["status"] == status]
    if category and category != "all":
        results = [l for l in results if l["category"] == category]
    if country and country != "all":
        results = [l for l in results if l["country"] == country]
    if group and group != "all":
        results = [l for l in results if l.get("group") == group]
    if year_min is not None:
        results = [l for l in results if l["year"] >= year_min]
    if year_max is not None:
        results = [l for l in results if l["year"] <= year_max]

    if sort == "oldest":
        results = sorted(results, key=lambda l: (l["year"], l["title"]))
    elif sort == "country":
        results = sorted(results, key=lambda l: (l["country"], l.get("jurisdiction", "")))
    else:
        results = sorted(results, key=lambda l: (l["year"], l["title"]), reverse=True)
    return results


@api_router.get("/laws/export")
async def export_laws(
    search: Optional[str] = None,
    region: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    group: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    sort: Optional[str] = "newest",
):
    """Export the currently filtered laws as CSV."""
    rows = _filter_laws(search, region, status, category, country, group, year_min, year_max, sort)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Jurisdiction", "Title", "Status", "Category", "Region",
                     "Year", "Authority", "Summary", "Source URL"])
    for l in rows:
        src = l["sources"][0]["url"] if l.get("sources") else ""
        writer.writerow([
            l.get("jurisdiction", l["country"]), l["title"], l["status"],
            l["category"], l["region"], l["year"], l.get("authority", ""),
            l["summary"], src,
        ])
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
    region_status = defaultdict(lambda: {"Enacted": 0, "Proposed": 0, "Draft": 0, "Superseded": 0})
    jurisdictions = set()

    for l in AI_LAWS:
        by_status[l["status"]] += 1
        by_region[l["region"]] += 1
        by_category[l["category"]] += 1
        by_year[l["year"]] += 1
        by_group[l.get("group", "Other")] += 1
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
    years = [l["year"] for l in AI_LAWS]
    return {
        "regions": regions,
        "statuses": statuses,
        "categories": categories,
        "countries": countries,
        "groups": groups,
        "year_min": min(years),
        "year_max": max(years),
        "maturity_labels": MATURITY_LABELS,
        "data_as_of": DATA_AS_OF,
    }


# --------------------------------------------------------------------------
# AI Assistant (grounded, streaming)
# --------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are the AI Policy Assistant for a worldwide tracker of AI laws, acts and "
    "regulations. Answer factually, clearly and concisely about global AI regulation. "
    "You are given a CONTEXT of tracked laws with numbered references. Ground your "
    "answers in this context and cite entries inline like [1], [2]. If the answer is "
    "not covered by the context and you are not confident, say you do not have verified "
    "information rather than guessing. Use short paragraphs and bullet points. Keep a "
    "neutral, professional tone."
)


def select_relevant_laws(query: str, limit: int = 6) -> List[dict]:
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
        lines.append(
            f"[{i}] {law['country']} — {law['title']} | Status: {law['status']} "
            f"({law['year']}) | Category: {law['category']}\n{law['summary']}"
        )
        refs.append({
            "index": i, "id": law["id"], "title": law["title"],
            "country": law["country"], "status": law["status"], "year": law["year"],
        })
    return "\n\n".join(lines), refs


@api_router.post("/chat")
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")

    relevant = select_relevant_laws(req.message)
    context, refs = build_context(relevant)

    await db.chat_messages.insert_one({
        "session_id": req.session_id,
        "role": "user",
        "content": req.message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    history = await db.chat_messages.find(
        {"session_id": req.session_id}, {"_id": 0}
    ).sort("timestamp", -1).to_list(6)
    history = list(reversed(history))
    history_text = ""
    if len(history) > 1:
        prev = history[:-1][-4:]
        history_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in prev)

    prompt = (
        f"CONTEXT (tracked AI laws):\n{context}\n\n"
        + (f"RECENT CONVERSATION:\n{history_text}\n\n" if history_text else "")
        + f"USER QUESTION: {req.message}"
    )

    async def event_generator():
        yield f"data: {json.dumps({'type': 'refs', 'refs': refs})}\n\n"
        collected = []
        try:
            chat_client = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=req.session_id,
                system_message=SYSTEM_PROMPT,
            ).with_model("openai", "gpt-5.4")
            async for event in chat_client.stream_message(UserMessage(text=prompt)):
                if isinstance(event, TextDelta):
                    collected.append(event.content)
                    yield f"data: {json.dumps({'type': 'delta', 'content': event.content})}\n\n"
                elif isinstance(event, StreamDone):
                    break
        except Exception as e:
            logger.exception("Chat streaming error")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        answer = "".join(collected)
        if answer:
            await db.chat_messages.insert_one({
                "session_id": req.session_id,
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
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
