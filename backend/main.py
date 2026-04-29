# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

import asyncio
import json
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from prompt_loader import build_user_message, load_system_blocks, parse_findings

load_dotenv()

app = FastAPI(title="LexHarmoni API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = Path(__file__).parent.parent


class HealthResponse(BaseModel):
    status: str
    service: str


class AnalyzeRequest(BaseModel):
    draft_id: str
    draft_text: str
    model: str = "claude-opus-4-7"


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok", "service": "lexharmoni-backend"}


@app.get("/corpus/manifest")
async def get_manifest():
    manifest_path = BASE / "corpus" / "manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Manifest file not found")
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading manifest: {str(e)}")


@app.get("/corpus/preset/pojk-40-2024")
async def get_preset_pojk():
    path = BASE / "corpus" / "active" / "POJK-40-2024.txt"
    if not path.exists():
        raise HTTPException(status_code=404, detail="POJK-40-2024.txt not found")
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return {"draft_id": "POJK-40-2024", "draft_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")


_MOCK_CHUNKS = [
    "<reasoning>\n",
    "## Analisis Regulasi: POJK-40-2024 (MOCK)\n\n",
    "Memulai analisis persilangan regulasi antara POJK 40/2024 sebagai draft uji ",
    "dengan korpus regulasi aktif: POJK 22/2023, SEOJK 19/2023, POJK 10/2022.\n\n",
    "### 1. Pemeriksaan Konflik Jam Penagihan\n\n",
    "POJK 22/2023 Pasal 62 ayat (2) huruf f menetapkan jam penagihan ",
    "08.00-20.00 WIB untuk hari kerja dan 08.00-17.00 WIB untuk Sabtu.\n",
    "SEOJK 19/2023 Bab XI angka 5 mengatur hari penagihan Senin-Sabtu ",
    "dengan ketentuan jam yang berbeda dari POJK 22/2023.\n\n",
    "POJK 40/2024 Pasal 235 memuat saving clause open-ended yang memperpanjang ",
    "berlakunya SEOJK 19/2023 tanpa batas waktu dan tanpa resolusi konflik.\n",
    "Dua norma setingkat dengan isi berbeda berlaku bersamaan.\n\n",
    "**Kualifikasi:** normative conflict. **Severity:** critical.\n\n",
    "### 2. Pemeriksaan Orphaned Delegation\n\n",
    "POJK 10/2022 mendelegasikan pengaturan teknis penagihan ke SEOJK 19/2023. ",
    "POJK 40/2024 Pasal 236 mencabut POJK 10/2022 sepenuhnya. ",
    "Namun SEOJK 19/2023 masih dipertahankan via saving clause Pasal 235.\n",
    "Delegation chain menjadi orphaned: parent dicabut, child masih berlaku.\n\n",
    "**Kualifikasi:** hierarchical conflict. **Severity:** major.\n\n",
    "### 3. Pemeriksaan Terminology Drift\n\n",
    "SEOJK 19/2023 menggunakan istilah 'Pendanaan multiguna'. ",
    "POJK 40/2024 menggunakan 'Pendanaan konsumtif' untuk kategori yang sama. ",
    "Tidak ada pasal bridging yang menyamakan kedua istilah.\n\n",
    "**Kualifikasi:** operational. **Severity:** minor.\n\n",
    "### Ringkasan\n\n",
    "Ditemukan 3 friction. Semua konsisten dengan ground truth. ",
    "Severity lock rules diterapkan: normative->critical, hierarchical->major, operational->minor.\n",
    "</reasoning>\n",
]

