# PROJECT DECISIONS

## Folder Structure Sign-off
The proposed folder structure is suitable and will be implemented to improve project organization and analysis efficiency.

### Final Structure
```
/corpus/
  /active/
    POJK-22-2023.txt
    POJK-40-2024.txt
    SEOJK-19-2025.txt
  /historical/
    POJK-77-2016.txt
    POJK-31-2020.txt
    POJK-10-2022.txt
    SEOJK-19-2023.txt
  manifest.json
/ground-truth/
  manual-analysis.md  (dari dok 07)
/prompts/
  friction-detection-v1.md
/backend/
  main.py
  ...
/frontend/
  ... (Next.js)
/docs/
  ARCHITECTURE.md
  DEMO_SCRIPT.md
README.md
.gitignore
```

### Rationale
- **Corpus Categorization:** Separating `active` and `historical` regulations allows the system to clearly distinguish between current law and outdated references, which is critical for "friction" and "inconsistency" detection.
- **Separation of Concerns:** Distinct directories for `frontend`, `backend`, and `prompts` ensure a clean development environment and simplify CI/CD pipelines.
- **Ground Truth:** Moving manual analysis to its own folder allows for automated evaluation of the model's performance against human findings.

**Signed off by:** Engineering Review

---

## Decision: Dependabot npm/pip PRs deferred post-v0.1.0

Date: 2026-04-29
Context: Dependabot opened 9 PRs immediately after `.github/dependabot.yml` was merged — covering pip (anthropic, python-dotenv, sse-starlette) and npm (react, react-dom, eslint, typescript, @types/node). github-actions PRs (#2–#4) were merged immediately as they carry no runtime risk.
Decision: All pip and npm Dependabot PRs are deferred indefinitely. Do not merge without explicit review.
Rationale:
- Project is a locked v0.1.0 hackathon submission. Demo is recorded, submission is done. No feature benefit from updating now.
- `anthropic` ≥0.39.0 → ≥0.97.0 is a 58-minor-version jump. The SDK has a history of breaking changes in streaming interface, client API, and beta header handling — all of which LexHarmoni relies on directly.
- `typescript` 5.x → 6.0.3 and `eslint` 9.x → 10.x are major version bumps that may introduce type errors or lint failures.
- `@types/node` 20.x → 25.x is a large jump that may conflict with the Node 20 runtime pinned in CI.
Consequence: Known dependency updates go un-merged. Compensating control: `security.yml` runs `pip-audit` and `npm audit --audit-level=high` weekly, which will surface any CVEs regardless of whether updates are merged.
When to revisit: At the start of post-hackathon development (v0.2.0 planning), merge one PR at a time and verify CI stays green after each.

---

## Decision: CI scope excludes Anthropic API calls

Date: 2026-04-29
Context: CI/CD added post-hackathon for repo hygiene and security. Project is a locked v0.1.0 hackathon submission.
Decision: CI does NOT call the Anthropic API. Smoke testing of API integration is performed manually pre-release.
Rationale: cost ($1.70–$6.75 per run), API key secret management complexity, and preference for deterministic CI.
Consequence: regression in API integration may not be caught by CI; compensating control is the manual smoke test (ST1/ST2 protocol in `docs/`) before tagging releases.

---

## Decision: Archive v0.1.0 as Hackathon Submission Snapshot

Date: 2026-04-30
Context: v0.1.0 was submitted to Cerebral Valley × Anthropic "Built with Opus 4.7" Hackathon in April 2026 with locked scope (see prior decisions and CHANGELOG `[ci-setup]` entry). Post-submission validation feedback from law firm prospects identified three features required for production use: multi-provider LLM support, flexible corpus selection, and prompt tuning from UI. These changes are architecturally incompatible with the hackathon submission's single-provider, fixed-corpus design. Continuing development in this repository would either (1) compromise hackathon submission integrity, or (2) create a confusing dual-purpose repository.

Decision: Archive this repository as a read-only snapshot. Two-tier tag preservation:
- `v0.1.0` — preserves exact hackathon submission state (do not modify)
- `v0.1.0-final` — preserves archived state including post-submission CI activation, Dependabot triage, and documentation updates

Continue development in a separate successor repository (to be initialized).

Rationale:
- Clean separation between hackathon artifact and commercial-direction successor
- Reproducibility preserved via two-tier tags
- Portfolio narrative remains coherent: submission → spawned tool → successor
- No scope confusion for visitors, reviewers, or potential users

Consequence: Bug reports cannot be resolved in this repository. Dependency rot will eventually compromise runnability; mitigated by pinned versions in dependency manifests, documented Python/Node versions, and KNOWN_ISSUES.md transparency. Successor repository link to be added post-archive via pinned GitHub issue (no unarchive needed).

Dependabot PRs categorized: no security advisories were identified; all 7 routine version-bump PRs (#5–#11) closed without merge. The spawned tool `regulasi-id-corpus-prep` (separate repository) remains independent and active under its own development lifecycle.
