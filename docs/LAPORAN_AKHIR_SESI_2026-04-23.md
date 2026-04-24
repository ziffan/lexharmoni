# Laporan Akhir Sesi — LexHarmoni
**Tanggal:** 2026-04-23
**Durasi:** ~1 hari penuh
**Total biaya:** $25.27 aktual (API $14.16 + Claude Code $11.11)

---

## Ringkasan Eksekutif

Sesi ini membangun LexHarmoni dari skeleton kosong hingga sistem yang berjalan penuh: FastAPI backend dengan SSE streaming ke Claude Opus 4.7, Next.js frontend dengan demo UI, corpus 7 regulasi OJK/LPBBTI dengan prompt caching, dan dua sesi smoke test (Sonnet plumbing + Opus quality). Semua milestone teknis tercapai. Sistem terbukti menemukan 3/3 ground-truth friction dari manual analysis di setiap run.

---

## 1. Kegiatan yang Dilakukan (Kronologis)

### MT-0 sampai MT-2: Fondasi (sebelum sesi ini)
- Folder skeleton dibuat: `backend/`, `frontend/`, `corpus/`, `docs/`, `ground-truth/`
- 7 file regulasi dikumpulkan dan diorganisasi: 3 aktif, 4 historis
- `corpus/manifest.json` dibuat dengan metadata lengkap (status, hierarki, revokes/revoked_by)
- `ground-truth/manual-analysis.md` ditulis: 3 friction utama diidentifikasi secara manual
- `tests/validate_corpus.py` dibuat untuk integrity check

### MT-3.1 & MT-4.1: Skeleton Backend + Frontend
- FastAPI skeleton dengan `/health` endpoint
- Next.js 15 (App Router) skeleton dengan landing placeholder

### MT-3.2 & MT-4.2: Integrasi Claude + Demo UI
Implementasi utama sesi ini berdasarkan `docs/INTEGRATION_SPEC_MT-3.2_MT-4.2.md`:

**Backend (`backend/main.py`, `backend/prompt_loader.py`):**
- Endpoint `POST /analyze` dengan SSE via `sse_starlette.EventSourceResponse`
- `GET /corpus/preset/pojk-40-2024` untuk load preset demo
- 4-block system array dengan `cache_control: {"type": "ephemeral"}`
- `build_user_message()` dengan instruksi output `<reasoning>` + `<findings>` JSON
- `parse_findings()` dengan regex extraction

**Frontend (`frontend/app/page.tsx`):**
- Manual SSE parsing via `fetch()` + `ReadableStream` (bukan `EventSource`)
- Reasoning panel streaming real-time (token-by-token)
- Findings cards dengan severity badge
- Model dropdown (Opus 4.7 / Sonnet 4.6)

### MT-OSS: Open Source Preparation
Agen terpisah menambahkan:
- `LICENSE` Apache 2.0
- `NOTICE`, `CONTRIBUTORS.md`
- License headers di semua `.py` files

### History Cleanup
Permintaan user untuk membersihkan referensi string sensitif dari git history:
- `git filter-branch --tree-filter` untuk menghapus string dari semua commit
- Force push ke remote
- Cleanup `refs/original/`, reflog expire, `git gc --prune=now`
- README history di-rewrite dengan konten baru

### MT-3.3: Extended Cache TTL
- `cache_control` diubah: tambah `"ttl": "1h"` di semua 4 system blocks
- `extra_headers: {"anthropic-beta": "extended-cache-ttl-2025-04-11"}` ditambah ke stream call
- Tujuan: perpanjang cache dari default ~5 menit ke 1 jam

### UI Redesign
Permintaan user untuk tema light-canvas / dark-data-panel:
- Page: `bg-slate-50`; panel: `bg-white border-slate-200 shadow-sm`
- Draft textarea + reasoning box: `bg-slate-900` (intentional dark contrast untuk readability)
- Severity badges: red/amber/slate
- Analyze button: emerald + disabled state lengkap

### Smoke Test 1 — Sonnet 4.6 (Plumbing)
- Draft: `tests/smoke_test_draft_minimal.txt` (~500 token synthetic)
- 2 confirmed runs (R1 + R2), keduanya `cache_read=409,540`
- Cache savings: ~90% ($0.12 vs $1.23 per call uncached)
- Result: **PASS** — semua plumbing checklist hijau