_MOCK_FINDINGS = {
    "findings": [
        {
            "id": "F001",
            "type": "normative",
            "severity": "critical",
            "title": "[MOCK] Konflik jam penagihan via saving clause Pasal 235",
            "summary": "POJK 22/2023 dan SEOJK 19/2023 memiliki ketentuan jam penagihan berbeda. Pasal 235 POJK 40/2024 memperpanjang SEOJK 19/2023 tanpa resolusi konflik.",
            "affected_regulations": [
                {
                    "regulation_id": "POJK-22-2023",
                    "article_or_section": "Pasal 62 ayat (2) huruf f",
                    "quoted_text": "08.00-20.00 WIB",
                    "role": "conflicting_norm",
                },
                {
                    "regulation_id": "SEOJK-19-2023",
                    "article_or_section": "Bab XI angka 5",
                    "quoted_text": "hari penagihan Senin-Sabtu",
                    "role": "conflicting_norm",
                },
            ],
            "reasoning_steps": [
                "Identifikasi dua norma berlaku bersamaan",
                "Verifikasi tidak ada hierarki eksplisit",
                "Klasifikasi sebagai normative conflict",
            ],
            "temporal_window": {
                "friction_active_from": "2024-01-01",
                "friction_active_until": None,
                "duration_months": None,
            },
            "recommended_resolution": "Tambahkan sunset clause pada Pasal 235 atau harmonisasi eksplisit ketentuan jam penagihan.",
            "confidence": 0.95,
        },
        {
            "id": "F002",
            "type": "hierarchical",
            "severity": "major",
            "title": "[MOCK] Orphaned delegation: SEOJK 19/2023 kehilangan cantolan parent",
            "summary": "Pasal 236 POJK 40/2024 mencabut POJK 10/2022 selaku parent delegasi SEOJK 19/2023, sementara SEOJK 19/2023 masih dipertahankan via saving clause.",
            "affected_regulations": [
                {
                    "regulation_id": "POJK-10-2022",
                    "article_or_section": "Pasal 25",
                    "quoted_text": "delegasi ke SEOJK",
                    "role": "revoked_parent",
                },
                {
                    "regulation_id": "SEOJK-19-2023",
                    "article_or_section": "Bab XI",
                    "quoted_text": "Bab Penagihan",
                    "role": "orphaned_child",
                },
            ],
            "reasoning_steps": [
                "Trace delegation chain",
                "Verifikasi pencabutan parent",
                "Konfirmasi anak masih berlaku",
            ],
            "temporal_window": {
                "friction_active_from": "2024-01-01",
                "friction_active_until": None,
                "duration_months": None,
            },
            "recommended_resolution": "Cantumkan dasar delegasi baru di POJK 40/2024 yang menggantikan POJK 10/2022.",
            "confidence": 0.92,
        },
        {
            "id": "F003",
            "type": "operational",
            "severity": "minor",
            "title": "[MOCK] Terminology drift: 'multiguna' vs 'konsumtif'",
            "summary": "SEOJK 19/2023 menggunakan 'Pendanaan multiguna', POJK 40/2024 menggunakan 'Pendanaan konsumtif' untuk kategori yang sama tanpa pasal bridging.",
            "affected_regulations": [
                {
                    "regulation_id": "SEOJK-19-2023",
                    "article_or_section": "Bab I",
                    "quoted_text": "Pendanaan multiguna",
                    "role": "source_term",
                },
                {
                    "regulation_id": "POJK-40-2024",
                    "article_or_section": "Pasal 1 angka 5",
                    "quoted_text": "Pendanaan konsumtif",
                    "role": "target_term",
                },
            ],
            "reasoning_steps": [
                "Temukan penggunaan istilah",
                "Verifikasi tidak ada pasal ekuivalensi",
                "Klasifikasi sebagai terminologi drift",
            ],
            "temporal_window": {
                "friction_active_from": "2024-01-01",
                "friction_active_until": None,
                "duration_months": None,
            },
            "recommended_resolution": "Tambahkan pasal definisi yang menyamakan kedua istilah.",
            "confidence": 0.85,
        },
    ],
    "summary_stats": {
        "total_findings": 3,
        "by_severity": {"critical": 1, "major": 1, "minor": 1},
        "by_type": {"normative": 1, "hierarchical": 1, "operational": 1},
    },
}


@app.post("/analyze/mock")
async def analyze_mock(req: AnalyzeRequest):
    """Mock SSE endpoint — streams pre-canned text with delays, no API call."""

    async def mock_stream():
        for chunk in _MOCK_CHUNKS:
            yield {"event": "reasoning", "data": chunk}
            await asyncio.sleep(0.15)
        yield {"event": "findings", "data": json.dumps(_MOCK_FINDINGS)}
        yield {"event": "done", "data": "complete"}

    return EventSourceResponse(mock_stream())


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")

    async def event_stream():
        full_text = ""
        try:
            system_blocks = load_system_blocks()
            user_message = build_user_message(req.draft_id, req.draft_text)

            client = anthropic.Anthropic(api_key=api_key)

            with client.messages.stream(
                model=req.model,
                max_tokens=128000,
                system=system_blocks,
                messages=[{"role": "user", "content": user_message}],
                extra_headers={"anthropic-beta": "extended-cache-ttl-2025-04-11"},
            ) as stream:
                for text_chunk in stream.text_stream:
                    full_text += text_chunk
                    yield {"event": "reasoning", "data": text_chunk}

                final = stream.get_final_message()
                u = final.usage
                cache_log = (
                    f"[CACHE] model={req.model} "
                    f"cache_creation={getattr(u, 'cache_creation_input_tokens', 'n/a')} "
                    f"cache_read={getattr(u, 'cache_read_input_tokens', 'n/a')} "
                    f"input={u.input_tokens} output={u.output_tokens}"
                )
                print(cache_log, file=sys.stderr, flush=True)
                print(cache_log, flush=True)
                log_path = BASE / "backend" / "cache_stats.log"
                with open(log_path, "a", encoding="utf-8") as lf:
                    lf.write(cache_log + "\n")

        except anthropic.APIError as e:
            msg = f"API error: {type(e).__name__}"
            print(f"[ERROR] {msg}: {e}", file=sys.stderr)
            yield {"event": "error", "data": msg}
            return
        except Exception as e:
            msg = f"Unexpected error: {type(e).__name__}"
            print(f"[ERROR] {msg}: {e}", file=sys.stderr)
            yield {"event": "error", "data": msg}
            return

        try:
            findings = parse_findings(full_text)
            yield {"event": "findings", "data": json.dumps(findings)}
        except ValueError as e:
            err_str = str(e)
            if err_str == "findings_not_found":
                print("[ERROR] <findings> block not found in response", file=sys.stderr)
                yield {"event": "error", "data": "malformed response"}
            else:
                print(f"[ERROR] findings JSON parse error: {e}", file=sys.stderr)
                yield {"event": "error", "data": "findings JSON malformed"}
            return
        except json.JSONDecodeError as e:
            print(f"[ERROR] findings JSON malformed: {e}", file=sys.stderr)
            yield {"event": "error", "data": "findings JSON malformed"}
            return

        yield {"event": "done", "data": "complete"}

    return EventSourceResponse(event_stream())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
