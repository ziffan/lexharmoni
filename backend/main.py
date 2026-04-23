import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any

app = FastAPI(title="LexHarmoni API", version="0.1.0")

# CORS middleware for Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    service: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok", "service": "lexharmoni-backend"}

@app.get("/corpus/manifest")
async def get_manifest():
    manifest_path = Path(__file__).parent.parent / "corpus" / "manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Manifest file not found")
    
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading manifest: {str(e)}")

@app.post("/analyze")
async def analyze():
    raise HTTPException(status_code=501, detail="Not Implemented - Claude integration coming in Day 2")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
