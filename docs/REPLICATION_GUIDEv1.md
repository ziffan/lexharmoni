# Replication Guide — Apply LexHarmoni's Workflow to Your Domain

> *"Saya bukan engineer, tapi saya tahu domain regulasi saya. Bisakah saya membangun alat seperti LexHarmoni untuk korpus saya sendiri?"*
>
> Ya. Dokumen ini menjelaskan bagaimana caranya.

---

## Who This Guide Is For

This guide is written for **domain experts who are not software engineers** — lawyers, regulators, policy analysts, compliance officers — who have deep knowledge of a specific regulatory corpus and want to replicate LexHarmoni's full-corpus reasoning approach for their own domain.

You do **not** need to write code from scratch. You will collaborate with three Claude surfaces (Claude.ai, Claude Code, and the Anthropic API), and the workflow below shows you exactly how to do that.

> *Catatan untuk pembaca Indonesia:* Dokumen ini ditulis dengan asumsi pembaca adalah praktisi domain (advokat, regulator, analis kebijakan) yang **bukan SWE**. Anda tidak perlu paham coding mendalam — yang Anda butuhkan adalah pemahaman domain, kemampuan baca dokumen Markdown, dan kesabaran untuk iterate dengan Claude.

### What you'll get at the end

A working LexHarmoni-style application — backend + frontend — configured for **your corpus**, surfacing friction patterns specific to **your domain**, validated against **your manual ground truth**.

---

## What You'll Need

| Requirement | Purpose | Cost |
|---|---|---|
| Claude.ai account (Pro recommended) | Stage 2 design conversation with Opus 4.7 | $20/month or pay-per-use |
| Claude Code installation | Stage 4 build phase | Free CLI; usage billed via API |
| Anthropic API key | Backend deployment + smoke testing | Pay-per-use, see cost estimate below |
| Your corpus as `.txt` files | Source material | Manual gathering (varies) |
| Git + GitHub account | Fork the LexHarmoni repository | Free |
| Python 3.11+ and Node.js 20+ | Runtime for backend + frontend | Free |
| 8–12 hours of focused time, spread across 2–3 days | End-to-end replication | — |

> *Catatan domain Indonesia:* Untuk korpus regulasi OJK/BI/Kemenkeu, sumber primer biasanya **JDIH** (Jaringan Dokumentasi dan Informasi Hukum) masing-masing instansi. Pastikan Anda mengambil **versi resmi** (bukan summary atau hukumonline paywall) untuk akurasi corpus.

---

## Stage 1 — Mini Research (Domain Expert Phase)

**Time: 6–8 hours · Tool: your brain + a notebook**

Before any code, you need a **manual ground truth**. This is the most important stage. Skip it, and you have no way to validate whether the AI is actually working.

### Why ground truth matters

LexHarmoni's claim is not *"AI finds friction"* — it is *"AI finds friction that a domain expert independently confirmed exists"*. Without your manual baseline, you cannot tell whether the model is surfacing real patterns or hallucinating plausible-sounding ones.

> *Catatan:* Ini adalah filosofi inti LexHarmoni. **Ground truth manual lebih penting daripada code yang elegant.** Tanpa baseline, tool legal AI = black box yang tidak bisa diaudit.

### How to scope your corpus tractably

LexHarmoni's pattern, replicable:

- **Number of documents:** ≤10 (kalau >10, cost dan complexity naik signifikan — coba split jadi sub-domain)
- **Domain boundary:** single regulatory area (e.g., P2P lending, not "all financial regulation")
- **Time window:** documents spanning at most 10 years (older docs add complexity without proportional value)
- **Reading budget:** the full corpus must be readable in ≤8 focused hours by you

### What to document

Open a fresh markdown file. Call it `manual-analysis.md`. Read your corpus chronologically and capture:

1. **Friction patterns** — places where two or more documents seem to contradict, drift in terminology, or leave gaps
2. **Dependency chains** — which documents reference or implement which others; what happens when one is revoked
3. **Saving clauses and transitional provisions** — open-ended language like *"sepanjang tidak bertentangan"* that creates legal limbo
4. **Severity ranking** — your judgment of which frictions are critical (compliance impact), major (legal ambiguity), or minor (operational annoyance)

### Output of Stage 1

A markdown file with **3–5 friction patterns documented**, each with:
- Specific article/section citations from both source and target documents
- Severity classification
- Temporal window (when active, when resolved if resolved)
- Why a single-document review would miss it

