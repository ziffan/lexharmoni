# Changelog

All notable changes to LexHarmoni are documented here.

---

## [Unreleased]

- Video editing: review B1/B2/B3 footage, pilih best take, edit demo video
- Submit ke Anthropic hackathon (deadline: 27 April 07:00 WIB)
- Pertimbangkan `temperature=0` untuk output lebih deterministik

---

## [ci-setup] — 2026-04-29

### Added
- GitHub Actions CI workflow (`.github/workflows/ci.yml`): lint, type-check, build, manifest validation, license header check, markdown link check.
- GitHub Actions security workflow (`.github/workflows/security.yml`): pip-audit, npm audit, gitleaks secret scan.
- Dependabot configuration (`.github/dependabot.yml`) for pip, npm, and github-actions ecosystems — weekly, Monday.
- `pyproject.toml` — ruff, mypy, and pytest baseline configuration.
- `--check` flag on `scripts/add_license_headers.py` (dry-run mode for CI).

### Changed
- `backend/main.py`, `backend/prompt_loader.py` — ruff formatting baseline (no logic changes).
- `README.md` — CI badge added.

---

## [docs-final] — 2026-04-24

### Added
- `docs/PROBLEM_STATEMENT.md` — full 8K-word problem analysis: workflow as regulatory officer, corpus deep-dive, 3 friction case studies, why human review fails, opportunity window, scope
- `recordings/voiceover-final-v1.md`, `recordings/HACKATHON_CONTEXT_v7.md` — video prep assets

### Changed
- `README.md` — promote READMEv2: accurate friction timelines (Dec 2023–Jul 2025), resolved-by annotations in corpus list, corpus date through Jul 2025
- `CLAUDE.md` — correct Opus 4.7 cache cost figures; remote URL → lexharmoni
- `.gitignore` — exclude recording/, *.mp4, *.mov

### Budget
- Claude Code sesi 2026-04-24 final: **$30.96** (Haiku $0.91 + Sonnet $30.06)
- Grand total: **$89.44** (API $47.37 + Claude Code $42.07)

---

## [demo-recording] — 2026-04-24

### Added
- `docs/DEMO_RECORDING_SESSION.md` — recording session log (timeline, cache stats, cost)
- `docs/smoke_test_2_detailed.md`, `docs/smoke_test_summary.md` — committed as permanent docs
- `.gitignore` — exclude `backend/cache_stats.log`, `backend/server.log`, `frontend/dev.log`, `.claude/`

### Removed
- `docs/INTEGRATION_SPEC_MT-3.2_MT-4.2.md` — superseded

### Recording Results
- Pre-recording Phase 1 checklist: PASS semua (health, manifest, API key, cache config, frontend)
- Cache warm-up: 18:35 WIB, `cache_creation=554,518` tokens confirmed
- Recorded runs: 3× Opus 4.7, semua `cache_read=554,518` (HIT), output 9.4K–11.1K tokens
- Recording session cost: $11.82

---

## [ui-streamfix] — 2026-04-24

### Added
- `backend/main.py` — `/analyze/mock` endpoint: streams pre-canned regulatory findings at 150ms/chunk, no API cost
- `frontend/app/page.tsx` — **Mock** option in model dropdown (replaces Sonnet 4.6)
- `frontend/app/page.tsx` — Disclaimer footer dengan copyright notice
- `tests/validate_severity_lock.py` — post-patch severity validation script
- `docs/SEVERITY_LOCK_VALIDATION.md` — hasil 2 post-patch runs (PASS)

### Fixed
- **Streaming real-time (React 19 auto-batching)**: ganti `flushSync` dengan `useRef` accumulator + `setInterval(60ms)` drain — bypass React 19 batching sepenuhnya
- **`<reasoning>` tag leak + broken words**: SSE CRLF line endings (`\r\n`) menyebabkan `\r` ter-embed di data field setelah `split('\n')`, sehingga tag terpotong (`<re\rasoning>`) dan kata terpisah (`f\rully`). Fix: `.replace(/\r$/, '')` per SSE data line
- **Tag strip regex**: normalisasi spasi di dalam `<...>` sebelum strip — handle tokenisasi BPE yang memecah tag lintas chunk
- **Mock analyze guard**: `analyze()` early-return `if (!draftText.trim())` tidak berlaku saat mode Mock
- **`cache_stats.log` path**: `Path(__file__).parent` → `BASE / "backend"` (uvicorn hot-reload path resolution)
- **Severity calibration**: severity lock patch di `prompt_loader.py` — normative→critical, hierarchical→major, operational→minor. PASS 2/2 post-patch runs
- **Footer layout**: hapus `max-w-4xl mx-auto`, teks `text-center`

### Changed
- `backend/main.py` — `max_tokens` 16K → 128K (Opus 4.7 actual API limit)

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
