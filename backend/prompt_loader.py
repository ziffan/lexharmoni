# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

import json
import re
from pathlib import Path

BASE = Path(__file__).parent.parent

BLOCK1_ROLE = """\
You are a senior regulatory counsel specializing in Indonesian financial
services law, specifically Otoritas Jasa Keuangan (OJK) regulations governing
peer-to-peer lending (LPBBTI — Layanan Pendanaan Bersama Berbasis Teknologi
Informasi).

Your task: analyze a proposed regulation draft against an existing corpus of
in-force and historical OJK regulations, and identify regulatory FRICTION.

## What is Regulatory Friction?

Friction occurs when a proposed regulation creates internal inconsistency in
the legal system. You will detect three types, ranked by severity:

### Type 1 — NORMATIVE FRICTION (Severity: CRITICAL)
Direct conflict between two rules that BOTH purport to govern the same subject
matter. A regulated party cannot comply with one without violating another.
Creates legal uncertainty and arbitrage opportunities.

Example pattern: Regulation A requires X hours. Regulation B requires Y hours
for the same activity. Neither regulation supersedes the other explicitly.

### Type 2 — HIERARCHICAL FRICTION (Severity: MAJOR)
Two sub-patterns:

(a) Lex Superior/Posterior violation: lower-hierarchy regulation persists
    after its higher-hierarchy basis is revoked, OR a newer regulation
    silently contradicts an older unrevoked one at the same level.

(b) Implicit Vacuum / Orphaned Delegation: a regulation references or
    implements articles from another regulation that have since been revoked,
    leaving operational gaps. The orphaned provisions may still be cited
    but have no legal foundation.

Example pattern: SEOJK (circular letter, hierarchy 4) implements articles of
a POJK (regulation, hierarchy 3). The POJK articles get revoked by a newer
POJK. The SEOJK articles remain in force, pointing to nothing.

### Type 3 — OPERATIONAL FRICTION (Severity: MINOR)
Non-conflicting inconsistencies that cause practical friction: terminology
mismatches across regulations governing the same subject, redundant reporting
obligations, or inconsistent definitions.

Example pattern: Regulation A calls a party "Pemberi Pinjaman" (Lender).
Regulation B, governing the same sector in the same era, calls the same
role "Pemberi Dana" (Fund Provider). Operators must map terminology.

## Indonesian Legal Hierarchy (OJK Context)

| Level | Instrument | Abbr |
|---|---|---|
| 1 | Undang-Undang | UU |
| 2 | Peraturan Pemerintah | PP |
| 3 | Peraturan OJK | POJK |
| 4 | Surat Edaran OJK | SEOJK |

Lex Superior: higher level prevails over lower.
Lex Posterior: newer prevails over older at the same level.
Lex Specialis: specific prevails over general (within the same level).

## Key Principles for Your Analysis

1. **Era-aware terminology:** Same legal concept may have different labels
   across time. "Pemberi Pinjaman" (2016-2022 era) ≈ "Pemberi Dana" (2022+
   era). Treat equivalent concepts as equivalent; treat terminology change
   itself as Operational friction if material.

2. **Quote before you reason:** Before concluding a friction exists, quote
   the exact article text from both regulations. Do not paraphrase and then
   reason from the paraphrase.

3. **Revocation scope matters:** A POJK may be "fully revoked" or "partially
   revoked." Check the manifest for scope. Articles revoked partially may
   still be in force for other subjects.

4. **Saving clauses create legal limbo:** Open-ended saving clauses (e.g.,
   "previous implementing regulations remain in force insofar as not
   contradictory") create interpretation space. Flag these explicitly.

5. **Temporal window matters:** Note when each friction became ACTIVE (draft
   date) and when resolved (if applicable). Friction that ran for months
   before resolution is demo gold.

6. **No hallucinated citations:** If you cannot find a specific article
   number in the provided corpus, say so. Do not invent citations.\
"""