This file becomes your `ground-truth/manual-analysis.md` in the cloned repo.

---

## Stage 2 — Design Conversation with Claude.ai (Opus 4.7)

**Time: 1–2 hours · Tool: Claude.ai web interface, Opus 4.7 model**

Once you have ground truth, it's time to design the system. Use Claude.ai (not Claude Code yet) for this — you want **conversation**, not code generation.

### Why Opus 4.7 specifically for this stage

Opus 4.7 has the depth to reason about prompt architecture, friction taxonomy, and edge cases in your domain. Cheaper models will give you working prompts but miss subtle considerations that affect output quality.

> *Catatan:* Stage ini adalah "konsultasi". Anda menjelaskan domain, Opus membantu translate domain knowledge ke prompt structure. **Opus tidak menulis kode di stage ini** — ia hanya membantu Anda merancang fondasi.

### Prompt template — Stage 2

Copy-paste prompt berikut ke Claude.ai (Opus 4.7), lalu edit bagian dalam `<KURUNG>`:

```text
I want to replicate the LexHarmoni full-corpus regulatory friction
detection pattern for my own domain. I'm a <DOMAIN: e.g., capital markets
regulator, building code compliance officer, healthcare policy analyst>
working with <NUMBER> regulations covering <TOPIC> in <JURISDICTION>.

Here's the LexHarmoni public repo for reference:
https://github.com/ziffan/lexharmoni

I've already done a manual analysis. The friction patterns I found are:

1. <FRICTION 1: name + type (normative/hierarchical/operational) +
   one-sentence description>
2. <FRICTION 2: same format>
3. <FRICTION 3: same format>

My corpus characteristics:
- Total documents: <N>
- Time span: <YEARS>
- Document hierarchy (if applicable): <e.g., "primary law > regulation >
  circular letter">
- Average document length: <approximate words per document>

Please help me with three things, in order:

A. Adapt LexHarmoni's friction taxonomy to my domain. Are the three
   friction types (normative/hierarchical/operational) still appropriate,
   or do I need different categories?

B. Draft a domain-specific system prompt (Block 1 of the LexHarmoni
   architecture), tailored to my <DOMAIN> and my friction taxonomy.

C. Recommend an output schema for findings — what fields do I need
   beyond LexHarmoni's defaults to capture my domain's nuances?

Important: do not write any code yet. We're designing the prompt
architecture and schema. Code generation comes in a later stage with
Claude Code.
```

### What to expect from Opus

Opus will respond with:
- Adjusted friction taxonomy (often the 3 types map cleanly; sometimes you need a 4th)
- A draft system prompt (~1500–2500 words) tailored to your domain
- An output schema (JSON structure) with your domain-specific fields

Iterate 2–3 turns. Push back where Opus's understanding of your domain is shallow. **Your domain expertise > generic prompt templates.**

### Output of Stage 2

A markdown file: `prompts/friction-detection-v1.md` containing:
- The system prompt (Block 1)
- The user message template
- Your output schema (JSON)

Save this. You'll feed it to Claude Code in Stage 4.

---

## Stage 3 — Corpus Preparation with Sonnet

**Time: 1–2 hours · Tool: Claude.ai or API, Sonnet 4.6 model**

This stage transforms your corpus into structured data the application can use.

### Why Sonnet (not Opus) for this stage

Generating structured metadata from documents is **bulk processing** — high volume, well-defined output, low ambiguity. Sonnet 4.6 does this at ~5x lower cost than Opus and produces equivalent quality for this task.

> *Catatan ekonomi:* Stage 3 di Opus akan habiskan ~$15–25 untuk korpus 7-10 dokumen. Sonnet ~$3–5. Tidak ada reason pakai Opus di stage ini.

### What you're generating

A `manifest.json` file capturing structured metadata for every document in your corpus. Reference LexHarmoni's manifest as the schema:

```
corpus/manifest.json (in LexHarmoni repo)
```

Key fields you'll need (adjust to your jurisdiction):
- `regulation_id` — short stable identifier
- `full_name` — official title
- `hierarchy_level` — numeric position in your jurisdiction's legal hierarchy
- `date_enacted`, `date_effective`, `date_revoked`
- `status` — active / revoked / partially_revoked
- `revokes` — list of documents this one revokes (with article-level scope)
- `revoked_by` — symmetric back-reference
- `primary_topics`, `primary_subjects` — for filtering and search

