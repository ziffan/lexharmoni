# LexHarmoni — Budget Tracker

**Session start:** 2026-04-23
**Source:** `claude_api_cost_2026_04_01_to_2026_04_24.csv` + `claude_api_cost_2026_04_24_to_2026_04_24-update.csv` + `claude_api_cost_2026_04_24_to_2026_04_24-streamfix.csv` + Claude Code invoice

---

## API Actual Cost — 2026-04-23 (dari CSV)

### Claude Opus 4.7

| Token type | Biaya aktual |
|---|---|
| input_no_cache | $2.79 |
| input_cache_read | $0.55 |
| input_cache_write_1h | $5.55 |
| output | $0.89 |
| **Opus Total** | **$9.78** |

### Claude Sonnet 4.6

| Token type | Biaya aktual |
|---|---|
| input_no_cache | $0.03 |
| input_cache_read | $0.86 |
| input_cache_write_5m | $0.00 |
| input_cache_write_1h | $2.46 |
| output | $1.03 |
| **Sonnet Total** | **$4.38** |

**Total API aktual: $14.16**

Note: Cache write Sonnet ($2.46) lebih tinggi dari estimasi karena beberapa gagal warm-up di ST1.
Cache write Opus ($5.55) mencerminkan 3 run ST2 — kemungkinan cache expired antara run sehingga
write terjadi lebih dari 1×.

---

## Estimasi per Run (perbandingan estimasi vs aktual)

### Smoke Test 1 — Sonnet 4.6

| Call | cache_creation | cache_read | input | output | Est. cost |
|---|---|---|---|---|---|
| R1 (warm-up, multiple failed) | ~409,540 | 0 | ~1,314 | ~10,000 | ~$1.24 |
| R1 (confirmed) | 0 | 409,540 | 1,314 | 10,458 | ~$0.28 |
| R2 (confirmed) | 1,311 | 409,540 | 3 | 9,980 | ~$0.28 |
| **ST1 est.** | | | | | **~$1.80** |

### Smoke Test 2 — Opus 4.7

| Call | cache_creation | cache_read | input | output | Est. cost |
|---|---|---|---|---|---|
| R1 (cache write) | ~409,540 | 0 | ~1,500 | ~15,000 | ~$2.43 |
| R2 (cache warm) | ~0 | ~409,540 | ~1,500 | ~15,000 | ~$0.58 |
| R3 (cache warm) | ~0 | ~409,540 | ~1,500 | ~15,000 | ~$0.58 |
| **ST2 est.** | | | | | **~$3.59** |

---

## API Actual Cost — 2026-04-24 (dari CSV streamfix — final)

### Claude Opus 4.7

| Token type | Biaya aktual | Token est. |
|---|---|---|
| input_no_cache | $6.54 | ~1.31M tokens (~7 runs × 186K) |
| input_cache_read | $2.50 | ~5.00M tokens (~9 reads × 554K) |
| input_cache_write_5m | $2.33 | ~373K tokens (2× user msg auto-cache) |
| input_cache_write_1h | $5.55 | ~555K tokens (corpus re-write, cache expired) |
| output | $2.00 | ~80K tokens (~9 calls × 8.9K avg) |
| **Opus Total April 24** | **$18.92** | |

### Claude Sonnet 4.6 (April 24)

| Token type | Biaya aktual | Token est. |
|---|---|---|
| input_no_cache | $0.00 | ~0 |
| input_cache_write_1h | $2.46 | ~410K tokens (1 corpus write) |
| output | $0.01 | ~670 tokens |
| **Sonnet Total April 24** | **$2.47** | |

**April 24 total: $21.39**

Note: +$2.87 dari CSV sebelumnya ($18.52→$21.39) — berasal dari sesi streaming fix (~2 Opus verify/debug run tambahan). Sonnet $2.47 berasal dari curl diagnostic saat debugging SSE — men-trigger corpus cache write Sonnet $2.46 yang tidak disengaja. `input_cache_write_5m` = user message POJK-40-2024 (~186K tokens) auto-cached 2× oleh Anthropic.

---

## Running Total — Aktual

| Item | Biaya | Tanggal |
|---|---|---|
| API — Sonnet 4.6 | $4.38 | 2026-04-23 |
| API — Opus 4.7 | $9.78 | 2026-04-23 |
| API — Opus 4.7 | $18.92 | 2026-04-24 |
| API — Sonnet 4.6 | $2.47 | 2026-04-24 |
| **Total API aktual** | **$35.55** | |
| Claude Code (sesi 2026-04-23) | $11.11 | 2026-04-23 |
| Claude Code (sesi 2026-04-24) | TBD | 2026-04-24 |
| **Grand Total s.d. 2026-04-24** | **≥$46.66** | |