### Pre-ST2 Preparation
- `max_tokens` dinaikkan ke 32K (awalnya 16K) untuk prevent truncation
- Pengguna menanyakan batas Opus 4.7 → cek dokumentasi resmi → ternyata **128K**
- `max_tokens` dikoreksi ke 128K dan di-commit

### Smoke Test 2 — Opus 4.7 (Quality, 3 runs)
- Draft: `corpus/active/POJK-40-2024.txt` (full retrospective, ~360K chars)
- 3 runs dijalankan selama cache masih warm
- Hasil: 4–5 findings per run, 3/3 core frictions ditemukan konsisten

---

## 2. Kendala, Akar Masalah, dan Solusi

### K-1: `ANTHROPIC_API_KEY not configured` (HTTP 500)
**Gejala:** Frontend menampilkan HTTP 500 berulang kali setelah API key diisi.
**Akar masalah:** Backend process lama (sebelum `.env` dibuat) masih berjalan. `load_dotenv()` hanya berjalan sekali saat import — process lama tidak membaca `.env` baru.
**Percobaan gagal:** Kill parent PID uvicorn tidak mematikan worker child process yang sebenarnya serve requests.
**Solusi:** Identifikasi actual worker PIDs (bukan parent reloader), kill worker PIDs secara langsung via `Stop-Process`, restart backend fresh.

### K-2: `findings JSON malformed` (4–5 kali berturut)
**Gejala:** Frontend menampilkan "Analysis failed: findings JSON malformed" meski reasoning stream berhasil.
**Akar masalah:** Sonnet 4.6 membalut konten `<findings>` dalam markdown code fence (` ```json ... ``` `), menyebabkan `json.loads()` gagal karena karakter ` ``` ` bukan valid JSON.
**Solusi:** Tambah `re.sub()` di `parse_findings()` untuk strip fence sebelum parse:
```python
raw = re.sub(r"^```(?:json)?\s*", "", raw)
raw = re.sub(r"\s*```$", "", raw)
```

### K-3: Stale backend process (versi lama tanpa endpoint baru)
**Gejala:** Endpoint `/corpus/preset/pojk-40-2024` tidak ditemukan padahal sudah di-deploy.
**Akar masalah:** Instance uvicorn lama (sebelum MT-3.2) masih berjalan di port 8000.
**Diagnosis:** Cek via `/openapi.json` — routes yang ada hanya 3 (health + 2 corpus), bukan 4.
**Solusi:** Kill orphan process, start fresh.

### K-4: `cache_stats.log` tidak terbuat
**Gejala:** File `backend/cache_stats.log` tidak ada setelah run berhasil.
**Akar masalah:** `Path(__file__).parent` kemungkinan tidak resolve ke path absolut setelah uvicorn hot-reload via watchfiles. Exact mechanism tidak teridentifikasi (file juga tidak tertulis di lokasi lain manapun yang dicari).
**Percobaan 1:** Ubah ke `Path(os.path.abspath(__file__)).parent` — tidak membantu karena timing reload.
**Solusi akhir:** Ubah ke `BASE / "backend" / "cache_stats.log"` di mana `BASE` adalah `Path(__file__).parent.parent` yang sudah terbukti benar (digunakan untuk load corpus yang berfungsi). **Belum diverifikasi** karena tidak ada run setelah fix ini.

### K-5: `max_tokens` salah (32K padahal limit 128K)
**Gejala:** Tidak ada masalah nyata, tapi user mempertanyakan nilai 32K.
**Akar masalah:** Asumsi salah tentang limit output Opus 4.7 — diperkirakan sama dengan model lama.
**Solusi:** Cek dokumentasi resmi via agent → Opus 4.7 mendukung 128K output token. Koreksi langsung.

### K-6: Severity calibration non-konsisten
**Gejala:** F001 (collection hours conflict, tipe normative) di-return dengan severity `major` di Run 1, tapi `critical` di Run 2 dan 3.
**Akar masalah:** Prompt tidak secara eksplisit mengunci mapping tipe→severity. Model melakukan reasoning sendiri tentang severity berdasarkan konteks (apakah friction sudah "dalam proses resolusi" atau tidak).
**Status:** **Belum diperbaiki** — pending untuk sesi berikutnya. Fix: tambah kalimat eksplisit di `build_user_message()`.

### K-7: Git history cleanup kompleks
**Gejala:** Setelah `git filter-branch`, string sensitif masih ditemukan via `git grep`.
**Akar masalah:** `refs/original/` (backup otomatis filter-branch) dan `refs/stash` masih menyimpan objek lama.
**Solusi:**
```bash
git update-ref -d refs/original/refs/heads/master
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## 3. Hasil Smoke Test

