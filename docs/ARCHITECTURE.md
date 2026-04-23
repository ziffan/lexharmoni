# LexHarmoni — Architecture Decisions (Day 1 End)

## AD-001: Corpus Injection via Prompt Caching
**Decision:** Corpus 7 regulasi + manifest.json dimuat ke `system` prompt
sebagai cached blocks (Anthropic prompt caching, TTL 5 menit default;
opsional 1 jam untuk demo session via `cache_control: {type: "ephemeral",
ttl: "1h"}`).

**Rationale:**
- Corpus static per session. Cache hit reduce cost ~90% on input tokens.
- Estimasi corpus size: ~150-200K tokens (7 regulasi lengkap).
  Cost uncached: ~$2.25-3/request input. Cached: ~$0.22-0.30/request.
- Budget $500 jadi sustain ~40-60 Opus runs plus experimentation.

**Implementation:**
- Backend menyusun `system` array:
  1. Block 1 (cached): role + framework definitions
  2. Block 2 (cached): manifest.json content
  3. Block 3 (cached): corpus active (3 regulasi)
  4. Block 4 (cached): corpus historical (4 regulasi)
- User message berisi draft under test (tidak di-cache).

**Trade-off accepted:**
- Cache warm-up request pertama tetap full cost.
- TTL 5 menit = demo harus smooth, tidak ada jeda 5+ menit di tengah recording.

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
- Opus extended thinking ter-expose ke UI = showcase "adaptive thinking".

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
- `thinking`: `{type: "adaptive"}`.
- `max_tokens`: 16000 (reasoning + JSON bisa panjang).

