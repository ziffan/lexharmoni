# LexHarmoni Demo Recording Session — 2026-04-24

## Summary
- Total runs: 4 (1 warm-up, 3 Opus recorded)
- Usable takes: 3 (B1, B2, B3)
- Selected take for video: TBD (review B1–B3 di CapCut)

## Session Timeline
- Cache warm-up complete: ~18:35 WIB
- Cache valid window: 18:35–19:35 WIB (1h TTL)
- Recording session end: ~18:46 WIB
- Buffer remaining: ~49 menit

## Opus Runs Detail
| Run | Filename | Duration | Cache Status | Output Tokens | Notes |
|---|---|---|---|---|---|
| Warm-up | — (unrecorded) | ~2:05 | WRITE 554K | 10,779 | Phase 2 cache warm-up |
| B1 | demo_opus_run_[timestamp].mp4 | ~2:05 | HIT 554K | 9,414 | |
| B2 | demo_opus_run_[timestamp].mp4 | ~2:05 | HIT 554K | 11,084 | |
| B3 | demo_opus_run_[timestamp].mp4 | ~2:05 | HIT 554K | 9,482 | |

*Update filename kolom dengan nama file OBS aktual.*

## Cache Stats (from cache_stats.log)
- Warm-up `cache_creation`: 554,518 tokens (corpus full write)
- B1 `cache_read`: 554,518 tokens ✅
- B2 `cache_read`: 554,518 tokens ✅
- B3 `cache_read`: 554,518 tokens ✅
- User message auto-cache (5min): 186,542 tokens per run (normal, Anthropic auto-behavior)

## Cost Actual (dari CSV update_demo)
Delta dari CSV sebelumnya = **+$11.82**

| Item | Token count | Aktual cost |
|---|---|---|
| Warm-up corpus cache_write_1h | 554,518 | $5.54 |
| Warm-up input_no_cache | 186,548 | $0.93 |
| Warm-up output | 10,779 | $0.27 |
| B1–B3 cache_read × 3 | 1,663,554 | $0.83 |
| B1–B3 cache_write_5m × 3 | ~559,626 | $3.50 |
| B1–B3 output × 3 | ~29,980 | $0.75 |
| **Recording session total** | | **$11.82** |

## Notes for Editing
- Take selection: review B1–B3, pilih yang paling smooth stream + best findings set
- B2 memiliki output token tertinggi (11,084) — kemungkinan reasoning paling detail
- Semua 3 takes confirmed cache HIT — tidak ada run dengan corpus re-write delay
- Mock run (File 1) untuk intro/demo segment: ~35 detik, instant results

## Known Issues
- (isi setelah review footage)