def _read(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_system_blocks() -> list[dict]:
    manifest_path = BASE / "corpus" / "manifest.json"
    manifest_text = json.dumps(
        json.loads(_read(manifest_path)), ensure_ascii=False, indent=2
    )

    active_dir = BASE / "corpus" / "active"
    active_files = ["POJK-22-2023.txt", "POJK-40-2024.txt", "SEOJK-19-2025.txt"]
    active_text = (
        "# ACTIVE REGULATIONS CORPUS\n# These regulations are currently in force.\n\n"
    )
    for fname in active_files:
        reg_id = fname.replace(".txt", "")
        active_text += f"--- REGULATION: {reg_id} ---\n"
        active_text += _read(active_dir / fname)
        active_text += "\n\n"

    historical_dir = BASE / "corpus" / "historical"
    historical_files = [
        "POJK-77-2016.txt",
        "POJK-31-2020.txt",
        "POJK-10-2022.txt",
        "SEOJK-19-2023.txt",
    ]
    historical_text = (
        "# HISTORICAL REGULATIONS CORPUS\n"
        "# These regulations have been revoked or superseded.\n"
        "# They remain relevant for detecting legacy citations and transitional frictions.\n\n"
    )
    for fname in historical_files:
        reg_id = fname.replace(".txt", "")
        historical_text += f"--- REGULATION: {reg_id} ---\n"
        historical_text += _read(historical_dir / fname)
        historical_text += "\n\n"

    def block(text: str) -> dict:
        return {
            "type": "text",
            "text": text,
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        }

    return [
        block(BLOCK1_ROLE),
        block(manifest_text),
        block(active_text),
        block(historical_text),
    ]


def build_user_message(draft_id: str, draft_text: str) -> str:
    return f"""\
# DRAFT UNDER TEST

**Identifier:** {draft_id}
**Content:**

{draft_text}

---

# TASK

Analyze this draft against the corpus provided in your system context.
Identify all regulatory frictions it creates or resolves.

## Output Protocol

Produce your analysis in TWO sequential sections, in this exact order:

### Section 1 — <reasoning>

Inside `<reasoning>` tags, produce natural-language analysis visible to the
human reviewer. For each candidate friction:

1. **Quote** the specific articles from both the draft and the corpus.
2. **Identify** the friction type (Normative / Hierarchical / Operational).
3. **Assess** severity and practical impact.
4. **Determine** temporal window (when active, when resolved if applicable).

You MAY think step-by-step, reconsider hypotheses, or note uncertainty. This
section is for human readers.

### Section 2 — <findings>

Inside `<findings>` tags, produce a single JSON object matching this schema
EXACTLY (no markdown fences, no extra prose):

{{
  "draft_id": "string",
  "analysis_timestamp": "ISO8601",
  "findings": [
    {{
      "id": "F001",
      "type": "normative|hierarchical|operational",
      "severity": "critical|major|minor",
      "title": "short human-readable title",
      "summary": "1-2 sentence plain-language summary",
      "affected_regulations": [
        {{
          "regulation_id": "must match manifest",
          "article_or_section": "e.g. 'Pasal 62 ayat (3)' or 'Bab XI'",
          "quoted_text": "verbatim quote, max 500 chars",
          "role": "source|target|draft"
        }}
      ],
      "reasoning_steps": [
        "step 1: observation",
        "step 2: cross-reference",
        "step 3: conclusion"
      ],
      "temporal_window": {{
        "friction_active_from": "YYYY-MM-DD or null",
        "friction_active_until": "YYYY-MM-DD or null if ongoing",
        "duration_months": "integer or null"
      }},
      "recommended_resolution": "concrete drafting suggestion",
      "confidence": "high|medium|low"
    }}
  ],
  "summary_stats": {{
    "total_findings": 0,
    "by_severity": {{"critical": 0, "major": 0, "minor": 0}},
    "by_type": {{"normative": 0, "hierarchical": 0, "operational": 0}}
  }}
}}

## Depth Requirements (Tiered)

- **Normative + Hierarchical findings:** Full depth. All fields populated.
  `reasoning_steps` should have 3-6 items. `quoted_text` is REQUIRED.
- **Operational findings:** Surface-level acceptable. `reasoning_steps` can
  be 1-2 items. Populate `quoted_text` only if quickly extractable.

If you find zero frictions of a type, return empty array for that type —
do NOT fabricate findings to fill quotas.

## Priority Focus for This Corpus

Based on the LPBBTI regulatory history in the corpus, pay special attention to:

1. Collection hours / debt collection timing (cross-check POJK 22/2023 vs
   SEOJK 19/2023 and any draft changes).
2. Consumer protection delegation chains (check if any draft references
   articles that have been revoked in POJK 10/2022).
3. Terminology drift ("Pinjam Meminjam" vs "LPBBTI", "Pemberi Pinjaman" vs
   "Pemberi Dana").
4. Saving clauses creating legal limbo.

These are KNOWN historical frictions. Do not assume they appear in this draft,
but prioritize these checks first.

## Severity Assignment Rules (STRICT — do not deviate)

Severity is determined by FRICTION TYPE, not by contextual reasoning:

- normative → ALWAYS severity: "critical"
- hierarchical → ALWAYS severity: "major"  
- operational → ALWAYS severity: "minor"

Do NOT downgrade severity because a friction is "being resolved" or 
"partially mitigated by a saving clause." Severity describes the TYPE 
of friction, not its resolution status. Resolution status is captured 
in temporal_window, not severity.

If a finding genuinely spans multiple types (e.g., a normative conflict 
perpetuated by a saving clause), classify by the MOST SEVERE applicable 
type: normative > hierarchical > operational.

Begin your analysis now.\
"""


def parse_findings(text: str) -> dict:
    match = re.search(r"<findings>(.*?)</findings>", text, re.DOTALL)
    if not match:
        raise ValueError("findings_not_found")
    raw = match.group(1).strip()
    # strip markdown code fences if model wraps JSON in ```json ... ```
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        import sys

        print(f"[PARSE_ERROR] JSONDecodeError: {e}", file=sys.stderr, flush=True)
        print(
            f"[PARSE_ERROR] raw preview: {repr(raw[:300])}", file=sys.stderr, flush=True
        )
        raise
