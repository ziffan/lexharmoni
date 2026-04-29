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
tests/
  smoke_test_draft_minimal.txt  ← DO NOT MODIFY (500-token synthetic draft for plumbing tests)
.github/
  workflows/ci.yml        Primary CI (lint, type-check, build, hygiene)
  workflows/security.yml  Security scan (pip-audit, npm audit, gitleaks) — weekly + on PR
  dependabot.yml          Auto-update PRs for pip/npm/github-actions — weekly Monday
pyproject.toml            ruff, mypy, pytest baseline config
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
- First call after >1h = cache write (~$5.55 for corpus, Opus 4.7); subsequent calls = cache read (~$0.28); total per-run warm = ~$1.70

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

## CI/CD

### Workflows

| Workflow | Trigger | Jobs |
|---|---|---|
| `ci.yml` | push/PR → master | backend-lint-and-test, frontend-lint-and-build, repo-hygiene |
| `security.yml` | weekly Mon 06:00 UTC, PR → master, manual | python-deps-audit, node-deps-audit, secret-scan |

**CI jobs detail:**
- `backend-lint-and-test`: ruff check + format, mypy, pytest (exit-5 tolerant — no pytest-discoverable tests yet)
- `frontend-lint-and-build`: `npm ci` → `npm run lint` (ESLint 9 flat config) → `npm run build`
- `repo-hygiene`: `python scripts/validate_manifest.py` → `python scripts/add_license_headers.py --check` → lychee offline link check

**Tool config (`pyproject.toml`):**
- ruff: `select = ["E","F"]`, `ignore = ["E501"]`, `line-length = 100`, `target-version = "py311"`
- mypy: `ignore_missing_imports = true`, `follow_imports = "silent"` (no strict mode)
- pytest marker: `requires_api` — tag tests that need ANTHROPIC_API_KEY so CI can skip them

### Dependabot PRs — current state (2026-04-29)

github-actions bumps (#2–#4) merged immediately. All pip/npm PRs **intentionally deferred** to v0.2.0:

| PR | Update | Why deferred |
|---|---|---|
| #8 | `anthropic` ≥0.39.0 → ≥0.97.0 | 58-minor-version jump; breaking changes in streaming/beta headers likely |
| #10 | `eslint` 9 → 10 | Major version; may break lint step |
| #6 | `typescript` 5 → 6 | Major version; may introduce type errors |
| #9 | `@types/node` 20 → 25 | Large jump; may conflict with Node 20 CI runtime |
| #11, #12 | `react`/`react-dom` patch | Safe but needs UI smoke test |
| #5, #7 | `sse-starlette`, `python-dotenv` | Minor; low risk but no urgency |

Full rationale in `DECISIONS.md`. Do not merge these without explicit decision and CI verification.

---

## Known Issues & Status

| Issue | Status | Fix |
|---|---|---|
| `cache_stats.log` not written after uvicorn hot-reload | ✅ Fixed + Verified | `BASE / "backend"` path — 5+ entries confirmed written |
| Severity calibration: normative→critical | ✅ Fixed + Verified | Severity lock patch in `prompt_loader.py` — PASS 2/2 post-patch runs |
| Streaming all-at-once (React 19 auto-batching) | ✅ Fixed + Verified | `useRef` accumulator + `setInterval(60ms)` drain; CRLF `.replace(/\r$/, '')` |
| `<reasoning>` tag visible / broken words | ✅ Fixed + Verified | CRLF strip + tag-strip regex with space normalization |
| Findings count non-deterministic (4–5 across runs) | ℹ️ Expected | Stochastic sampling; 3 core frictions always present |

---

## Corpus — IMMUTABLE

The 7 regulation files in `corpus/active/` and `corpus/historical/` are the ground truth corpus.
**Do not modify them.** If corpus changes are needed, treat as a new milestone (MT-x.x).

Corpus integrity: run `python tests/validate_corpus.py` to check against `manifest.json`.

### Corpus Preparation (Stage 0)

File `.txt` di `corpus/` disiapkan menggunakan [`regulasi-id-corpus-prep`](https://github.com/ziffan/regulasi-id-corpus-prep):

```bash
pip install regulasi-id-corpus-prep
regulasi-id-corpus-prep run dokumen.pdf --profile ojk-pojk --output-dir ./corpus/
```

Lihat `docs/REPLICATION_GUIDEv1.md` Stage 0 untuk instruksi lengkap. Jangan replace file corpus yang ada tanpa menjalankan round-trip test (target: 100.00% SequenceMatcher ratio).

---

## Smoke Test Status

| Test | Model | Result | Date |
|---|---|---|---|
| ST1 — Sonnet plumbing | Sonnet 4.6 | ✅ PASS | 2026-04-23 |
| ST2 — Opus quality (3 runs) | Opus 4.7 | ✅ PASS | 2026-04-23 |

**ST2 key finding:** 3/3 ground-truth frictions found in every run. Severity calibration sudah di-fix (severity lock patch) dan di-verified PASS 2/2 runs.

**Verify run (2026-04-24):** 4 findings, 1 critical/1 major/2 minor. Temporal window tepat (2024-12-27 → 2025-07-31, 7 bulan). UI streaming confirmed working.

---

## Budget (kumulatif s.d. 2026-04-29)

| Sesi | API | Claude Code |
|---|---|---|
| 2026-04-23 | $14.16 | $11.11 |
| 2026-04-24 | $33.21 | $30.96 |
| 2026-04-29 (CI/CD setup) | — | $2.76 |
| **Total** | **$47.37** | **$44.83** |

**Grand total s.d. 2026-04-29: $92.20** — See `docs/BUDGET_TRACKER.md` for per-call breakdown.

**Sesi 2026-04-29 breakdown:** Sonnet 4.6 $2.75 + Haiku 4.5 $0.004. 6.0M cache read tokens (corpus warm dari sesi sebelumnya).

---

## Pending Work (Next Session)

1. **Dependabot PRs** — review dan merge pip/npm PRs satu per satu saat mulai v0.2.0 development. Prioritas pertama: `anthropic` SDK (cek breaking changes di CHANGELOG SDK dulu).
2. **Pertimbangkan `temperature=0`** untuk output lebih deterministik (findings count 4–5 stochastic).
3. **Stabilisasi Terminology Drift** (stochastic 1/2 post-patch).

---

## Git

- Remote: https://github.com/ziffan/lexharmoni.git
- Branch: `master`
- License: Apache 2.0 (headers on all `.py` files)
- History is clean — sensitive strings removed via filter-branch in earlier session
- **CI badge** on README: green = master passing all 3 CI jobs