### Smoke Test 1 — Sonnet 4.6 (2026-04-23)

| | R1 | R2 |
|---|---|---|
| cache_creation | 0 | 1,311 |
| cache_read | 409,540 | 409,540 |
| input | 1,314 | 3 |
| output | 10,458 | 9,980 |
| Elapsed | ~170s | ~166s |
| Est. cost | ~$0.28 | ~$0.28 |

**Result: PASS** — semua plumbing checklist hijau. Cache hit rate 100%.

### Smoke Test 2 — Opus 4.7, 3 Runs (2026-04-23)

| | R1 | R2 | R3 |
|---|---|---|---|
| Total findings | 4 | 5 | 5 |
| Critical | 0 | 1 | 1 |
| Major | 2 | 2 | 3 |
| Minor | 2 | 2 | 1 |

**Konsistensi finding (3/3 runs):**
1. Collection hours conflict (SEOJK 19/2023 vs POJK 22/2023) via saving clause Pasal 235
2. Orphaned cantolan Bab XI (delegasi dicabut oleh Pasal 236/POJK 22/2023)
3. Terminology drift "Pendanaan multiguna" vs "Pendanaan konsumtif"

**Ground truth coverage:** 3/3 core frictions ditemukan di setiap run. Zero hallucination.

**Result: PASS** (dengan catatan severity calibration pending)

---

## 4. Kondisi Akhir Sistem

| Komponen | Status |
|---|---|
| Backend FastAPI | ✅ Running, healthy |
| Frontend Next.js | ✅ Running |
| Corpus caching | ✅ Verified (409,540 tokens) |
| SSE streaming | ✅ Berfungsi end-to-end |
| Findings parsing | ✅ Robust (fence stripping) |
| cache_stats.log | ⚠️ Fix diterapkan, belum diverifikasi |
| Severity calibration | ⚠️ Pending prompt fix |

---

## 5. Commit History Sesi Ini

```
4a6ec90 [test] ST2 complete — 3-run cross-analysis + cache log path fix
c87a2e8 [test] Smoke Test 2 PASS — Opus 4.7 quality evaluation
266d2f9 [pre-ST2] Bump max_tokens to 128K (Opus 4.7 actual API limit)
ffbf745 [pre-ST2] Increase max_tokens to 32K and add budget tracker
987c27f [test] Smoke test 1 PASS — Sonnet plumbing + cache verified
9f1475a [ui] Light-canvas theme with dark data panels for demo readability
60c1721 [MT-3.3] Extend corpus cache TTL to 1 hour
0855795 Update README — full project description and demo context
1ccc99e [MT-OSS] Add Apache 2.0 license, NOTICE, contributors guide
3d99286 [MT-3.2-4.2] Backend Claude integration + frontend demo UI
```

---

## 6. Budget

| Item | Biaya |
|---|---|
| API — Sonnet 4.6 (semua calls, aktual) | $4.38 |
| API — Opus 4.7 (semua calls, aktual) | $9.78 |
| Claude Code (sesi 2026-04-23) | $11.11 |
| **Total hari ini (aktual)** | **$25.27** |

---

## 7. Pekerjaan Sesi Berikutnya

| Prioritas | Item |
|---|---|
| High | Fix severity calibration: tambah constraint di `build_user_message()` |
| High | Verifikasi `cache_stats.log` tertulis (run 1 analyze setelah server restart) |
| Medium | Demo script: pilih 3 consistent findings untuk narasi demo |
| Low | Pertimbangkan `temperature=0` untuk output deterministik |
