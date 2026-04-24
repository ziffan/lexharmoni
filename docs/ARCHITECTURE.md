# LexHarmoni — Architecture Decisions (Day 1 End)

## AD-001: Corpus Injection via Prompt Caching
**Decision:** Corpus 7 regulasi + manifest.json dimuat ke `system` prompt
sebagai 4 cached blocks dengan `cache_control: {type: "ephemeral", ttl: "1h"}`
via Anthropic extended-cache-ttl beta (`anthropic-beta: extended-cache-ttl-2025-04-11`).

**Rationale:**
- Corpus static per session. Cache hit reduce cost ~83% on input tokens.
- Corpus size aktual: ~554K tokens total (410K corpus + 144K system + manifest).
  Cost cold (corpus write): ~$6.75/run. Cost warm (cache read): ~$1.70/run.
- 1h TTL dipilih agar seluruh recording session (3-4 runs) masuk dalam satu window.

**Implementation:**
- Backend menyusun `system` array:
  1. Block 1 (cached): role + framework definitions
  2. Block 2 (cached): manifest.json content
  3. Block 3 (cached): corpus active (3 regulasi)
  4. Block 4 (cached): corpus historical (4 regulasi)
- User message berisi draft under test (tidak di-cache secara eksplisit;
  Anthropic auto-cache via cache_write_5m).

**Trade-off accepted:**
- Cache warm-up request pertama tetap full cost (~$6.75).
- User message auto-cached oleh Anthropic setiap run ($1.17/run) — tidak bisa dimatikan.

## AD-002: Hybrid Output Streaming
**Decision:** Streaming text reasoning (SSE) → final structured JSON block
di akhir response.

**Format:**
```
<reasoning>
[streamed token-by-token Opus thinking + explanation for user]
</reasoning>

<findings>
{JSON structured output per schema}
</findings>
```

**Rationale:**
- UX: User lihat Opus "berpikir" real-time (demo gold).
- Parsing: JSON di delimiter `<findings>...</findings>` trivial di frontend.
- Extended thinking / adaptive thinking TIDAK diaktifkan — output adalah plain Opus 4.7 reasoning, bukan thinking blocks.

**Implementation:** FastAPI stream via SSE. Frontend parse `<findings>` setelah
stream done.

## AD-003: POJK 40/2024 sebagai Retrospective Draft
**Decision:** Sistem ship dengan POJK 40/2024 pre-loaded sebagai "draft under
test" untuk demo. Corpus historical yang dibandingkan: POJK 77/2016, POJK
31/2020, POJK 10/2022, SEOJK 19/2023. Corpus active yang jadi pembanding:
POJK 22/2023.

**Rationale:**
- Ground truth sudah ada (manual-analysis.md) = evaluable.
- Retrospective validation = narrative kuat demo: "Opus temukan yang regulator
  butuh 19 bulan untuk temukan."
- User tidak perlu upload apapun untuk demo → zero friction.

**Implementation:** 
- Frontend: default state = POJK 40/2024 loaded sebagai draft.
- Upload feature tetap ada sebagai "advanced" option, tapi bukan default path.
- Backend treat POJK 40/2024 differently: jangan ikutkan dalam corpus reasoning
  pool, tapi di-mark sebagai `draft_under_test`.

## AD-004: Three-Tier Detection, Tiered by Depth
**Decision:** Prompt request semua 3 tipe friksi (Normative, Hierarchical,
Operational), tapi dengan instruction tiered depth:
- Normative + Hierarchical: full deep analysis dengan reasoning steps.
- Operational: surface-level flagging (title + affected regulations + 1-sentence
  rationale).

**Rationale:**
- Demo butuh 2 case deep (Normative jam penagihan, Hierarchical dangling clause).
- Operational di UI showcase only (per konteks v4 §4.4).
- Hedge terhadap quality degradation dari "too many asks."

## AD-005: Model Selection
**Decision:** 
- Integration smoke test: `claude-sonnet-4-6` (plumbing validation only, no
  quality judgment).
- Real detection run: `claude-opus-4-7`.
- Tidak ada fallback otomatis. Switch model = config change.

**Parameter constraints:**
- `temperature`, `top_p`, `top_k`: default (NOT configurable).
- `thinking`: NOT enabled (plain output mode).
- `max_tokens`: 128,000 (Opus 4.7 actual API limit; verified from official docs).

