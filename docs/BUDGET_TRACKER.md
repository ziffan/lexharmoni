# LexHarmoni — Budget Tracker

**Session start:** 2026-04-23
**Total budget cap:** $10.00

---

## Smoke Test 1 — Sonnet 4.6 (2026-04-23)

| Call | cache_creation | cache_read | input | output | Est. cost |
|---|---|---|---|---|---|
| R1 (warm-up, multiple failed) | ~409,540 | 0 | ~1,314 | ~10,000 | ~$1.24 |
| R1 (confirmed) | 0 | 409,540 | 1,314 | 10,458 | ~$0.28 |
| R2 (confirmed) | 1,311 | 409,540 | 3 | 9,980 | ~$0.28 |
| **ST1 Total** | | | | | **~$1.80** |

Notes:
- First confirmed R1 had corpus already cached from warm-up calls
- Cache savings: ~90% on corpus tokens ($0.12 vs ~$1.23 uncached per call)

---

## Smoke Test 2 — Opus 4.7 (2026-04-23)

| Call | cache_creation | cache_read | input | output | Est. cost |
|---|---|---|---|---|---|
| R1 (cache write, est.) | ~409,540 | 0 | ~1,500 | ~15,000 | ~$2.43 |
| R2 (cache warm, est.) | ~0 | ~409,540 | ~1,500 | ~15,000 | ~$0.58 |
| R3 (cache warm, est.) | ~0 | ~409,540 | ~1,500 | ~15,000 | ~$0.58 |
| **ST2 Total** | | | | | **~$3.59** |

Notes:
- Opus pricing: $5/MTok input, $25/MTok output
- Cache read rate: $0.50/MTok (90% saving vs uncached)
- cache_stats.log not written during runs — path fix applied post-run; see ST2 results

---

## Running Total

| Test | Cost |
|---|---|
| Smoke Test 1 (Sonnet) | ~$1.80 |
| Smoke Test 2 (Opus, 3 runs) | ~$3.59 |
| **Total spent** | **~$5.39** |
| **Remaining budget** | **~$4.61** |
