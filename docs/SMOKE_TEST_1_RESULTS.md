# Smoke Test 1 — Sonnet Plumbing

**Date:** 2026-04-23
**Model:** claude-sonnet-4-6
**Draft:** tests/smoke_test_draft_minimal.txt (~500 tokens, synthetic LPBBTI draft)
**Duration:** ~6 hours total (includes setup, debugging, and two verified API calls)
**Cost:** ~$0.56 confirmed (R1 + R2); total session estimate ~$1.80 including failed warm-up attempts

---

## Plumbing Checklist

- [x] Backend 3 endpoints work (`/health`, `/corpus/manifest`, `/corpus/preset/pojk-40-2024`)
- [x] Frontend loads, no JS error (F12 Console clean)
- [x] SSE connection established
- [x] Reasoning text streams in UI (token-by-token, monospace box)
- [x] `<findings>` JSON parsed
- [x] Findings cards render with severity badges
- [x] Request 1: `cache_read_input_tokens = 409,540` (corpus cached, full hit)
- [x] Request 2: `cache_read_input_tokens = 409,540` (cache hit confirmed)
- [x] Total spent: <$3

**Result: PASS**

---

## Cache Performance

| | Request 1 | Request 2 |
|---|---|---|
| `cache_creation_input_tokens` | 0 | 1,311 |
| `cache_read_input_tokens` | 409,540 | 409,540 |
| `input_tokens` | 1,314 | 3 |
| `output_tokens` | 10,458 | 9,980 |
| Elapsed | 170.4s | 166.0s |
| Est. cost | ~$0.28 | ~$0.28 |

**Cache hit rate: 100%** on corpus (409,540 tokens read from cache both calls).

Note: Initial corpus cache write (`cache_creation ~409K`) occurred during warm-up calls
earlier in the session. By the time R1/R2 ran, corpus was already fully cached.
R2's `cache_creation=1,311` is the user-message block being cached on second call.

Cache TTL: 1 hour (extended via `anthropic-beta: extended-cache-ttl-2025-04-11` + `"ttl": "1h"`).

**Effective input cost vs uncached:**
- Uncached: 409,540 × $3.00/MTok = ~$1.23 per call
- Cached:   409,540 × $0.30/MTok = ~$0.12 per call
- **Savings: ~90% on corpus input tokens**

---

## Findings Output — Quality Note

> NOTE: Sonnet quality NOT evaluated here — plumbing only.

R1 returned **4 findings** (critical × 1, major × 2, minor × 1).
R2 returned **3 findings** (critical × 1, major × 1, minor × 1).

Minor variation between calls is expected (non-deterministic sampling). Full quality
evaluation is reserved for Smoke Test 2 with Opus 4.7 against ground truth.

---

## Issues Found & Resolved

1. **`findings JSON malformed` (4-5 failed calls)**
   - Cause: Sonnet 4.6 wrapped `<findings>` JSON in markdown code fences (` ```json ... ``` `)
   - Fix: Added regex strip in `parse_findings()` in `backend/prompt_loader.py`
   - Status: RESOLVED

2. **`ANTHROPIC_API_KEY not configured` (first backend start)**
   - Cause: Backend process started before `.env` was created; `load_dotenv()` only runs once at startup
   - Fix: Kill stale process, restart backend fresh after `.env` populated
   - Status: RESOLVED

3. **Stale backend process (old version without `/corpus/preset/` endpoint)**
   - Cause: Old uvicorn instance survived from before MT-3.2 deployment
   - Fix: Force-killed orphan worker processes, started fresh
   - Status: RESOLVED

---

## Ready for Smoke Test 2 (Opus)?

- [x] Yes — plumbing confirmed, cache warm, cost within budget

**Pre-conditions for Smoke Test 2:**
- Use `corpus/active/POJK-40-2024.txt` as draft (retrospective validation)
- Switch model toggle to `claude-opus-4-7`
- Corpus cache already warm from this session (re-warm if >1 hour elapsed)
- Expected output: ≥1 normative, ≥1 hierarchical, ≥1 operational finding
- Compare against `ground-truth/manual-analysis.md` for quality evaluation
