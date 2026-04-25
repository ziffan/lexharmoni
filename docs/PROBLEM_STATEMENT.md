# Problem Statement — LexHarmoni

**An exploration of how human regulatory review meets its ceiling at scale, and why a 1M-token context window changes what is architecturally possible.**

---

## Table of Contents

1. [My Workflow as a Regulatory Officer](#1-my-workflow-as-a-regulatory-officer)
2. [The Indonesian P2P Lending Regulatory Corpus](#2-the-indonesian-p2p-lending-regulatory-corpus)
3. [Mini Research — Methodology and Scope](#3-mini-research--methodology-and-scope)
4. [Three Documented Friction Patterns](#4-three-documented-friction-patterns)
5. [Why Human Review Alone Cannot Scale](#5-why-human-review-alone-cannot-scale)
6. [The Opportunity Window](#6-the-opportunity-window)
7. [Scope, Non-Scope, and Intended User](#7-scope-non-scope-and-intended-user)

---

## 1. My Workflow as a Regulatory Officer

I worked as an Officer in the Regulatory Unit at the Indonesia Stock Exchange (IDX). The work was steady and mostly quiet. New capital markets regulation drafts would periodically circulate for internal review, and my job — among other things — was to check whether those drafts created friction with existing rules.

My actual workflow, day-to-day, came down to two tools.

**First, institutional memory.** I would walk to a senior colleague's desk and ask them whether a particular provision had been discussed before, whether there was precedent I should be aware of, whether a similar clause had been tried in another regulation and failed. Those conversations were immensely valuable. Senior regulators carry in their heads a map of connections across hundreds of documents built over decades — which article depends on which, where the exceptions live, which provisions had been quietly softened through implementing circulars. This kind of expert recall is well-documented in cognitive science: skilled performers in knowledge-intensive domains develop long-term working memory structures that let them rapidly access domain content through retrieval cues, far beyond the ~4-chunk active capacity of general working memory (Ericsson & Kintsch, 1995; Cowan, 2001).

**Second, Ctrl+F.** When a draft mentioned a specific term, I would search across the small set of documents I suspected might be relevant. If the term appeared, I would check the context. If it appeared in a context that contradicted the draft, I would flag it.

Both tools worked — for a narrow range of problems.

They worked beautifully when a draft touched one or two existing regulations. Senior colleagues could pull the relevant context from memory; Ctrl+F could confirm their intuition; the friction, if any, was usually surfaced within the day.

They did not work when a draft touched fifteen regulations across a decade of regulatory evolution. At that scale, recall becomes partial. Ctrl+F becomes a matter of guessing the right search terms. Context slips — not from negligence, but because the dependency web between regulations exceeds what any single reviewer can actively traverse during a drafting cycle, even with the deep long-term memory that experienced regulators bring.

This is not a problem unique to IDX. It is a problem inherent to the scale of modern regulatory work.

---

## 2. The Indonesian P2P Lending Regulatory Corpus

To ground the problem, consider the specific corpus LexHarmoni operates on: Indonesia's peer-to-peer (P2P) lending sector, regulated by the Otoritas Jasa Keuangan (OJK).

### 2.1 The hierarchical structure

Indonesian financial regulation follows a strict hierarchy. At the top sits **Peraturan OJK (POJK)** — the primary regulation, which carries the weight of law in its domain. Below that sit **Surat Edaran OJK (SEOJK)** — circular letters that operationalize POJK provisions with implementing detail.

A POJK delegates certain matters to SEOJK for implementation. A SEOJK, in turn, is legally bound by its parent POJK — if the POJK is revoked, the SEOJK's delegation chain is broken, and its legal basis becomes ambiguous unless a saving clause explicitly preserves it.

This hierarchy matters because **friction patterns emerge precisely at the seams** — where saving clauses extend older circulars beyond the life of their parent POJK, where terminology drifts between regulatory generations, where two active regulations governing the same subject matter specify different requirements.

### 2.2 The seven regulations

The LexHarmoni corpus captures seven regulations covering the P2P lending sector over nine years (2016–2025):

**Active in force:**
- **POJK 22/2023** — Consumer Protection in Financial Services
- **POJK 40/2024** — LPBBTI (replaces POJK 10/2022)
- **SEOJK 19/2025** — LPBBTI Implementation (replaces SEOJK 19/2023)

**Historical (revoked or superseded):**
- **POJK 77/2016** — Fintech Lending (original P2P regulation, superseded by POJK 10/2022)
- **POJK 31/2020** — Consumer Services at OJK (several articles revoked by POJK 22/2023)
- **POJK 10/2022** — LPBBTI (Articles 102–104 pre-revoked by POJK 22/2023 on 22 Dec 2023; full repeal by POJK 40/2024 on 27 Dec 2024)
- **SEOJK 19/2023** — LPBBTI Implementation (revoked by SEOJK 19/2025 on 31 Jul 2025; operated with a partially-orphaned delegation chain between Dec 2023 and Jul 2025)

### 2.3 The dependency web

Reading these seven regulations in isolation is straightforward. Reading them as a web is where complexity compounds.

POJK 22/2023 (Consumer Protection) took the unusual step of **surgically revoking Articles 102, 103, and 104 of POJK 10/2022** on 22 December 2023 (via Article 124(1)(f)) — one year before POJK 10/2022 was repealed in full by POJK 40/2024. Article 104(2) of POJK 10/2022 was the specific delegating clause that authorized SEOJK 19/2023's Chapter XI on debt collection procedures.

Once that parent article was pruned, SEOJK 19/2023's Chapter XI remained operationally active but lost its formal legal anchor. The chapter continued to bind P2P operators, but the specific delegation that justified its technical parameters had been severed.

POJK 40/2024 (27 December 2024) subsequently repealed POJK 10/2022 in full and included a **general saving clause** (Article 235) declaring prior implementing regulations "remain in force to the extent not in conflict" (*sepanjang tidak bertentangan*). This saving clause provided transitional cover but did not restore the specific delegation chain for Chapter XI. The orphaning was finally resolved on 31 July 2025, when SEOJK 19/2025 replaced SEOJK 19/2023 entirely, drawing its authority from POJK 40/2024.

Simultaneously, during the December 2023 – July 2025 window, SEOJK 19/2023 contained specifications (for example, collection hours) that differed from parallel specifications in POJK 22/2023 — an active, separate regulation on consumer protection. Reading either regulation in isolation, the conflict was invisible. Reading both together, the conflict was visible but required tracing which specification should prevail under Lex Superior or Lex Posterior doctrine.

And layered on top of this: terminology had already shifted once before, between two simultaneously-active regulations. From July 2022 to December 2023, POJK 10/2022 used the new term *LPBBTI* (Layanan Pendanaan Bersama Berbasis Teknologi Informasi — Technology-Based Joint Funding Service), while POJK 31/2020 — still in force — continued to list "Penyelenggara Layanan Pinjam Meminjam Uang Berbasis Teknologi Informasi" in its PUJK definition. The shift reflects maturation of regulatory thinking, but during the overlap period it produced two active regulations using different identifiers for the same industry.

No single regulator, reading these seven documents sequentially, is likely to catch every friction. Not because they are careless. Because the dependency graph exceeds what working memory can hold.

---

## 3. Mini Research — Methodology and Scope

Before building LexHarmoni, I conducted a **bounded manual legal review** — a mini research exercise — to establish a baseline for what AI-assisted analysis should be able to surface.

### 3.1 Time and scope constraints

The mini research was deliberately bounded:
- **Under 8 hours of focused review time.**
- **Seven regulations only** — enough to capture meaningful cross-document patterns, tractable within the time budget.
- **Three friction categories** — normative, hierarchical, operational — chosen because they map to the three most common ways regulatory friction manifests in Indonesian practice.

The boundedness is important. This is not a definitive legal analysis of the LPBBTI regime. It is a reproducible baseline, scoped to be completed in an afternoon by a single reviewer familiar with the domain. The goal was to establish a **ground truth that LexHarmoni could be validated against** — not to produce exhaustive legal scholarship.

### 3.2 What I was looking for

The mini research focused on three questions:

1. **Are there direct normative conflicts** between two active regulations governing the same subject matter? (These would violate Lex Superior/Posterior principles and require doctrinal resolution.)
2. **Are there orphaned delegation chains** where an implementing SEOJK remains in force after its parent POJK has been revoked, leaving specific provisions without clear legal anchoring?
3. **Are there operational inconsistencies** — terminology drift, definitional ambiguity, redundant reporting requirements — that would create compliance overhead without serving a clear regulatory purpose?

### 3.3 Reading protocol

I read the seven regulations in rough chronological order, keeping a running notebook of:
- Specific articles cited in multiple regulations
- Saving clauses and their scope
- Terminology and definitional shifts
- Delegation chains and their current status post-revocation

The output is documented in [`ground-truth/manual-analysis.md`](../ground-truth/manual-analysis.md). It is not polished legal opinion. It is the working notes of a single reviewer, intentionally preserved in their rough form so that LexHarmoni's output can be compared against them directly.

### 3.4 Why manual baseline matters

Evaluation of AI output in legal contexts cannot rely on generic benchmarks. A regulatory friction-detection tool needs domain-specific validation. By producing a manual baseline first — with all its limitations — I established a concrete comparison point: *these are the patterns a single reviewer found in 8 hours; here is what the tool surfaces in 2 minutes; where do they agree, where do they differ, and what does each approach miss that the other catches?*

---

## 4. Three Documented Friction Patterns

The mini research surfaced three distinct friction patterns. Each has been independently detected by LexHarmoni across multiple validation runs, with specific article-level citations matching the manual baseline.

**A note on framing:** All three friction patterns documented below have since been resolved through subsequent OJK regulation (POJK 22/2023 for terminology; SEOJK 19/2025 for collection hours and orphaned Chapter XI). The manual review was deliberately scoped to previously-documented, since-resolved frictions so that LexHarmoni's detections could be validated against a known ground truth: if the tool surfaces these patterns with correct citations and correct severity classification, that is evidence the full-corpus reasoning approach works. It does not establish that the tool can detect frictions that have not yet been identified by humans — that is a separate validation question, addressed under "Ex-ante deployment validation" in §7.4.

### 4.1 Normative friction: Collection-hours mismatch

**Severity: Critical**
**Friction window: 22 Dec 2023 – 31 Jul 2025 (~19 months)**
**Current status: Resolved by SEOJK 19/2025**

Between December 2023 and July 2025, POJK 22/2023 (Consumer Protection, Article 62(2)(f)) and SEOJK 19/2023 (LPBBTI Implementation, Chapter XI point 5(d)(8)) specified conflicting time windows for permissible debt collection:

- **POJK 22/2023:** Monday–Saturday, excluding national holidays, 08:00–20:00 local time.
- **SEOJK 19/2023:** 08:00–20:00 debtor's local time, with no restriction on days of week.

Both regulations were active during this window. Both applied to P2P lending operators. They specified different permissible hours. Reconciling them required applying Lex Superior doctrine — POJK as the higher-hierarchy regulation prevails over SEOJK — or Lex Posterior doctrine — the later-in-time regulation prevails. Both doctrines required conscious application; they were not automatic.

The friction was eliminated in SEOJK 19/2025, which removed the specific hour/day specification from Chapter XI and attributed collection timing entirely to the consumer-protection POJK: *"Penagihan... dilaksanakan sesuai dengan ketentuan peraturan perundang-undangan yang mengatur mengenai pelindungan konsumen dan masyarakat di sektor jasa keuangan."*

**Why this was invisible to single-document review:** Reading POJK 22/2023 alone, its collection-hours specification seemed definitive. Reading SEOJK 19/2023 alone, its specification also seemed definitive. The conflict emerged only when both were read together and reconciled against Lex doctrine.

**How LexHarmoni surfaces it:** By loading both regulations into the same reasoning context, the model can cross-reference collection-hours specifications across all regulations simultaneously and flag the normative conflict with citations to both articles. Retrospective detection validates tool capability against a friction whose resolution timeline is now known.

### 4.2 Hierarchical friction: Orphaned Chapter XI

**Severity: Major**
**Friction window: 22 Dec 2023 – 31 Jul 2025 (~19 months)**
**Current status: Resolved by SEOJK 19/2025**

SEOJK 19/2023 was originally issued under explicit delegation authority from several articles of POJK 10/2022, including Article 104(2) — the specific authority for Chapter XI on debt collection procedures. This delegation chain is verifiable in SEOJK 19/2023's opening recital, which cites *Pasal 104 ayat (2) POJK 10/2022* by name.

On 22 December 2023, POJK 22/2023 (Consumer Protection) took the unusual step of revoking specific articles of POJK 10/2022 — Articles 102, 103, and 104 — while leaving the rest of POJK 10/2022 intact. This was a **surgical revocation**, not a full repeal.

The consequence: from 22 December 2023 onward, Chapter XI of SEOJK 19/2023 was operationally active but its delegating parent article (Article 104(2)) no longer existed. The chapter continued to bind P2P operators, but its formal hierarchical anchor had been severed.

POJK 40/2024 (27 December 2024) subsequently repealed POJK 10/2022 in full and included a general saving clause (Article 235) declaring prior implementing regulations "remain in force to the extent not in conflict." This saving clause provided transitional cover but did not restore the specific delegation chain for Chapter XI.

The orphaning was finally resolved on 31 July 2025, when SEOJK 19/2025 replaced SEOJK 19/2023 entirely, drawing its authority from POJK 40/2024 articles that explicitly re-delegate collection-procedure implementation.

This was not a catastrophic situation — the chapter's substantive provisions were generally sensible, and the general saving clause provided legal cover — but it was a structural irregularity that, left unresolved for 19 months, created ambiguity about the hierarchical authority underlying Chapter XI's requirements.

**Why this was invisible to single-document review:** The orphaning became visible only when four facts were held simultaneously: (a) POJK 22/2023 pre-revoked Articles 102–104 of POJK 10/2022, (b) SEOJK 19/2023's Chapter XI specifically cited Article 104(2) as its authority, (c) POJK 40/2024 later repealed POJK 10/2022 in full without re-establishing equivalent specific delegation, and (d) SEOJK 19/2023 remained in force throughout this period.

**How LexHarmoni surfaces it:** By holding the delegation-chain metadata across all seven regulations in context simultaneously, the model traces each SEOJK provision back to its parent POJK article and flags where that parent article has been revoked — regardless of whether the revocation was surgical (POJK 22/2023) or via full repeal (POJK 40/2024).

### 4.3 Operational friction: Terminology inconsistency between active regulations

**Severity: Minor**
**Friction window: 4 Jul 2022 – 22 Dec 2023 (~17 months)**
**Current status: Resolved by POJK 22/2023**

Indonesian P2P lending regulation underwent a definitional shift in July 2022:

- **Before:** POJK 77/2016 used *Pinjam Meminjam Uang* (lending-borrowing) — framed as bilateral credit transaction.
- **After (4 Jul 2022):** POJK 10/2022 reframed the industry as *LPBBTI* — Layanan Pendanaan Bersama Berbasis Teknologi Informasi — to accommodate Sharia-compliant variants where *pinjam meminjam* was doctrinally unsuitable. This rationale is stated explicitly in the POJK 10/2022 Penjelasan Umum.

The friction was not the shift itself, but the **lag in cross-regulatory terminology alignment**. From 4 July 2022 to 22 December 2023, POJK 10/2022 used the new LPBBTI terminology while POJK 31/2020 — still active — continued to list *"Penyelenggara Layanan Pinjam Meminjam Uang Berbasis Teknologi Informasi"* in its PUJK definition. Two active regulations referred to the same industry by different names.

The inconsistency was resolved on 22 December 2023 when POJK 22/2023 was enacted, adopting the new terminology consistently across its provisions (including in its definition of *Lembaga Jasa Keuangan Lainnya*) and revoking the specific PUJK-definition article in POJK 31/2020 that used the outdated term.

This is the mildest of the three frictions — it does not create normative conflict, merely ambiguity about which regulatory identifier applies. But it is instructive as a class: regulators updating core terminology must simultaneously update cross-referencing regulations, or risk temporary incoherence.

**Why this is visible to single-document review but rarely flagged:** A reviewer reading POJK 10/2022 alone would not know that POJK 31/2020 continued to use older terminology. A reviewer reading both would notice the shift, but might not flag it as a problem unless actively tracking cross-regulatory definitional consistency.

**How LexHarmoni surfaces it:** Cross-corpus pattern detection compares how each regulation uses key terms and flags where two active regulations use inconsistent identifiers for the same regulated entity.

---

## 5. Why Human Review Alone Cannot Scale

The three friction patterns above each persisted for 17–19 months before being resolved through subsequent OJK regulation. This is not unusual. It is what happens at the intersection of three hard constraints:

### 5.1 Reading capacity limits

Sustained focused reading of dense legal text is bounded by two factors: reading rate and attention persistence. Meta-analyses place average adult reading rates for non-fiction at ~238 wpm (Brysbaert, 2019); for dense technical or legal text with full comprehension, effective rates drop to roughly 150–200 wpm. At those rates, the LPBBTI corpus — seven regulations totaling roughly 150,000 words of dense legal text — represents 12–16 hours of continuous reading time before any cross-referencing or note-taking. Even split across multiple focused sessions, holding the integrated structure of the full corpus in active working memory is bounded by the ~4-chunk capacity of focal attention (Cowan, 2001), which is why expert review relies heavily on long-term working memory and external aids (notes, indexes, Ctrl+F) rather than pure recall.

### 5.2 Cross-reference complexity growth

The complexity of regulatory friction scales quadratically with corpus size for pairwise dependencies, and polynomially (O(nᵏ)) for k-hop chains. With two documents, there is one possible dependency pair. With seven documents, there are 21. With 50 documents (OJK's full Consumer Protection domain), there are 1,225 pairwise dependencies — and many actual frictions are not pairwise. The orphaned-Chapter-XI pattern documented in §4.2, for example, is a 4-hop dependency (POJK 22/2023 → POJK 10/2022 Art. 104(2) → SEOJK 19/2023 Chapter XI ← POJK 40/2024 saving clause). Human review can audit pairwise dependencies exhaustively at low corpus counts; multi-hop dependency traversal becomes intractable far earlier.

### 5.3 Temporal drift

Regulatory corpora are not static. Regulations are amended, revoked, and introduced. A reviewer who internalized the corpus state in March may find their mental model stale by October. Maintaining an accurate dependency graph across time requires continuous re-reading — which compounds reading capacity constraints.

### 5.4 What this is not

Nothing in this analysis should be read as criticism of regulators or regulatory reviewers. Regulatory work is thoughtful, careful, and done by people who care about getting it right. The 17–19 month persistence of the frictions documented above is not evidence of failure. It is evidence of a **structural constraint**: human cognitive capacity is bounded, regulatory corpora are growing, and the gap between what is humanly reviewable and what regulation actually contains is widening.

What is needed is not better reviewers. What is needed is **tools that scale with the corpus**.

---

## 6. The Opportunity Window

The ability to address this problem computationally is very recent — measured in months, not years. Three technical capabilities had to mature simultaneously for LexHarmoni to become architecturally possible:

### 6.1 1M-token context windows

Claude Opus 4.7 supports a 1M-token context window. This is the first commercial model where loading an entire mid-size regulatory corpus (hundreds of thousands of tokens) into a single inference becomes viable. Earlier models forced architectural compromises — either chunked retrieval (losing cross-document reasoning) or sliding-window processing (losing global coherence). 1M context makes full-corpus reasoning a design option, not a constraint.

### 6.2 Prompt caching with extended TTL

Naively, loading a 500K-token corpus per inference would cost $5–10 per query — prohibitive for routine use. Anthropic's prompt caching with extended 1-hour TTL (via the `extended-cache-ttl-2025-04-11` beta header) changes the economics: the corpus is cached once, reads are ~10% of write cost, and the cache persists across multiple consecutive queries. Runs 2+ in a warm window cost roughly $1.70 each — economically routine.

### 6.3 Streaming with intermediate reasoning

Black-box legal AI is a non-starter. A regulator cannot be asked to trust a model that says "here is the friction" without showing its work. Streaming output — where the model's reasoning unfolds token-by-token in real time, visible to the reviewer — turns AI output into something auditable. The reviewer watches the model trace citations; if the trace goes astray, they see it immediately and discount the output. Streaming is not just a UX choice; it is what makes AI output acceptable in legal contexts at all.

### 6.4 What was not possible 18 months ago

Before these three capabilities converged, a tool like LexHarmoni was not buildable. Earlier context windows (200K, 32K) forced RAG architectures that fragmented cross-document reasoning. Earlier cache economics made repeated corpus loading unaffordable. Non-streaming output forced reviewers to accept or reject opaque results. Each constraint is individually resolvable; their simultaneous resolution in Opus 4.7 is what makes the full-corpus approach architecturally sensible now.

This is the opportunity window LexHarmoni sits in.

---

## 7. Scope, Non-Scope, and Intended User

### 7.1 What LexHarmoni is

LexHarmoni is a **stress-test harness for regulatory drafting**. It accepts a draft regulation as input, loads a corpus of existing regulations in the same domain, and surfaces friction patterns — normative conflicts, hierarchical gaps, operational inconsistencies — with article-level citations and severity assessments.

The intended mental model: *just as software engineers run test suites before shipping code, regulatory drafters can run friction tests before enacting regulation.*

### 7.2 What LexHarmoni is not

- **Not a legal opinion generator.** LexHarmoni surfaces patterns. Doctrinal resolution (Lex Superior, Lex Posterior, Lex Specialis) requires human legal judgment.
- **Not a substitute for senior regulatory counsel.** The tool augments review; it does not replace reviewers. A senior regulatory counsel still signs off on regulation.
- **Not a general-purpose legal AI.** The current corpus is seven Indonesian P2P lending regulations. The tool is not tested on other jurisdictions, other regulatory domains, or other legal systems. Extending scope requires new corpus curation and new validation.
- **Not an adjudicator.** When LexHarmoni flags a normative conflict, it does not decide which regulation prevails. It surfaces the conflict; humans decide.
- **Not a definitive analysis tool.** The mini research baseline is under 8 hours. LexHarmoni's validation against that baseline shows it catches the core patterns; it may miss patterns that a more thorough manual analysis would catch, and it may surface secondary patterns that require additional review to evaluate.

### 7.3 Intended user

The primary intended user is a **regulatory drafter or reviewer within an OJK-equivalent body** who is working on a new draft regulation in a domain with an existing corpus of related rules. The user is assumed to have:

- Domain expertise in the relevant regulatory area.
- Familiarity with Indonesian legal doctrine (Lex Superior, saving clauses, delegation chains).
- Authority and responsibility for the final regulatory decision.

LexHarmoni is designed to slot into their workflow as a **second pair of eyes** — one that can hold more context simultaneously than any single reviewer could carry in working memory.

The tool is not designed for:
- Non-specialist users seeking legal interpretation.
- Consumers attempting to understand their rights under P2P regulations.
- Compliance officers looking for a definitive compliance checklist.

### 7.4 The upgrade paths

The current prototype is deliberately scoped — seven regulations, retrospective validation, plain Opus 4.7 output without adaptive thinking enabled. This scoping was driven by hackathon constraints (5-day build window, bounded budget). Natural upgrade paths that would increase LexHarmoni's utility:

- **Adaptive thinking mode.** Enabling Opus 4.7's adaptive thinking (the default-off reasoning mode that can be enabled via `thinking: {type: "adaptive"}`) may deepen normative conflict detection, particularly for subtle doctrinal reconciliation. Initial experimentation is deferred to post-hackathon.
- **Corpus expansion.** Scaling from 7 to 50+ POJK across the full Consumer Protection domain would test whether the full-corpus approach scales economically and whether friction detection quality holds at larger corpus sizes.
- **Cross-ministry friction.** Indonesian financial regulation involves multiple regulators (OJK, Bank Indonesia, Kemenkeu, Kemenkominfo). Extending the corpus across ministerial boundaries would surface a distinct class of friction invisible to single-regulator review.
- **Ex-ante deployment validation.** The current validation is retrospective (analyzing already-enacted POJK 40/2024 against its surrounding corpus). Deploying LexHarmoni in an active drafting workflow, where drafts circulate before enactment, requires different validation protocols.
- **Systematic evaluation harness.** A reproducible evaluation framework measuring LexHarmoni's precision and recall against multiple manual baselines would turn the current validation from proof-of-concept into measurable capability.

---

## Closing Note

LexHarmoni is one experiment in giving regulators a safety net that didn't exist before — a second pair of eyes on drafts that have more context than any single reviewer could hold. The problem it addresses is not new; the architectural tools to address it are. This document attempts to be honest about both.

The code, corpus, manual baseline, and validation outputs are all open-source and auditable. If you are a regulatory practitioner, legal technologist, or researcher interested in any aspect of this work, engagement is welcome.

---

## References

- Brysbaert, M. (2019). How many words do we read per minute? A review and meta-analysis of reading rate. *Journal of Memory and Language*, 109, 104047.
- Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*, 24(1), 87–114.
- Ericsson, K. A., & Kintsch, W. (1995). Long-term working memory. *Psychological Review*, 102(2), 211–245.

---
**Author:** Ziffany Firdinal
**Credentials:** Former Regulatory Officer, Indonesia Stock Exchange (IDX). OJK-registered Capital Markets Legal Consultant.
**Date:** April 2026
**Context:** Written during the Anthropic *"Built with Opus 4.7"* Hackathon.

Related documents:
- [`README.md`](../README.md) — project overview
- [`ground-truth/manual-analysis.md`](../ground-truth/manual-analysis.md) — mini research baseline
- [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) — technical architecture deep-dive