### Prompt template — Stage 3

Copy-paste to Claude.ai (Sonnet 4.6), one document at a time:

```text
I'm building a structured manifest for a regulatory corpus, following the
LexHarmoni manifest.json schema. Here is one document from my corpus —
please extract the metadata fields below.

Document text:
<PASTE FULL DOCUMENT TEXT HERE — or relevant excerpts if document is long>

Generate a JSON object with these fields:

{
  "regulation_id": "<short stable ID, e.g. 'POJK-22-2023'>",
  "full_name": "<official title in original language>",
  "short_name": "<readable shortened title>",
  "hierarchy_level": <integer matching jurisdiction hierarchy>,
  "hierarchy_label": "<e.g. 'POJK', 'SEOJK', 'Statute', 'Regulation'>",
  "date_enacted": "YYYY-MM-DD",
  "date_effective": "YYYY-MM-DD",
  "date_revoked": "YYYY-MM-DD or null",
  "status": "active|revoked|partially_revoked",
  "revokes": [
    {
      "regulation_id": "<target ID>",
      "scope": "full|partial",
      "articles": ["<list of revoked articles, or null for full revocation>"],
      "note": "<one-sentence explanation>"
    }
  ],
  "revoked_by": [<same structure, opposite direction>],
  "primary_topics": ["<2-5 topic tags>"],
  "primary_subjects": ["<2-5 subject types>"],
  "file_path": "corpus/<active|historical>/<filename>.txt"
}

Important:
- If a field is unknown or not stated in the document, use null —
  do not guess.
- For 'revokes' and 'revoked_by', cite the specific article (e.g.,
  "Pasal 124(1)(f)") that does the revoking.
- Note any saving clauses or transitional provisions in a separate
  '_revocation_note' field.
```

### Validation step (critical)

Sonnet will sometimes mis-extract dates, mix up revocation directions, or hallucinate article numbers. **You must spot-check every entry against the source document.** Budget 30–60 minutes for this.

LexHarmoni includes a validation script at `tests/validate_corpus.py` that catches structural errors (missing fields, broken cross-references). Run it after Sonnet generates the manifest.

> *Catatan:* Validation Sonnet output **wajib**. Jangan trust output 100% tanpa cek. Mistake di manifest = mistake yang akan propagate ke semua downstream reasoning.

### Output of Stage 3

`corpus/manifest.json` — validated, structurally clean, with all your documents catalogued.

---

## Stage 4 — Build with Claude Code

**Time: 2–4 hours · Tool: Claude Code CLI**

Now you fork LexHarmoni and have Claude Code adapt it to your corpus.

### Step 4.1 — Fork and clone

```bash
# On GitHub, fork: https://github.com/ziffan/lexharmoni
# Then locally:
git clone https://github.com/<your-username>/lexharmoni.git
cd lexharmoni
```

### Step 4.2 — Open with Claude Code

```bash
claude code .
```

### Prompt template — Stage 4 (adaptation)

Paste this prompt to Claude Code in the project directory:

```text
I've forked LexHarmoni to adapt it for my own regulatory corpus.
My domain is <DOMAIN: e.g., Indonesian banking regulation, US tax code,
EU GDPR compliance>.

I have already prepared the following materials:
1. Ground truth analysis: ground-truth/manual-analysis.md (I will replace
   the existing file)
2. New corpus files: <N> .txt documents to place in corpus/active/ and
   corpus/historical/
3. New manifest.json (already validated): corpus/manifest.json
4. Domain-specific system prompt: prompts/friction-detection-v1.md
   (replaces the current LPBBTI-focused version)

Please help me adapt the codebase by:

A. Replacing corpus files: I will manually copy my .txt files into
   corpus/active/ and corpus/historical/. Then update backend/prompt_loader.py
   to reflect my new file list (active_files and historical_files arrays).

B. Updating frontend copy:
   - frontend/app/page.tsx: replace "POJK 40/2024 (Demo)" button text and
     pre-loaded draft with my domain's equivalent demo case.
   - Update page title, description, and any LPBBTI-specific labels.
   - Replace the example findings cards with examples from my domain.

C. Updating documentation:
   - README.md: replace LPBBTI/OJK references with my domain.
   - Keep architecture sections intact (those are domain-agnostic).
   - Update the "Corpus" section to list my regulations.

D. Verifying the build:
   - Run backend smoke test (uvicorn main:app --reload, hit /health).
   - Run frontend (npm run dev), confirm UI loads.
   - Do NOT run live Opus inference yet — that's smoke testing in Stage 5.

Important constraints:
- Do NOT modify backend caching logic, SSE streaming, or the dual-stream
  UI architecture. These are domain-agnostic and should stay as-is.
- Do NOT touch scripts/validate_manifest.py — the schema validator is
  generic.
- Preserve all license headers and attribution notices.

Walk me through each change as you make it. I will approve before you
commit.
```

