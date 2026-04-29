# Copyright 2026 Ziffany Firdinal
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

"""One-shot severity lock validation — calls /analyze via SSE, parses findings."""
import json
import sys
import time
import urllib.request

BASE_URL = "http://localhost:8000"

# Step A: load preset
print("[1/3] Loading POJK-40-2024 preset...", flush=True)
with urllib.request.urlopen(f"{BASE_URL}/corpus/preset/pojk-40-2024") as r:
    preset = json.loads(r.read())
draft_id = preset["draft_id"]
draft_text = preset["draft_text"]
print(f"      draft_id={draft_id}, text_length={len(draft_text)} chars", flush=True)

# Step B: POST /analyze with SSE
print("[2/3] Streaming /analyze (Opus 4.7) — this takes 2-4 min...", flush=True)
payload = json.dumps({
    "draft_id": draft_id,
    "draft_text": draft_text,
    "model": "claude-opus-4-7"
}).encode()

req = urllib.request.Request(
    f"{BASE_URL}/analyze",
    data=payload,
    headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
    method="POST"
)

findings_data = None
error_data = None
reasoning_chars = 0
t0 = time.time()

with urllib.request.urlopen(req, timeout=600) as resp:
    current_event = None
    for raw_line in resp:
        line = raw_line.decode("utf-8").rstrip("\n").rstrip("\r")
        if line.startswith("event:"):
            current_event = line[6:].strip()
        elif line.startswith("data:"):
            data_str = line[5:].strip()
            if current_event == "reasoning":
                reasoning_chars += len(data_str)
                # print a dot every ~500 chars so user sees progress
                if reasoning_chars % 2000 < len(data_str):
                    print(".", end="", flush=True)
            elif current_event == "findings":
                findings_data = json.loads(data_str)
            elif current_event == "error":
                error_data = data_str
            elif current_event == "done":
                break

elapsed = time.time() - t0
print(f"\n      elapsed={elapsed:.1f}s  reasoning_chars={reasoning_chars}", flush=True)

if error_data:
    print(f"\n[ERROR] SSE returned error: {error_data}", file=sys.stderr)
    sys.exit(1)

if not findings_data:
    print("\n[ERROR] No findings received", file=sys.stderr)
    sys.exit(1)

# Step C: report
print("\n[3/3] Findings Report", flush=True)
print("=" * 70)

findings = findings_data.get("findings", [])
stats = findings_data.get("summary_stats", {})
by_sev = stats.get("by_severity", {})
by_type = stats.get("by_type", {})

print(f"\nTotal findings : {stats.get('total_findings', len(findings))}")
print(f"By severity    : critical={by_sev.get('critical',0)}  major={by_sev.get('major',0)}  minor={by_sev.get('minor',0)}")
print(f"By type        : normative={by_type.get('normative',0)}  hierarchical={by_type.get('hierarchical',0)}  operational={by_type.get('operational',0)}")

print("\n--- Findings Table ---")
print(f"{'ID':<6} {'Type':<14} {'Severity':<10} Title")
print("-" * 70)

ANCHOR_KEYWORDS = {
    "collection hours": ("normative", "critical"),
    "jam penagihan":    ("normative", "critical"),
    "saving clause":    ("normative", "critical"),
    "bab xi":           ("hierarchical", "major"),
    "bab penagihan":    ("hierarchical", "major"),
    "cantolan":         ("hierarchical", "major"),
    "orphaned":         ("hierarchical", "major"),
    "terminologi":      ("operational", "minor"),
    "terminology":      ("operational", "minor"),
    "multiguna":        ("operational", "minor"),
    "konsumtif":        ("operational", "minor"),
}

SEVERITY_LOCK = {"normative": "critical", "hierarchical": "major", "operational": "minor"}

lock_pass = []
lock_fail = []

for f in findings:
    fid      = f.get("id", "?")
    ftype    = f.get("type", "?")
    fsev     = f.get("severity", "?")
    ftitle   = f.get("title", "")[:55]
    expected = SEVERITY_LOCK.get(ftype)
    ok = "PASS" if fsev == expected else "FAIL"
    print(f"{fid:<6} {ftype:<14} {fsev:<10} {ftitle}  [{ok}]")
    if fsev == expected:
        lock_pass.append(fid)
    else:
        lock_fail.append(f"{fid}(expected {expected}, got {fsev})")

# anchor detection
print("\n--- Anchor Finding Check ---")
title_blob = " ".join(f.get("title","").lower() + f.get("summary","").lower() for f in findings)
anchors = {
    "Collection Hours Conflict": any(k in title_blob for k in ["jam penagihan","collection hour","saving clause"]),
    "Bab XI / Orphaned Cantolan":any(k in title_blob for k in ["bab xi","bab penagihan","cantolan","orphaned","delegasi"]),
    "Terminology Drift":         any(k in title_blob for k in ["terminologi","terminology","multiguna","konsumtif"]),
}
for name, found in anchors.items():
    print(f"  [{'FOUND' if found else 'MISSING'}] {name}")

print("\n--- Severity Lock Verdict ---")
if lock_fail:
    print(f"  [FAIL] mismatches: {', '.join(lock_fail)}")
else:
    print(f"  [PASS] all {len(lock_pass)} findings have correct severity")

print("\n--- Raw JSON (findings array) ---")
print(json.dumps(findings_data, ensure_ascii=False, indent=2))
