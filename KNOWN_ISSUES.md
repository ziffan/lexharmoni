# Known Issues — Not Fixed in v0.1.0-final

These issues are documented for transparency. **They will not be resolved in
this archived repository.** They may or may not be addressed in the successor
project.

## Archive Status

This repository was archived on April 30, 2026. See README.md and DECISIONS.md
for full context on the archive decision.

---

## Hackathon Scope Constraints (Intentional, Not Bugs)

These were design decisions made for hackathon scope discipline. They are
limitations, not defects. The successor project plans to address them.
See DECISIONS.md for architectural rationale.

- **Single LLM provider:** Anthropic Claude only. No OpenAI, OpenRouter,
  Gemini, or other provider support.
- **Fixed corpus:** Hardcoded Indonesian P2P lending regulatory dataset (7
  regulations, OJK LPBBTI domain). Users cannot upload custom corpora or
  switch between corpora at runtime.
- **No prompt customization:** Prompts are hardcoded in `backend/prompt_loader.py`.
  Users cannot edit, version, or tune prompts via UI.
- **Single tenancy:** No multi-user, no workspace isolation, no role-based
  access control.
- **No persistent storage of queries:** Each session is ephemeral. Analysis
  results are not saved between page refreshes.
- **Retrospective validation only:** The demo validates LexHarmoni against
  already-enacted regulation. Ex-ante deployment in an active drafting workflow
  has not been tested.

---

## Functional Limitations (Documented, Not Bugs)

### Pytest test suite not yet implemented

No pytest-discoverable test files exist in the `tests/` directory. The CI
`backend-lint-and-test` job exits cleanly via an `exit 5` workaround
(`|| [ $? -eq 5 ]` in `ci.yml`) — pytest exit code 5 means "no tests
collected", which is treated as a passing state. The `requires_api` pytest
marker is defined in `pyproject.toml` but is not exercised by any test file.

The two validation scripts in `tests/` (`validate_corpus.py`,
`validate_severity_lock.py`) are run-on-demand tools, not pytest test cases.

### `validate_severity_lock.py` excluded from CI

`tests/validate_severity_lock.py` validates that the model's severity
calibration (normative→critical, hierarchical→major, operational→minor) is
correct across live runs. It requires a running backend server and a live
Anthropic API key. It is run manually pre-release per the smoke test protocol
in `docs/`. It is intentionally excluded from CI per the "Decision: CI scope
excludes Anthropic API calls" in DECISIONS.md.

### Stochastic secondary findings (non-deterministic count)

The three core friction patterns surface consistently across all recorded runs.
Secondary findings (finding count 4–5) vary by run due to stochastic sampling.
This is expected behavior from language model inference, not a bug. Using
`temperature=0` may reduce variance (noted in CHANGELOG `[Unreleased]` as a
future consideration).

---

## Dependency Risks

- Dependencies pinned to versions current as of archive date (April 30, 2026).
- **Python version:** 3.11 (see `pyproject.toml` `python_version`).
- **Node version:** ≥20 (see `@types/node` version constraint in
  `frontend/package.json`; CI runs on Node 20).
- Anthropic SDK, Next.js, and other dependencies may have breaking changes in
  future major versions. No further patches will be applied in this repository.
- All 7 Dependabot PRs (#5–#11) were closed without merge as part of the archive
  process — no security advisories were identified. See DECISIONS.md.

---

## Reporting

GitHub Issues are disabled on archived repositories. For issues with the
successor project, use the successor repository (link in README when available).

For issues with the spawned tool `regulasi-id-corpus-prep`, use that
repository's issue tracker directly:
https://github.com/ziffan/regulasi-id-corpus-prep/issues