### What to expect

Claude Code will:
1. Read the existing repo structure
2. Identify the files needing changes
3. Propose edits with diff previews
4. Apply edits after your approval
5. Verify the build runs

Common pitfalls:
- **Hardcoded LPBBTI strings** — Claude Code is good at finding these but may miss inline comments. Do a final `grep -r "LPBBTI"` to catch stragglers.
- **Frontend type definitions** — if your finding schema differs from LexHarmoni's, TypeScript types in `frontend/app/` need parallel updates.
- **License headers** — make sure the existing Apache 2.0 + your attribution notice both stay intact.

### Output of Stage 4

A working application — backend running on `localhost:8000`, frontend on `localhost:3000` — configured for your domain. **No live Opus inference yet.** That comes next.

---

## Stage 5 — Smoke Test & Iterate

**Time: 1–2 hours · Tool: your judgment + the application**

### Step 5.1 — Mock test first

Before paying for Opus inference, run the mock endpoint to confirm the UI flow works:

1. Open `http://localhost:3000`
2. Click your equivalent of "Load Demo"
3. Select **Mock (no API)** in the model dropdown
4. Click **Analyze**
5. Confirm: streaming output renders, findings cards appear, expand/collapse works

If anything breaks here, fix it before paying for Opus.

### Step 5.2 — Cold cache run with Opus 4.7

Switch model dropdown to **Opus 4.7** and run the demo. Expect:
- ~6–10 second wait for cache warm-up
- Streaming reasoning begins, takes 1–3 minutes
- Findings appear at the end
- Cost: $5–15 depending on corpus size

### Step 5.3 — Compare against ground truth

Open your `ground-truth/manual-analysis.md` side-by-side with the Opus output. For each friction you documented:

- ✅ Did Opus surface it? (Coverage)
- ✅ Are the citations correct? (Accuracy)
- ✅ Is severity classified the same way you did? (Calibration)

### Step 5.4 — Iterate based on what you see

| Symptom | Fix location |
|---|---|
| Opus misses a known friction | Adjust prompt, not corpus. Add explicit hint in `prompts/friction-detection-v1.md` |
| Opus hallucinates citations | Tighten the "no hallucinated citations" rule in the system prompt |
| Severity miscalibrated | Add explicit examples in the prompt: *"X type → Y severity"* |
| Output schema mismatch | Adjust both the prompt schema and the frontend parser |

> *Catatan:* Iterasi prompt **lebih murah daripada iterasi corpus**. Kalau Opus miss friction yang Anda tahu ada di corpus, kemungkinan besar prompt-nya yang perlu diperjelas, bukan corpus yang kurang.

### Output of Stage 5

