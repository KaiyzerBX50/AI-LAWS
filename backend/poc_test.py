"""
POC: AI Assistant for global AI-law/regulation Q&A.
Validates:
 1. Emergent LLM key + emergentintegrations works (gpt-5.4).
 2. Grounded answers using injected law context.
 3. Graceful "I don't know" when info is outside provided context.
 4. Streaming works (for real app SSE).
"""
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

# Small curated context bundle simulating what backend will inject from Mongo
LAW_CONTEXT = """
[1] EU — EU AI Act (Regulation 2024/1689) | Status: Enacted (2024) | Category: Comprehensive
Summary: World's first comprehensive AI law. Risk-based approach classifying AI systems into
unacceptable, high, limited, and minimal risk. Bans certain uses (social scoring, real-time
biometric ID with exceptions). High-risk systems face conformity assessments. Phased entry
into force 2025-2027.

[2] United States — Executive Order 14110 on Safe, Secure, and Trustworthy AI | Status: Enacted (2023) | Category: Executive/Sectoral
Summary: Directed federal agencies to develop AI safety standards, required safety test
result reporting for powerful models under the Defense Production Act, and addressed privacy,
equity, and workforce. (Note: partially rescinded/revised by subsequent administrations.)

[3] China — Interim Measures for the Management of Generative AI Services | Status: Enacted (2023) | Category: Generative AI
Summary: Requires generative AI providers to ensure content aligns with core socialist values,
conduct security assessments, label AI-generated content, and protect personal data.
"""

SYSTEM_PROMPT = (
    "You are an AI Policy Assistant for a worldwide AI-law tracker. "
    "Answer factually and concisely about AI laws, acts, and regulations. "
    "You are given a CONTEXT list of laws. Prefer grounding your answers in this context and "
    "cite entries like [1], [2]. If the answer is not in the context and you are not confident, "
    "say you don't have verified information rather than guessing."
)

QUESTIONS = [
    "What is the EU AI Act and what approach does it take?",
    "How does China regulate generative AI?",
    "Compare the US and EU approaches to AI regulation based on the context.",
    "What are the exact penalty amounts in the fictional AI law of Atlantis?",  # should say unknown
    "Which of the listed laws are already enacted?",
]


async def ask(question: str, use_stream: bool = True) -> str:
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id="poc-session",
        system_message=SYSTEM_PROMPT,
    ).with_model("openai", "gpt-5.4")

    prompt = f"CONTEXT:\n{LAW_CONTEXT}\n\nQUESTION: {question}"
    msg = UserMessage(text=prompt)

    if use_stream:
        chunks = []
        async for event in chat.stream_message(msg):
            if isinstance(event, TextDelta):
                chunks.append(event.content)
            elif isinstance(event, StreamDone):
                break
        return "".join(chunks)
    else:
        return await chat.send_message(msg)


async def main():
    print("=== AI Policy Assistant POC ===")
    print(f"Key present: {bool(EMERGENT_LLM_KEY)}\n")
    passed = 0
    for i, q in enumerate(QUESTIONS, 1):
        try:
            ans = await ask(q, use_stream=True)
            ok = bool(ans and len(ans.strip()) > 5)
            if ok:
                passed += 1
            print(f"[Q{i}] {q}")
            print(f"  -> {ans.strip()[:400]}")
            print(f"  STATUS: {'PASS' if ok else 'FAIL (empty)'}\n")
        except Exception as e:
            print(f"[Q{i}] {q}\n  ERROR: {type(e).__name__}: {e}\n")
    print(f"=== RESULT: {passed}/{len(QUESTIONS)} produced answers ===")


if __name__ == "__main__":
    asyncio.run(main())
