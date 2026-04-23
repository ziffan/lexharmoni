# Changelog

All notable changes to LexHarmoni are documented here.

---

## [Unreleased]

- Prompt fix: enforce type→severity mapping (normative→critical, hierarchical→major)
- Verify `cache_stats.log` write after BASE-path fix

---

## [smoke-test-2] — 2026-04-23

### Added
- `docs/SMOKE_TEST_2_RESULTS.md` — 3-run cross-analysis, consistency matrix, quality notes
- `docs/BUDGET_TRACKER.md` — per-call cost tracking with Opus/Sonnet pricing

### Changed
- `backend/main.py` — `max_tokens` 32K → 128K (Opus 4.7 actual API limit)
- `backend/main.py` — `cache_stats.log` path: `Path(__file__).parent` → `BASE / "backend"` (fix for uvicorn hot-reload path resolution)

### Quality (ST2, 3 runs)
- 3/3 ground-truth core frictions found in every run
- Consistent: collection hours conflict, dangling cantolan Bab XI, terminology drift
- Stochastic (1–2/3 runs): TKB vs 5-kategori, manfaat ekonomi Pasal 140, Sertifikat Elektronik

---

## [smoke-test-1] — 2026-04-23

### Added
- `docs/SMOKE_TEST_1_RESULTS.md` — Sonnet 4.6 plumbing verification, cache hit confirmed
- Cache stats logging in `backend/main.py` (stderr + stdout + file)

### Changed
- `backend/main.py` — default model → `claude-opus-4-7`

### Fixed
- `findings JSON malformed` — Sonnet 4.6 wraps `<findings>` in ` ```json ``` ` fences;
  stripped by `re.sub` in `parse_findings()` (`backend/prompt_loader.py`)

---

## [MT-3.3] — 2026-04-23

### Changed
- `backend/prompt_loader.py` — `cache_control` TTL extended: ephemeral default → `"1h"`
- `backend/main.py` — added `extra_headers: {"anthropic-beta": "extended-cache-ttl-2025-04-11"}`

---

## [ui-redesign] — 2026-04-23

### Changed
- `frontend/app/page.tsx` — light-canvas / dark-data-panel theme
  - Page: `bg-slate-50`; panels: `bg-white border-slate-200`
  - Draft + reasoning: `bg-slate-900` (intentional contrast)
  - Severity badges: red/amber/slate; Analyze button: emerald

---

## [MT-OSS] — 2026-04-23

### Added
- `LICENSE` — Apache 2.0
- `NOTICE`, `CONTRIBUTORS.md`
- Apache 2.0 license headers on all `.py` files

---

## [MT-3.2 / MT-4.2] — 2026-04-23

### Added
- `backend/main.py` — `/analyze` SSE endpoint, `/corpus/preset/pojk-40-2024`
- `backend/prompt_loader.py` — 4-block system array, `build_user_message()`, `parse_findings()`
- `frontend/app/page.tsx` — full demo UI: SSE streaming, reasoning panel, findings cards, model dropdown
- `frontend/.env.local.example`, `backend/.env.example`

---

## [MT-2.2 / MT-2.3] — 2026-04-23

### Added
- `corpus/manifest.json` — metadata for all 7 regulations
- `tests/validate_corpus.py` — manifest integrity validation

---

## [MT-4.1] — 2026-04-23

### Added
- Next.js 15 skeleton with App Router (`frontend/`)

---

## [MT-3.1] — 2026-04-23

### Added
- FastAPI skeleton with `/health` endpoint (`backend/`)

---

## [MT-1.x] — 2026-04-23

### Added
- `corpus/active/` — POJK-22-2023, POJK-40-2024, SEOJK-19-2025
- `corpus/historical/` — POJK-77-2016, POJK-31-2020, POJK-10-2022, SEOJK-19-2023
- `ground-truth/manual-analysis.md` — 3 core frictions, hand-authored
- `AUDIT_DAY1_BASELINE.md`

---

## [MT-0.x] — 2026-04-23

### Added
- Project skeleton: `backend/`, `frontend/`, `corpus/`, `docs/`, `ground-truth/`, `prompts/`
- `DECISIONS.md`, `.gitignore`

---

## [initial] — 2026-04-23

- Repository initialized
