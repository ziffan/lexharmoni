# CLAUDE.md — LexHarmoni Session Guide

AI-powered regulatory stress-testing platform for Indonesian OJK/LPBBTI regulations.
Detects normative, hierarchical, and operational friction using Claude Opus 4.7 with prompt caching.

---

## Quick Start

```bash
# Terminal 1 — Backend
cd backend
./venv/Scripts/uvicorn main:app --reload   # Windows venv

# Terminal 2 — Frontend
cd frontend
npm run dev
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Health check: GET http://localhost:8000/health

**Required:** `backend/.env` with `ANTHROPIC_API_KEY=sk-ant-...`
(file exists, not committed — ask user to verify if missing)

---

## Project Structure

```
corpus/
  active/       POJK-22-2023, POJK-40-2024, SEOJK-19-2025  ← DO NOT MODIFY
  historical/   POJK-77-2016, POJK-31-2020, POJK-10-2022, SEOJK-19-2023  ← DO NOT MODIFY
  manifest.json
backend/
  main.py           FastAPI app — /health, /corpus/manifest, /corpus/preset/pojk-40-2024, /analyze (SSE)
  prompt_loader.py  System blocks, build_user_message(), parse_findings()
  requirements.txt
frontend/
  app/page.tsx      Full single-file client component (light-canvas theme)
ground-truth/
  manual-analysis.md  Hand-authored friction analysis — ground truth for quality evaluation
docs/
  SMOKE_TEST_1_RESULTS.md
  SMOKE_TEST_2_RESULTS.md
  BUDGET_TRACKER.md
  INTEGRATION_SPEC_MT-3.2_MT-4.2.md
tests/
  smoke_test_draft_minimal.txt  ← DO NOT MODIFY (500-token synthetic draft for plumbing tests)
```

---

## Key Technical Details

### Model
- **Default:** `claude-opus-4-7` (set in `AnalyzeRequest.model`)
- **Max output:** 128,000 tokens (verified from official docs)
- **Pricing:** $5/MTok input, $25/MTok output, $0.50/MTok cache read
- Sonnet 4.6 also available via dropdown for cheaper testing: $3/$15/$0.30

### Prompt Caching
- 4 system blocks, each with `cache_control: {"type": "ephemeral", "ttl": "1h"}`
- Beta header: `anthropic-beta: extended-cache-ttl-2025-04-11`
- Corpus size: ~409,540 tokens (confirmed from cache_read stats)
- **Caches are model-specific** — Sonnet and Opus maintain separate caches
- First call after >1h = cache write (~$2.05 for corpus); subsequent calls = cache read (~$0.20)

### SSE Endpoint (`/analyze`)
- Uses synchronous `anthropic.Anthropic` client + `client.messages.stream()` inside async FastAPI generator
- Events: `reasoning` (streaming text), `findings` (JSON), `error`, `done`
- `full_text` accumulates all streaming chunks; `parse_findings()` called after stream ends

### Findings Parsing
- Model output: `<reasoning>...</reasoning>` then `<findings>...</findings>`
- `parse_findings()` strips markdown code fences before `json.loads()` (some models wrap JSON in ` ```json ``` `)
- Schema: `findings[]` with `id`, `type`, `severity`, `title`, `summary`, `affected_regulations`, `reasoning_steps`, `temporal_window`, `recommended_resolution`, `confidence`

### Frontend SSE Parsing
- Manual parsing via `fetch()` + `ReadableStream` reader (not `EventSource`)
- Tracks `currentEvent` across newline-delimited chunks
- `data:` lines decoded per event type

---

## Known Issues & Status

| Issue | Status | Fix |
|---|---|---|
| `cache_stats.log` not written after uvicorn hot-reload | ✅ Fixed | Changed path from `Path(__file__).parent` to `BASE / "backend"` — needs verification in next run |
| Severity calibration: F001 normative→should be critical | ⚠️ Pending | Add explicit type→severity constraint in `build_user_message()` prompt |
| Findings count non-deterministic (4–5 across runs) | ℹ️ Expected | Stochastic sampling; 3 core frictions are always present |

---

## Corpus — IMMUTABLE

The 7 regulation files in `corpus/active/` and `corpus/historical/` are the ground truth corpus.
**Do not modify them.** If corpus changes are needed, treat as a new milestone (MT-x.x).

Corpus integrity: run `python tests/validate_corpus.py` to check against `manifest.json`.

---

## Smoke Test Status

| Test | Model | Result | Date |
|---|---|---|---|
| ST1 — Sonnet plumbing | Sonnet 4.6 | ✅ PASS | 2026-04-23 |
| ST2 — Opus quality (3 runs) | Opus 4.7 | ✅ PASS | 2026-04-23 |

**ST2 key finding:** 3/3 ground-truth frictions found in every run. Severity of anchor finding (collection hours conflict) fluktuatif: 1× major, 2× critical across 3 runs. Prompt fix pending.

---

## Budget (2026-04-23)

Total spent today: ~$26.00 (API ~$5.39 + Claude Code ~$20.61)
See `docs/BUDGET_TRACKER.md` for per-call breakdown.

---

## Pending Work (Next Session)

1. **Prompt fix — severity calibration**: add to `build_user_message()` in `prompt_loader.py`:
   > "Severity MUST follow type: normative → critical, hierarchical → major, operational → minor. Do not override based on perceived mitigation."

2. **Verify `cache_stats.log`**: run one analysis and confirm file appears at `backend/cache_stats.log`

3. **Demo prep**: decide which of the 3 consistent findings to script for demo narrative

---

## Git

- Remote: https://github.com/ziffan/hackathon.opus47.git
- Branch: `master`
- License: Apache 2.0 (headers on all `.py` files)
- History is clean — sensitive strings removed via filter-branch in earlier session
