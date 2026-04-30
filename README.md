# LexHarmoni

**AI-Powered Regulatory Stress-Testing**
*"Test the impact, before it's enacted."*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/ziffan/lexharmoni/actions/workflows/ci.yml/badge.svg)](https://github.com/ziffan/lexharmoni/actions/workflows/ci.yml)
[![Built with](https://img.shields.io/badge/Built%20with-Claude%20Opus%204.7-D97757.svg)](https://www.anthropic.com/claude)
[![Hackathon](https://img.shields.io/badge/Built%20with%20Opus%204.7-Hackathon-8B5CF6.svg)](https://cerebralvalley.ai/e/built-with-4-7-hackathon)
![Status](https://img.shields.io/badge/status-archived-lightgrey)
![Type](https://img.shields.io/badge/type-hackathon%20submission-blue)
![Version](https://img.shields.io/badge/version-v0.1.0--final-green)

---

> ## ⚠️ Repositori Diarsipkan / Repository Archived
>
> ### 🇮🇩 Indonesia
>
> Repositori ini diarsipkan pada **30 April 2026** sebagai snapshot proyek
> hackathon. LexHarmoni v0.1.0 dikembangkan untuk **Cerebral Valley × Anthropic
> "Built with Opus 4.7" Hackathon (April 2026)**.
>
> **Dua tag tersedia untuk reprodusibilitas:**
> - [`v0.1.0`](https://github.com/ziffan/lexharmoni/releases/tag/v0.1.0) — state asli submisi hackathon
> - [`v0.1.0-final`](https://github.com/ziffan/lexharmoni/releases/tag/v0.1.0-final) — state arsip dengan
>   improvement post-submisi (CI, security patches, dokumentasi)
>
> **Status CI terakhir:** ✅ Green pada **2026-04-29** (lihat
> [Actions tab](https://github.com/ziffan/lexharmoni/actions))
>
> **Tidak ada pengembangan lanjutan, bug fix, atau pull request yang akan
> diterima di repositori ini.** Issues boleh dibuka untuk arsip diskusi tapi
> tidak akan diresolve di sini.
>
> 🔄 **Pengembangan aktif dilanjutkan di proyek successor:** _[link akan
> ditambahkan saat repo successor diinisialisasi]_
>
> 📚 **Untuk corpus preparation Indonesian regulatory PDFs**, lihat tool
> independent yang di-spawn dari proyek ini:
> [regulasi-id-corpus-prep](https://github.com/ziffan/regulasi-id-corpus-prep)
>
> Untuk konteks keputusan arsitektur dan constraint hackathon, lihat
> [DECISIONS.md](./DECISIONS.md), [CHANGELOG.md](./CHANGELOG.md), dan
> [KNOWN_ISSUES.md](./KNOWN_ISSUES.md).
>
> ---
>
> ### 🇬🇧 English
>
> This repository was archived on **April 30, 2026** as a hackathon project
> snapshot. LexHarmoni v0.1.0 was built for the **Cerebral Valley × Anthropic
> "Built with Opus 4.7" Hackathon (April 2026)**.
>
> **Two tags are available for reproducibility:**
> - [`v0.1.0`](https://github.com/ziffan/lexharmoni/releases/tag/v0.1.0) — original hackathon submission state
> - [`v0.1.0-final`](https://github.com/ziffan/lexharmoni/releases/tag/v0.1.0-final) — archived state with
>   post-submission improvements (CI, security patches, documentation)
>
> **Last CI status:** ✅ Green on **2026-04-29** (see
> [Actions tab](https://github.com/ziffan/lexharmoni/actions))
>
> **No further development, bug fixes, or pull requests will be accepted in
> this repository.** Issues may be opened for archival discussion but will
> not be resolved here.
>
> 🔄 **Active development continues in the successor project:** _[link to be
> added when successor repository is initialized]_
>
> 📚 **For Indonesian regulatory PDF corpus preparation**, see the independent
> spawned tool:
> [regulasi-id-corpus-prep](https://github.com/ziffan/regulasi-id-corpus-prep)
>
> For context on architectural decisions and hackathon constraints, see
> [DECISIONS.md](./DECISIONS.md), [CHANGELOG.md](./CHANGELOG.md), and
> [KNOWN_ISSUES.md](./KNOWN_ISSUES.md).
>
> ---

---

> *"I worked as a Regulatory Officer at the Indonesia Stock Exchange. When a draft crossed my desk, I had two tools: asking senior colleagues who drew from their experience and memory, and Ctrl+F. For a handful of documents, that worked. For hundreds, context slips — not from negligence, but because the dependency web between regulations exceeds what any single reviewer can hold in active working memory while drafting. I built LexHarmoni for the regulator I used to be."*

LexHarmoni loads an entire regulatory corpus into Claude Opus 4.7's 1M-token context window, then compares a new draft against the full corpus simultaneously. The result: friction patterns that would otherwise take months to surface in manual review become visible in roughly two minutes.

---

## What LexHarmoni Is

A **stress-test harness for legal drafting**. Just as software engineers run test suites before shipping code, regulatory drafters can now run friction tests before enacting regulation.

LexHarmoni is not a replacement for legal expertise — it is augmentation. A senior regulatory counsel still reviews and signs off. LexHarmoni provides a second pair of eyes that can hold more context simultaneously than any single reviewer could carry in working memory.

### Three-Tier Friction Taxonomy

- **Normative (Critical):** Direct conflicts between articles governing the same subject matter.
- **Hierarchical (Major):** Lex Superior/Posterior violations, or orphaned delegation chains when higher-order provisions are revoked while their implementing circulars remain in force.
- **Operational (Minor):** Terminology drift, reporting redundancies, or definitional inconsistency across regulatory generations.

---

## The Problem

Indonesia's peer-to-peer lending sector is governed by seven regulations spanning nine years (2016–2025). Reading them chronologically, patterns emerge — saving clauses extending older circulars, terminology shifting between drafts, delegation chains tangled by successive revocations.

Some of these patterns persist for 17–19 months before being resolved through subsequent OJK regulation. Not because anyone failed. Because the dependency web between documents exceeds what working memory can hold during any single drafting cycle.

The table below summarizes three friction patterns documented in our [manual analysis baseline](ground-truth/manual-analysis.md) — patterns LexHarmoni independently surfaces when given the same corpus. All three have since been resolved through subsequent regulation; the manual review was deliberately scoped to known, since-resolved frictions so that LexHarmoni's detections can be validated against ground truth.

| Friction | Type | Window (Duration) | Nature of the Gap |
|---|---|---|---|
| Terminology inconsistency: POJK 10/2022 (*LPBBTI*) vs POJK 31/2020 (*Pinjam Meminjam*) | Operational | Jul 2022 – Dec 2023 (~17 months) | Two simultaneously-active regulations used different identifiers for the same industry; resolved by POJK 22/2023 |
| Orphaned Chapter XI of SEOJK 19/2023 after surgical revocation of POJK 10/2022 Art. 102–104 | Hierarchical | Dec 2023 – Jul 2025 (~19 months) | Implementing chapter operationally active but parent delegating article revoked by POJK 22/2023; resolved by SEOJK 19/2025 |
| Collection-hours mismatch: SEOJK 19/2023 vs POJK 22/2023 | Normative | Dec 2023 – Jul 2025 (~19 months) | Two active regulations specified different permissible hours, reconciled only by Lex Superior doctrine; resolved by SEOJK 19/2025 |

For detailed methodology, corpus selection rationale, and case studies, see [`docs/PROBLEM_STATEMENT.md`](docs/PROBLEM_STATEMENT.md).

---

## The Approach

Most LLM applications handle large document corpora via Retrieval-Augmented Generation (RAG) — retrieving top-K relevant chunks and reasoning over fragments. RAG is well-suited to question-answering and summarization, and recent work shows carefully designed RAG (graph-based retrieval, multi-hop query decomposition, OP-RAG) can be competitive with long-context models on multi-hop benchmarks.

For friction detection in a small, stable regulatory corpus, the design trade-off tilts the other way. Detecting that Article A in Regulation 1 contradicts Article B in Regulation 2, while Saving Clause C in Regulation 3 keeps the conflict active, requires holding the relationships between all three documents in the same reasoning chain. RAG can do this, but it requires careful retrieval engineering — and a wrong retrieval at any hop silently drops a document the model needed to see. Loading the full corpus eliminates that design surface entirely, at the cost of higher per-inference compute.

**Opus 4.7's 1M-token context window makes loading an entire regulatory corpus per inference architecturally practical at reasonable cost.** LexHarmoni loads all 7 regulations (~554K tokens including system prompt) via Anthropic prompt caching with 1-hour TTL, then lets Opus 4.7 traverse the full corpus rather than retrieve fragments.

| Approach | Better fit when |
|---|---|
| RAG (top-K retrieval) | Corpus is large or dynamic; per-query retrieval cost dominates; questions are localized to a few documents |
| LexHarmoni (full-context) | Corpus is small and stable; every document matters per query; reasoning crosses many document boundaries; coverage matters more than per-inference cost |

This is a deliberate design choice, not a categorical claim about RAG. The advantage for this task class is asserted from the corpus characteristics; a controlled benchmark against a tuned RAG baseline is left to future work.

---

## Demo — Retrospective Validation on POJK 40/2024

LexHarmoni demonstrates its capability by retroactively analyzing POJK 40/2024 — an already-enacted P2P lending regulation — against the six other regulations in the corpus. This retrospective validation compares LexHarmoni's findings against three friction patterns that are already documented in the manual baseline, each of which persisted for 17–19 months before being resolved by subsequent OJK regulation. Because the resolution timeline is now known, the manual baseline provides a ground truth against which LexHarmoni's detections can be directly checked.

**What the demo shows:**
1. Opus 4.7 streams its reasoning in real time, quoting specific articles as it works.
2. It identifies the normative contradiction on debt-collection hours between SEOJK 19/2023 and POJK 22/2023, with article-level citations.
3. It traces the orphaned Chapter XI delegation — from SEOJK 19/2023's original citation of *Pasal 104(2) POJK 10/2022*, through the surgical revocation of that article by POJK 22/2023 (22 Dec 2023), through the full repeal of POJK 10/2022 by POJK 40/2024 (27 Dec 2024).
4. It flags the terminology inconsistency between POJK 10/2022 (*LPBBTI*) and the then-active POJK 31/2020 (*Pinjam Meminjam*) during their 17-month overlap.
5. Every finding includes temporal window, severity level, and a recommended resolution path.

**Duration:** Roughly two minutes from draft submission to complete findings (validated across three recorded Opus runs). For comparison: the manual review baseline that established these friction patterns took ~8 hours of focused expert work. The 17–19 month resolution timeline cited elsewhere is a separate metric — it measures the gap from friction onset to enactment of corrective regulation, which includes drafting, public consultation, and enactment cycles, not just analytical detection time.
The validation baseline — a manual legal analysis conducted prior to the hackathon — is documented in [`ground-truth/manual-analysis.md`](ground-truth/manual-analysis.md).

**Demo video:** [https://youtu.be/v1EbVazszEs](https://youtu.be/v1EbVazszEs)

Watch a 3-minute walkthrough showing draft submission, real-time reasoning stream, and  friction findings:


---

## Architecture

```
┌────────────────────┐          ┌──────────────────────────┐
│   Next.js UI       │  SSE     │   FastAPI Backend        │
│   (frontend/)      │ ───────► │   (backend/)             │
│                    │          │   ─ /analyze (streams)   │
│   - Draft panel    │ ◄─────── │   ─ /analyze/mock        │
│   - Reasoning view │  stream  │   ─ /corpus/manifest     │
│   - Findings cards │          │   ─ /health              │
└────────────────────┘          └────────────┬─────────────┘
         │                                    │
         │ useRef + setInterval               │ anthropic-beta:
         │ drain pattern                      │ extended-cache-ttl-2025-04-11
         │ (React 19 batching fix)            │
         ▼                                    ▼
   Real-time reasoning           ┌──────────────────────────┐
   token-by-token display        │  Claude Opus 4.7 API     │
                                 │  ─ 1M context window     │
                                 │  ─ 128K max output       │
                                 │  ─ 4 cached system blocks│
                                 │  ─ 1h TTL prompt cache   │
                                 │  ─ Streaming response    │
                                 └────────────┬─────────────┘
                                              │
                                              ▼
                                 ┌──────────────────────────┐
                                 │  Corpus (7 regulations)  │
                                 │  + manifest.json         │
                                 │  + versioned prompt      │
                                 │  ~410K tokens corpus     │
                                 │  ~554K tokens total      │
                                 │  (including system)      │
                                 └──────────────────────────┘
```

---

## Design Decisions

Hackathon judges and future contributors often want to understand *why this, not that*. The five decisions below shaped LexHarmoni's architecture.

### 1. Why full-corpus context, not RAG

Friction detection is fundamentally cross-document reasoning. A normative conflict between Regulation A and Regulation B, perpetuated by a saving clause in Regulation C, is invisible to top-K retrieval — the three documents are each relevant independently, but the conflict emerges only when they are held simultaneously. Opus 4.7's 1M context window is the first commercial architecture where this approach becomes viable at reasonable cost.

### 2. Why 1-hour cache TTL (not 5-minute default)

Our recording session needed multiple consecutive runs without re-paying corpus ingestion cost. The Anthropic extended-cache-ttl beta header (`extended-cache-ttl-2025-04-11`) lets us hold the ~554K-token cache for a full hour at roughly 10% of re-write cost on subsequent reads. Without this, each demo run would incur a $5+ cache write; with it, runs 2–4 in a warm window cost ~$1.70 each.

### 3. Why streaming with a dual-stream UI (reasoning + findings)

Black-box output erodes trust in legal contexts. By streaming Opus's reasoning token-by-token alongside structured findings, reviewers can watch the model trace citations and flag friction in real time — and push back where the reasoning seems off. Explainability is not a feature; it is a precondition for regulators being willing to use AI output at all.

### 4. Why Opus 4.7 over Sonnet 4.6

Smoke testing showed Opus 4.7 consistently surfaced all three core frictions across three independent runs with zero hallucination and correctly cited articles. Sonnet 4.6 was used earlier for plumbing validation (streaming, cache confirmation) but produced less nuanced severity calibration on the same corpus. For a low-volume, high-stakes workflow like regulatory review, Opus 4.7's output quality justified the 5x input pricing differential.

### 5. Why immutable corpus after MT-1.3 commit

Reasoning is only reproducible if the corpus is versioned. Every finding LexHarmoni produces can be traced back to a specific commit of the corpus directory, with the prompt version recorded in the system prompt itself. Changes to the corpus require a new commit and trigger re-validation — there is no silent corpus drift.

Full architectural rationale, including failed approaches and trade-offs: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## Cost Transparency

LexHarmoni was built during a 5-day hackathon window on a bounded budget. Actual API costs over the development + recording period:

| Phase | Cost |
|---|---|
| Development (2 days, smoke tests + iterations) | ~$47.37 API + ~$42 Claude Code |
| Recording session (1 warm-up + 3 recorded Opus runs) | $11.82 |
| **Total project to date** | **~$89.44** |

**Per-inference cost (for operational reference, validated from demo session CSV):**
- Opus 4.7 run with warm cache (1h TTL): ~$1.70 (corpus cache read $0.28 + user msg auto-cache $1.17 + output $0.25)
- Opus 4.7 run with cold cache (corpus write): ~$6.75 (corpus write $5.55 + user msg no-cache $0.93 + output $0.27)

A regulatory body running 20–30 draft stress tests per month at this per-inference cost would spend roughly $15–75 in API costs monthly — negligible relative to the human-hour cost of a missed friction surfacing 17 months later.

---

## Limitations & Honest Assessment

LexHarmoni is an exploratory prototype. What it does not do matters as much as what it does.

- **Scope is narrow.** Seven Indonesian P2P lending regulations. Not a general-purpose legal AI. Not tested on other jurisdictions, other regulatory domains, or other legal systems.
- **Not an adjudication tool.** LexHarmoni surfaces friction patterns. Applying Lex Superior, Lex Posterior, or Lex Specialis doctrine to resolve those frictions requires human legal counsel judgment.
- **Stochasticity in secondary findings.** The three core frictions surface consistently across all three validation runs. Additional patterns vary by reasoning path — useful for broadening review surface, but the tool is not a single-answer oracle.
- **Corpus captured through July 2025.** The most recent regulation in scope is SEOJK 19/2025 (31 July 2025). Amendments or new regulations after that date are not in scope for this prototype.
- **Retrospective validation, not ex-ante deployment.** The demo validates LexHarmoni against already-enacted regulation. Ex-ante deployment in an active drafting workflow has not been tested and would require additional validation.
- **Source accuracy not comprehensively verified.** Corpus documents were sourced from JDIH OJK and processed via automated scripts. Spot checks passed; full text-level verification against authoritative OJK prints has not been conducted.

---

## Quickstart

**Requirements:** Python 3.11+, Node.js 20+, Anthropic API key.

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # add your ANTHROPIC_API_KEY
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000), click **Load POJK 40/2024 (Demo)**, then **Analyze**.

Full setup and troubleshooting: [`docs/USER_MANUAL.md`](docs/USER_MANUAL.md).
If you want to replicate this project, see [`docs/REPLICATION_GUIDEv1.md`](docs/REPLICATION_GUIDEv1.md).

**Mock mode:** Select "Mock (no API)" in the model dropdown to stream pre-canned findings without API cost. Useful for UI development or offline demos.

---

## Corpus

Seven OJK regulations covering Indonesia's P2P lending sector across 9 years (2016–2025). Full structured metadata in [`corpus/manifest.json`](corpus/manifest.json).

**Active (in force):**
- POJK 22/2023 — Consumer Protection in Financial Services
- POJK 40/2024 — LPBBTI (replaces POJK 10/2022)
- SEOJK 19/2025 — LPBBTI Implementation (replaces SEOJK 19/2023)

**Historical (revoked / superseded):**
- POJK 77/2016 — Fintech Lending (original, superseded by POJK 10/2022)
- POJK 31/2020 — Consumer Services at OJK (several articles revoked by POJK 22/2023)
- POJK 10/2022 — LPBBTI (Art. 102–104 surgically revoked by POJK 22/2023 on 22 Dec 2023; full repeal by POJK 40/2024 on 27 Dec 2024)
- SEOJK 19/2023 — LPBBTI Implementation (revoked by SEOJK 19/2025 on 31 Jul 2025)

Corpus is read-only after initial commit. See [`corpus/README.md`](corpus/README.md).

---

## Project Structure

```
lexharmoni/
├── backend/              FastAPI + Anthropic SDK
├── frontend/             Next.js 15, App Router, Tailwind
├── corpus/               7 OJK regulations (immutable)
│   ├── active/
│   ├── historical/
│   └── manifest.json
├── ground-truth/         Human expert analysis (evaluation baseline)
├── prompts/              Versioned prompts (friction-detection-v1.md)
├── scripts/              Manifest validator
└── docs/                 Architecture, decisions, user manual, specs
```

---

## Status & Roadmap

**Built during:** Cerebral Valley × Anthropic — *Built with Opus 4.7* Hackathon (April 21–26, 2026).

**Current scope:** Indonesian P2P lending (LPBBTI) — 7 regulations, 3 friction types, retrospective validation.

**Upgrade paths being explored:**
- **Adaptive thinking integration.** The current implementation uses plain Opus 4.7 output. Enabling adaptive thinking mode (`thinking: {type: "adaptive"}` with high effort) is a natural next step and may deepen normative conflict detection specifically. Initial testing deferred to post-hackathon.
- **Corpus expansion.** Scaling from 7 to 50+ POJK covering the full OJK Consumer Protection domain.
- **Cross-ministry friction.** Extending to Bank Indonesia (banking, payment systems) and cross-ministry interactions (OJK ↔ Kemenkeu ↔ Kemenkominfo).
- **Ex-ante drafting workflow integration.** The current prototype validates retrospectively. Integrating into an active drafting workflow as an advisory layer is the natural deployment target.
- **Evaluation harness.** A systematic evaluation against multiple corpus snapshots to measure precision and recall on friction detection.

---

## Built With

- **[Claude Opus 4.7](https://www.anthropic.com/claude)** — primary reasoning engine (1M context window, 128K max output, prompt caching with 1h TTL).
- **[Claude Code](https://www.anthropic.com/claude-code)** — primary coding agent for implementation.
- **[Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)** — API integration.
- **[FastAPI](https://fastapi.tiangolo.com/)** + **[SSE-Starlette](https://github.com/sysid/sse-starlette)** — streaming backend.
- **[Next.js 15](https://nextjs.org/)** (App Router) + **[Tailwind CSS](https://tailwindcss.com/)** — frontend.

---

## Contributing

Contributions welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Security issues: see [`SECURITY.md`](SECURITY.md).

---

## Acknowledgments

Built by **Ziffany Firdinal** — former Regulatory Officer at the Indonesia Stock Exchange (IDX), currently practicing as an OJK-registered capital markets legal consultant. The workflow LexHarmoni augments is the one I used daily.

The friction taxonomy and corpus analysis derive from a **mini research exercise** — a bounded manual legal review of the seven regulations conducted in under 8 hours prior to the hackathon. That analysis is documented in [`ground-truth/manual-analysis.md`](ground-truth/manual-analysis.md) and serves as the evaluation baseline for LexHarmoni's AI output. The corpus was deliberately scoped to seven regulations to keep the mini research tractable within the available time.

---

## Disclaimer

LexHarmoni is an educational exploration tool. Output is AI-generated (Claude Opus 4.7) based on a limited corpus of 7 Indonesian P2P lending regulations sourced from JDIH OJK and processed via automated scripts — source accuracy is not comprehensively verified.

Findings represent AI-assisted personal opinion and are **NOT legal advice**. All outputs require independent verification before being used as a basis for any decision-making. **DYOR (Do Your Own Research).**

© 2026 Ziffany Firdinal. Built for Anthropic *"Built with Opus 4.7"* Hackathon, April 2026.

---

## License

Licensed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE) for the full text.

Copyright © 2026 Ziffany Firdinal.