A validated application that surfaces **at least your ground-truth frictions** with correct citations. Bonus findings (frictions you didn't manually catch) need separate human review — treat them as leads, not conclusions.

---

## Cost Estimate for Your Replication

Based on LexHarmoni's actual costs (corpus ~410K tokens, 7 documents):

| Stage | Activity | Estimated Cost |
|---|---|---|
| 1 | Mini research (manual) | $0 |
| 2 | Design conversation Claude.ai Pro | included in $20/mo subscription |
| 3 | Sonnet corpus preparation | $2–5 |
| 4 | Claude Code build | $10–20 |
| 5 | Smoke test (1 cold + 2–3 warm Opus runs) | $10–25 |
| **Total** | | **$22–50** for one full replication cycle |

After replication, **per-analysis ongoing cost** with warm cache (1-hour TTL): ~$1.70 per analysis (corpus cache read $0.28 + user msg auto-cache $1.17 + output $0.25). A regulatory body running 20–30 analyses per month would spend $34–51 monthly in API costs.

> *Catatan:* Estimasi ini untuk korpus seukuran LexHarmoni. Korpus 2x lebih besar = cost 2x. Korpus 5x lebih besar = mungkin perlu hybrid RAG, di luar scope guide ini.

---

## When This Pattern Works (and When It Doesn't)

### ✅ This pattern works well for

- **Small, well-bounded corpora** (≤10 documents, single regulatory domain)
- **Domains with formal hierarchy** — financial regulation, building codes, tax law, healthcare compliance
- **Cross-document friction is the primary analytical task** — not summarization, not Q&A
- **Domain expert is available** to produce ground truth and validate output
- **Stakeholder is comfortable with AI as augmentation**, not replacement

### ⚠️ Marginal fit

- **10–50 document corpora** — costs increase, may need hybrid RAG architecture, but still feasible
- **Cross-jurisdiction analysis** — terminology and hierarchy differences add complexity
- **Soft-law domains** (guidelines, best practices) — friction definitions become fuzzy

### ❌ This pattern doesn't work for

- **100+ document corpora** — token cost prohibitive, RAG-first architecture more appropriate
- **Fuzzy domain boundaries** — if you can't bound the corpus, you can't validate findings
- **Adjudication tasks** — LexHarmoni surfaces friction, it doesn't decide which rule prevails
- **Domains requiring multi-step deduction** — friction detection is pattern matching, not legal reasoning at full depth

---

## Common Replication Mistakes (Anti-Patterns)

Things that have failed in earlier replication attempts (LexHarmoni's own development included):

1. **Skipping Stage 1.** Without ground truth, you have no way to validate. The temptation to "just see what Opus finds" leads to publishing findings that may be hallucinated.

2. **Using Opus for Stage 3.** Bulk metadata extraction is a Sonnet task. Opus is overkill and expensive.

3. **Modifying backend architecture in Stage 4.** The caching logic, SSE streaming, and dual-stream UI took multiple iterations to get right. Don't refactor unless you have a specific reason.

4. **Treating bonus findings as authoritative.** When Opus surfaces frictions you didn't manually catch, those need human review. They're leads, not conclusions.

5. **Not documenting changes.** Fork without changelog entries = unmaintainable in 3 months. Keep `CHANGELOG.md` updated as you go.

---

## What's Next After Replication

Once your domain-specific LexHarmoni is running:

- **Expand the corpus** — but only after the small-corpus version is validated
- **Add evaluation harness** — systematic precision/recall measurement against multiple manual baselines
- **Integrate to drafting workflow** — the natural deployment target is ex-ante review of new drafts before enactment
- **Share back upstream** — if your adaptation produces patterns or prompts that generalize, consider contributing back to LexHarmoni or publishing your fork as a sister project

---

## Getting Help

- **Architecture questions:** see `docs/ARCHITECTURE.md`
- **API reference:** see `docs/USER_MANUAL.md`
- **Issues with replication:** open a GitHub issue tagged `replication`
- **Domain-specific questions:** out of scope for this guide; consult a domain practitioner

---

## Appendix — Three Prompt Templates (Quick Reference)

### Template A — Stage 2 Design Conversation (full text in Stage 2 above)
**Use with:** Claude.ai web, Opus 4.7
**Purpose:** Adapt friction taxonomy + design system prompt + define output schema
**Output:** `prompts/friction-detection-v1.md` for your domain

### Template B — Stage 3 Manifest Generation (full text in Stage 3 above)
**Use with:** Claude.ai web or API, Sonnet 4.6
**Purpose:** Extract structured metadata per document
**Output:** `corpus/manifest.json` entries (run once per document)

### Template C — Stage 4 Codebase Adaptation (full text in Stage 4 above)
**Use with:** Claude Code CLI, in your forked repo directory
**Purpose:** Adapt LexHarmoni codebase to your corpus and domain
**Output:** Working backend + frontend configured for your domain

---

## Closing Note

LexHarmoni was built in a 5-day hackathon by a regulatory practitioner — not an engineer — collaborating with Claude. The fact that this replication guide exists at all is evidence that the pattern is reproducible by other domain experts.

If you replicate this pattern for your domain and it works, consider sharing what you learned. The friction-detection use case generalizes far beyond Indonesian P2P lending; the more domain experts who try this approach, the better we collectively understand where it works and where it breaks.

---

**Author:** Ziffany Firdinal
**License:** This guide is part of the LexHarmoni project, licensed under Apache 2.0.
**Last updated:** April 2026
