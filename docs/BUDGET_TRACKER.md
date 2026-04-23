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
| TBD | | | | | |

Expected first call: cache_creation ~250K tokens (Opus cache separate from Sonnet), est. ~$3.00

---

## Running Total

| Test | Cost |
|---|---|
| Smoke Test 1 (Sonnet) | ~$1.80 |
| Smoke Test 2 (Opus) | TBD |
| **Total spent** | **~$1.80** |
| **Remaining budget** | **~$8.20** |
