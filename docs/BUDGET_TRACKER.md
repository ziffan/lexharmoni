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
| R1 (est.) | ~409,540 | 0 | ~1,500 | ~15,000 | ~$2.43 |

Notes:
- Opus pricing: $5/MTok input, $25/MTok output (vs Sonnet $3/$15)
- cache_stats.log not written — path issue after uvicorn reload; see ST2 results
- Est. cache write: 409,540 × $5/MTok = $2.05 + output 15K × $25/MTok = $0.38

---

## Running Total

| Test | Cost |
|---|---|
| Smoke Test 1 (Sonnet) | ~$1.80 |
| Smoke Test 2 (Opus) | ~$2.43 |
| **Total spent** | **~$4.23** |
| **Remaining budget** | **~$5.77** |
