# LexHarmoni — Installation & Run Manual

## System Requirements

- **OS:** Windows 10+, macOS 12+, or Linux (tested: Ubuntu 22.04)
- **Python:** 3.11 or newer
- **Node.js:** 20 LTS or newer (npm 10+)
- **Git:** any recent version
- **Anthropic API key:** required for analysis (set as env var)
- **Disk space:** ~500MB (mostly node_modules)
- **Network:** outbound HTTPS to `api.anthropic.com`

---

## One-Time Setup

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/lexharmoni.git
cd lexharmoni
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
```

Activate virtual environment:
- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Windows (cmd):** `.\venv\Scripts\activate.bat`
- **macOS / Linux:** `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

Set API key:
```bash
cp .env.example .env
```

Edit `.env` in a text editor and set:
```
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

Return to repo root:
```bash
cd ..
```

### 3. Frontend setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
```

Default `.env.local` should work as-is for local dev.

Return to repo root:
```bash
cd ..
```

---

## Running LexHarmoni

You need **two terminals open simultaneously.**

### Terminal 1: Backend

```bash
cd backend
# Activate venv (see above)
uvicorn main:app --reload
```

Wait for output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal running.

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Wait for:
```
- Local:   http://localhost:3000
```

Leave this terminal running.

### Open browser

Navigate to: `http://localhost:3000`

---

## Using LexHarmoni

### Quick demo (POJK 40/2024 retrospective)

1. Click **"Load POJK 40/2024 (Demo)"**. The draft text appears in the left
   panel.
2. Ensure model dropdown shows **"Opus 4.7"** (or switch to Sonnet 4.6 for
   a cheaper smoke test).
3. Click **"Analyze"**.
4. Watch the reasoning stream fill the right panel (takes 30-90 seconds
   depending on model).
5. When streaming completes, findings cards appear below.
6. Click each card to expand and see detailed reasoning, quoted articles,
   and recommended resolutions.

### Analyzing your own draft

1. Prepare draft as a UTF-8 `.txt` file.
2. Click **"Upload .txt file"** in the left panel.
3. Continue as above from step 2.

### Cost awareness

Each analysis:
- **Opus 4.7:** ~$5-15 per run with corpus caching (first run ~$10-15 due to
  cache write; subsequent runs within 5 minutes ~$1-3).
- **Sonnet 4.6:** ~$0.50-2 per run (recommended for development/debugging).

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
Verify `backend/.env` exists and contains your key. Restart the backend
terminal after editing.

### Frontend shows "Failed to fetch"
Backend is not running, or port 8000 is blocked. Check Terminal 1.

### "Module not found" errors in backend
Virtual environment not activated. Activate it before running uvicorn.

### Analysis takes too long / times out
- First run warms the cache (slower).
- If >3 minutes with Opus, check your network and Anthropic status.
- Try switching to Sonnet to isolate whether it's a model or plumbing issue.

### Reasoning stream stops mid-way
Refresh the page. Known issue with long-running SSE connections on some
networks. Non-streaming fallback planned for v2.

---

## Project Structure

```
lexharmoni/
├── backend/          FastAPI server (Python)
├── frontend/         Next.js app (TypeScript/React)
├── corpus/           7 OJK regulations (READ-ONLY after MT-1.3)
│   ├── active/       3 regulations currently in force
│   ├── historical/   4 regulations revoked/superseded
│   └── manifest.json Structured metadata
├── ground-truth/     Manual expert analysis (evaluation baseline)
├── prompts/          Versioned prompts for friction detection
├── scripts/          Utility scripts (manifest validator)
├── docs/             Architecture, decisions, this manual
└── README.md
```

---

## Next Steps

- To understand the architecture: `docs/ARCHITECTURE.md`
- To see how the prompt works: `prompts/friction-detection-v1.md`
- To compare against human analysis: `ground-truth/manual-analysis.md`
```

---
