```markdown
# Integration Specification — Backend & Frontend Wire-Up

**Audience:** Claude Code (Sonnet) as executing agent
**Prerequisite:** MT-3.1 (FastAPI skeleton) and MT-4.1 (Next.js skeleton) done.
**Output target:** Working end-to-end flow, demo-able, pre-smoke-test.

---

## MT-3.2 — Backend: Claude Integration Endpoint

### Target file: `backend/main.py` (edit existing)

### New endpoint: `POST /analyze`

Replace current 501 stub with full implementation.

**Request schema:**
```python
class AnalyzeRequest(BaseModel):
    draft_id: str
    draft_text: str  # full text of regulation draft under test
    model: str = "claude-opus-4-7"  # or "claude-sonnet-4-6" for smoke test
```

**Response:** Server-Sent Events stream. Event types:
- `event: reasoning` → data: chunk of reasoning text
- `event: findings` → data: parsed JSON object (sent once at end)
- `event: error` → data: error message
- `event: done` → data: completion signal

**Behavior:**
1. Load `corpus/manifest.json`.
2. Load all 7 regulation files from `corpus/active/` and `corpus/historical/`.
3. Load prompt template from `prompts/friction-detection-v1.md`.
4. Assemble `system` array with 4 cached blocks (role+framework, manifest,
   active corpus, historical corpus). Each block gets:
   `"cache_control": {"type": "ephemeral"}`.
5. Call Anthropic API via `anthropic` Python SDK with `stream=True`.
6. Yield reasoning tokens as they arrive.
7. After stream done, extract text between `<findings>` and `</findings>`,
   parse as JSON, yield as `findings` event.
8. Yield `done` event.

**Environment:**
- Read `ANTHROPIC_API_KEY` from environment variable (NOT hardcoded).
- Create `backend/.env.example` documenting required env vars.
- Add `.env` to `.gitignore` if not already.

**Error handling:**
- API error → yield `error` event with sanitized message (no API key in logs).
- `<findings>` block not found → yield `error` event "malformed response".
- JSON parse error → yield `error` event "findings JSON malformed".
- All errors also log to stderr for debugging.

**New dependency:**
Add to `backend/requirements.txt`:
```
anthropic>=0.39.0
python-dotenv>=1.0.0
sse-starlette>=2.0.0
```

### New endpoint: `GET /corpus/preset/pojk-40-2024`

Returns the full text of `corpus/active/POJK-40-2024.txt` as JSON:
```json
{"draft_id": "POJK-40-2024", "draft_text": "..."}
```

Used by frontend to load the retrospective demo draft.

### New file: `backend/prompt_loader.py`

Helper module:
- `load_system_blocks() -> list[dict]` — reads prompt markdown + corpus files,
  returns properly structured `system` array with `cache_control`.
- `parse_findings(text: str) -> dict` — extracts JSON from `<findings>` tags.

Keep `main.py` thin. Business logic in `prompt_loader.py`.

---

## MT-4.2 — Frontend: Demo UI

### Target files: `frontend/app/page.tsx`, plus new components

### Layout (single page, no routing)

```
┌─────────────────────────────────────────────────┐
│ Header: LexHarmoni                              │
│ Subtitle: AI-Powered Regulatory Stress-Testing  │
├─────────────────────────────────────────────────┤
│ Left column (40%)      Right column (60%)       │
│ ────────────────────   ──────────────────────── │
│ DRAFT UNDER TEST       FRICTION ANALYSIS        │
│ [Load POJK 40/2024]                             │
│ [Upload .txt file]     [Reasoning stream box]   │
│ [Analyze button]       [Findings cards below]   │
│                                                 │
│ Draft preview (ro)     ...                      │
└─────────────────────────────────────────────────┘
```

### Required components (single-file or split — your choice)

1. **`DraftPanel`** (left column)
   - Button: "Load POJK 40/2024 (Demo)" → fetches
     `GET /corpus/preset/pojk-40-2024`, stores in state.
   - File upload input: accepts `.txt`, reads file, stores in state.
   - Read-only textarea showing loaded draft (monospace, scrollable).
   - "Analyze with Opus 4.7" button → triggers POST to `/analyze`.
   - Model toggle (small dropdown): Opus 4.7 / Sonnet 4.6 (for smoke testing).

2. **`ReasoningStream`** (right column, top)
   - Box that receives streamed tokens from `/analyze`.
   - Monospace font, auto-scroll to bottom.
   - Subtle animation: blinking cursor while streaming.
   - Label: "Opus 4.7 Reasoning" with a small badge showing "streaming..."
     when active.

3. **`FindingsList`** (right column, below stream)
   - Populated when `findings` event arrives.
   - Each finding = collapsible card:
     - Title (h3)
     - Severity badge (critical=red, major=orange, minor=yellow)
     - Type label
     - Summary (plain text)
     - Expand to see: reasoning_steps, affected_regulations (with quotes),
       temporal_window, recommended_resolution.
   - Sort: critical → major → minor.

4. **`StatusBar`** (top of right column)
   - Shows: "Idle" / "Loading corpus..." / "Analyzing (streaming)..." /
     "Complete — N findings".

### State management
Use Next.js client component with `useState`. No Redux, no Zustand. Single
page app.

### SSE client
Use native `fetch` with `ReadableStream` reader. Parse SSE manually (no
dedicated library — SSE is trivial). If complexity bites, `eventsource`
package is acceptable fallback.

### API base URL
Read from `NEXT_PUBLIC_API_URL`. Default `http://localhost:8000`.
Create `frontend/.env.local.example` documenting this.

### Styling constraint
Tailwind only. NO new dependencies (no shadcn, no component lib). Simple,
clean, demo-ready. Use a neutral palette (slate/zinc) with one accent
(indigo or emerald for "active" states).

### NO features to add
- No authentication.
- No persistence (no localStorage — will break in some environments).
- No multi-session. Each analyze = fresh.
- No export/download of findings (Day 3 if needed).
- No dark mode toggle.

---

## Verification checklist (for Claude Code)

After implementation, run end-to-end:

1. `cd backend && uvicorn main:app --reload`
2. `cd frontend && npm run dev`
3. Open `http://localhost:3000`.
4. Click "Load POJK 40/2024 (Demo)".
5. Verify textarea populates.
6. Select model: Sonnet 4.6 (cheap smoke test).
7. Click "Analyze".
8. Verify reasoning streams into right column.
9. Verify findings cards render after stream.
10. Check browser network tab: should see SSE connection to
    `/analyze`, with multiple `event: reasoning` messages and one
    `event: findings`.

Paste curl equivalent to confirm backend works standalone:
```bash
curl -N -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"draft_id":"test","draft_text":"...","model":"claude-sonnet-4-6"}'
```

## Stop conditions

- If SSE streaming fails → fall back to non-stream in v1, note as issue.
- If caching doesn't reduce cost (check response headers
  `x-cache-creation-input-tokens` vs `x-cache-read-input-tokens`) → debug
  before proceeding to Opus run.
- If corpus exceeds context window → STOP, report size, we'll decide whether
  to compress historical corpus.

## Budget for this MT

- Smoke test 1 (Sonnet, end-to-end plumbing): 1× call, est. $0.30-0.80.
- Do NOT run Opus during MT-3.2/MT-4.2 work. Opus run = separate planned
  session.
```

---