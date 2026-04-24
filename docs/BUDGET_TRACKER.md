# LexHarmoni — Budget Tracker

**Session start:** 2026-04-23
**Source:** `claude_api_cost_2026_04_01_to_2026_04_24.csv` (actual) + Claude Code invoice

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

## Running Total — Aktual

| Item | Biaya |
|---|---|
| API — Sonnet 4.6 (all calls) | $4.38 |
| API — Opus 4.7 (all calls) | $9.78 |
| **Total API aktual** | **$14.16** |
| Claude Code (sesi 2026-04-23) | $11.11 |
| **Grand Total 2026-04-23** | **$25.27** |
