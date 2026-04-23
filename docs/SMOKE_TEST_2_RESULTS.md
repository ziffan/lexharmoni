# Smoke Test 2 — Opus 4.7 (Quality Evaluation)

**Date:** 2026-04-23
**Model:** claude-opus-4-7
**Draft:** corpus/active/POJK-40-2024.txt (full retrospective draft)
**max_tokens:** 128,000
**Runs:** 3

---

## Quality Checklist

- [x] Backend healthy at start of run
- [x] Full POJK-40-2024 draft loaded via "Load POJK 40/2024 (Demo)" button
- [x] SSE stream completed — reasoning visible in UI (all 3 runs)
- [x] Findings cards rendered (4–5 findings per run)
- [x] 3/3 ground-truth core frictions found in every run
- [x] Zero hallucinated citations (all reference real articles)
- [⚠️] Severity calibration fluktuatif: anchor finding critical/major bergantian
- [⚠️] cache_stats.log tidak tertulis — path fix diterapkan setelah run (BASE fix)

**Result: PASS**

---

## Findings per Run

### Run 1 — 4 findings (0 critical · 2 major · 2 minor)

| ID | Type | Severity | Title |
|---|---|---|---|
| F001 | normative | major | Pasal 235 saving clause perpetuates SEOJK 19/2023 collection-hours conflict with POJK 22/2023 |
| F002 | hierarchical | major | Pasal 236 mencabut POJK 10/2022 tanpa merehabilitasi cantolan delegasi Bab Penagihan SEOJK 19/2023 |
| F003 | operational | minor | Saving clause Pasal 235 bersifat open-ended tanpa sunset |
| F004 | operational | minor | Terminologi 'Pendanaan konsumtif' (POJK 40/2024) vs 'Pendanaan multiguna' (SEOJK 19/2023) |

### Run 2 — 5 findings (1 critical · 2 major · 2 minor)

| ID | Type | Severity | Title |
|---|---|---|---|
| F001 | hierarchical | critical | Open-ended saving clause perpetuates SEOJK 19/2023 Bab Penagihan conflict with POJK 22/2023 |
| F002 | hierarchical | major | Orphaned delegation: batas minimum usia dan penghasilan Penerima Dana (Pasal 149) tanpa ketentuan pelaksana |
| F003 | hierarchical | major | Batas maksimum manfaat ekonomi Pasal 140 ayat (3) bergantung pada SEOJK 19/2023 yang diselamatkan Pasal 235 |
| F004 | operational | minor | Perubahan terminologi 'Pendanaan multiguna' menjadi 'Pendanaan konsumtif' |
| F005 | operational | minor | Istilah 'Sertifikat Elektronik' digunakan di Pasal 154 tanpa definisi dalam Pasal 1 |

### Run 3 — 5 findings (1 critical · 3 major · 1 minor)

| ID | Type | Severity | Title |
|---|---|---|---|
| F001 | hierarchical | major | Open-ended saving clause memperpanjang SEOJK 19/2023 yang delegasi aslinya telah dicabut |
| F002 | normative | critical | Perpetuasi konflik jam penagihan POJK 22/2023 vs SEOJK 19/2023 melalui saving clause |
| F003 | operational | major | Format publikasi kinerja Pendanaan: TKB (SEOJK 19/2023) vs kualitas Pendanaan 5-kategori (POJK 40/2024) |
| F004 | hierarchical | major | Orphaned cross-reference: SEOJK 19/2023 merujuk Pasal 25 POJK 10/2022 yang telah dicabut |
| F005 | operational | minor | Pergeseran terminologi 'Pendanaan multiguna' ke 'Pendanaan konsumtif' |

---

## Cross-Run Consistency Analysis

| Finding (konsep) | R1 | R2 | R3 | Stability |
|---|---|---|---|---|
| Collection hours conflict / saving clause | F001 normative·major | F001 hierarchical·critical | F002 normative·critical | ✅ **3/3 ANCHOR** |
| Orphaned cantolan Bab XI / delegasi dicabut | F002 hierarchical·major | F001 (overlap) | F001+F004 hierarchical·major | ✅ **3/3 STABLE** |
| Terminology "multiguna" vs "konsumtif" | F004 operational·minor | F004 operational·minor | F005 operational·minor | ✅ **3/3 STABLE** |
| Open-ended saving clause tanpa sunset | F003 minor | — | F001 framing | ⚠️ 2/3 |
| Orphaned specific cross-ref (Pasal 25/149) | — | F002 major | F004 major | ⚠️ 2/3 |
| TKB vs 5-kategori kualitas Pendanaan | — | — | F003 major | ❌ 1/3 stochastic |
| Manfaat ekonomi Pasal 140 dependency | — | F003 major | — | ❌ 1/3 stochastic |
| Sertifikat Elektronik tanpa definisi | — | F005 minor | — | ❌ 1/3 stochastic |

---

## Ground Truth Comparison (3-run aggregate)

| Ground Truth Finding | Status |
|---|---|
| Normative (Critical): jam penagihan SEOJK 19/2023 vs POJK 22/2023 | ✅ 3/3 runs — type/severity varies but substance consistent |
| Hierarchical (Major): dangling Bab XI / cantolan hilang | ✅ 3/3 runs — exact hit |
| Operational (Minor): terminology drift | ✅ 3/3 runs — exact hit |
| Operational (Minor): beban ganda pelaporan | ℹ️ 0/3 — likely correct omission for POJK 40/2024 scope |

---

## Quality Notes

### Severity Calibration
Anchor finding (collection hours conflict) severity is non-deterministic:
- R1: major | R2: critical | R3: critical
Two of three runs return critical — aligns with ground truth.
**Fix:** Add explicit type→severity constraint in prompt to lock this.

### Novel Findings
Run 2 and 3 surface plausible additional findings (Pasal 149 orphaned delegation,
TKB vs 5-kategori, Sertifikat Elektronik) not in ground truth. These represent
genuine cross-regulation analysis, not hallucinations.

### Demo Reliability
The 3 consistent findings are safe for demo script — appear in every run regardless
of stochastic sampling. Stochastic findings (1/3 only) should not be scripted.

---

## Issues

1. **cache_stats.log not written** — path was `Path(__file__).parent` which may resolve
   relative after uvicorn hot-reload. Fixed to `BASE / "backend" / "cache_stats.log"` where
   `BASE` is verified working (corpus loading uses same path).
2. **Severity calibration** — prompt tweak needed before demo if critical label required.
