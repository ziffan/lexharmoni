# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

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
                log_path = Path(__file__).parent / "cache_stats.log"
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
