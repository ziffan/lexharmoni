'use client';

import { useState, useRef, useEffect, useCallback } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type AppStatus = 'idle' | 'loading_preset' | 'analyzing' | 'complete' | 'error';

interface AffectedRegulation {
  regulation_id: string;
  article_or_section: string;
  quoted_text: string;
  role: string;
}

interface TemporalWindow {
  friction_active_from: string | null;
  friction_active_until: string | null;
  duration_months: number | null;
}

interface Finding {
  id: string;
  type: string;
  severity: 'critical' | 'major' | 'minor';
  title: string;
  summary: string;
  affected_regulations: AffectedRegulation[];
  reasoning_steps: string[];
  temporal_window: TemporalWindow;
  recommended_resolution: string;
  confidence: string;
}

interface FindingsData {
  draft_id: string;
  analysis_timestamp: string;
  findings: Finding[];
  summary_stats: {
    total_findings: number;
    by_severity: { critical: number; major: number; minor: number };
    by_type: { normative: number; hierarchical: number; operational: number };
  };
}

function severityBadge(severity: string) {
  if (severity === 'critical') return 'bg-red-900 text-red-200 border border-red-700';
  if (severity === 'major') return 'bg-orange-900 text-orange-200 border border-orange-700';
  return 'bg-yellow-900 text-yellow-200 border border-yellow-700';
}

function severityOrder(s: string) {
  return s === 'critical' ? 0 : s === 'major' ? 1 : 2;
}

function FindingCard({ finding }: { finding: Finding }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-800 overflow-hidden">
      <button
        onClick={() => setExpanded(v => !v)}
        className="w-full text-left px-4 py-3 flex items-start gap-3 hover:bg-slate-750 transition-colors"
      >
        <span className={`mt-0.5 shrink-0 px-2 py-0.5 rounded text-xs font-bold uppercase ${severityBadge(finding.severity)}`}>
          {finding.severity}
        </span>
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-slate-100 text-sm leading-snug">{finding.title}</h3>
          <p className="text-slate-400 text-xs mt-0.5">{finding.type} · {finding.id}</p>
        </div>
        <span className="text-slate-500 text-xs shrink-0 mt-0.5">{expanded ? '▲' : '▼'}</span>
      </button>

      {expanded && (
        <div className="px-4 pb-4 border-t border-slate-700 space-y-4 pt-3">
          <p className="text-slate-300 text-sm">{finding.summary}</p>

          {finding.reasoning_steps.length > 0 && (
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase tracking-wide mb-1">Reasoning</p>
              <ol className="list-decimal list-inside space-y-1">
                {finding.reasoning_steps.map((step, i) => (
                  <li key={i} className="text-slate-300 text-xs">{step}</li>
                ))}
              </ol>
            </div>
          )}

          {finding.affected_regulations.length > 0 && (
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase tracking-wide mb-1">Affected Regulations</p>
              <div className="space-y-2">
                {finding.affected_regulations.map((reg, i) => (
                  <div key={i} className="bg-slate-900 rounded p-2 text-xs">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-mono font-bold text-indigo-400">{reg.regulation_id}</span>
                      <span className="text-slate-400">{reg.article_or_section}</span>
                      <span className="ml-auto text-slate-500 uppercase text-xs">{reg.role}</span>
                    </div>
                    {reg.quoted_text && (
                      <blockquote className="border-l-2 border-indigo-700 pl-2 text-slate-400 italic leading-relaxed">
                        {reg.quoted_text}
                      </blockquote>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {(finding.temporal_window.friction_active_from || finding.temporal_window.friction_active_until) && (
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase tracking-wide mb-1">Temporal Window</p>
              <p className="text-slate-300 text-xs">
                {finding.temporal_window.friction_active_from ?? '?'} →{' '}
                {finding.temporal_window.friction_active_until ?? 'ongoing'}
                {finding.temporal_window.duration_months != null && ` (${finding.temporal_window.duration_months} months)`}
              </p>
            </div>
          )}

          {finding.recommended_resolution && (
            <div>
              <p className="text-slate-500 text-xs font-semibold uppercase tracking-wide mb-1">Resolution</p>
              <p className="text-slate-300 text-xs">{finding.recommended_resolution}</p>
            </div>
          )}

          <p className="text-slate-500 text-xs">Confidence: <span className="text-slate-400">{finding.confidence}</span></p>
        </div>
      )}
    </div>
  );
}

function FindingsList({ data }: { data: FindingsData | null }) {
  if (!data) return null;

  const sorted = [...data.findings].sort(
    (a, b) => severityOrder(a.severity) - severityOrder(b.severity)
  );

  const { by_severity } = data.summary_stats;

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center gap-4 text-xs pb-2 border-b border-slate-700">
        <span className="text-slate-400 font-semibold">{data.findings.length} findings</span>
        {by_severity.critical > 0 && (
          <span className="text-red-400">{by_severity.critical} critical</span>
        )}
        {by_severity.major > 0 && (
          <span className="text-orange-400">{by_severity.major} major</span>
        )}
        {by_severity.minor > 0 && (
          <span className="text-yellow-400">{by_severity.minor} minor</span>
        )}
      </div>
      <div className="space-y-2">
        {sorted.map(f => <FindingCard key={f.id} finding={f} />)}
      </div>
    </div>
  );
}

function ReasoningStream({ text, isStreaming }: { text: string; isStreaming: boolean }) {
  const boxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = boxRef.current.scrollHeight;
    }
  }, [text]);

  if (!text && !isStreaming) return null;

  return (
    <div className="mt-3">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-slate-400 text-xs font-semibold uppercase tracking-wide">Opus 4.7 Reasoning</span>
        {isStreaming && (
          <span className="px-2 py-0.5 rounded-full bg-indigo-900 text-indigo-300 text-xs font-medium animate-pulse">
            streaming…
          </span>
        )}
      </div>
      <div
        ref={boxRef}
        className="h-64 overflow-y-auto rounded-lg border border-slate-700 bg-slate-900 p-3 font-mono text-xs text-slate-300 leading-relaxed"
      >
        <span>{text}</span>
        {isStreaming && (
          <span className="inline-block w-1.5 h-3 bg-indigo-400 ml-0.5 animate-pulse align-middle" />
        )}
      </div>
    </div>
  );
}

function StatusBar({ status, findingsCount }: { status: AppStatus; findingsCount: number }) {
  const label: Record<AppStatus, string> = {
    idle: 'Idle',
    loading_preset: 'Loading corpus…',
    analyzing: 'Analyzing (streaming)…',
    complete: `Complete — ${findingsCount} finding${findingsCount !== 1 ? 's' : ''}`,
    error: 'Error',
  };

  const color: Record<AppStatus, string> = {
    idle: 'text-slate-500',
    loading_preset: 'text-indigo-400',
    analyzing: 'text-emerald-400',
    complete: 'text-emerald-300',
    error: 'text-red-400',
  };

  return (
    <div className={`text-xs font-semibold uppercase tracking-widest ${color[status]}`}>
      {label[status]}
    </div>
  );
}

export default function Home() {
  const [draftId, setDraftId] = useState('');
  const [draftText, setDraftText] = useState('');
  const [model, setModel] = useState('claude-opus-4-7');
  const [reasoning, setReasoning] = useState('');
  const [findings, setFindings] = useState<FindingsData | null>(null);
  const [status, setStatus] = useState<AppStatus>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const loadPreset = useCallback(async () => {
    setStatus('loading_preset');
    setErrorMsg('');
    try {
      const res = await fetch(`${API_URL}/corpus/preset/pojk-40-2024`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setDraftId(data.draft_id);
      setDraftText(data.draft_text);
      setStatus('idle');
    } catch (e) {
      setErrorMsg(`Failed to load preset: ${e instanceof Error ? e.message : String(e)}`);
      setStatus('error');
    }
  }, []);

  const handleFileUpload = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      setDraftText(ev.target?.result as string ?? '');
      setDraftId(file.name.replace('.txt', ''));
    };
    reader.readAsText(file);
  }, []);

  const analyze = useCallback(async () => {
    if (!draftText.trim()) return;
    setStatus('analyzing');
    setReasoning('');
    setFindings(null);
    setErrorMsg('');

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft_id: draftId || 'draft', draft_text: draftText, model }),
      });

      if (!res.ok) {
        const detail = await res.text();
        throw new Error(`HTTP ${res.status}: ${detail}`);
      }

      if (!res.body) throw new Error('No response body');

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let currentEvent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (currentEvent === 'reasoning') {
              setReasoning(prev => prev + data);
            } else if (currentEvent === 'findings') {
              try {
                setFindings(JSON.parse(data));
              } catch {
                setErrorMsg('Failed to parse findings JSON');
              }
            } else if (currentEvent === 'error') {
              setErrorMsg(data);
              setStatus('error');
            } else if (currentEvent === 'done') {
              setStatus('complete');
            }
          }
        }
      }

      setStatus(prev => prev === 'analyzing' ? 'complete' : prev);
    } catch (e) {
      setErrorMsg(`Analysis failed: ${e instanceof Error ? e.message : String(e)}`);
      setStatus('error');
    }
  }, [draftId, draftText, model]);

  const findingsCount = findings?.summary_stats.total_findings ?? 0;
  const isStreaming = status === 'analyzing';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-800 px-6 py-4">
        <h1 className="text-2xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-emerald-400">
          LexHarmoni
        </h1>
        <p className="text-slate-400 text-sm mt-0.5">AI-Powered Regulatory Stress-Testing</p>
      </header>

      {/* Main layout */}
      <main className="flex flex-1 overflow-hidden">
        {/* Left column — 40% */}
        <div className="w-2/5 border-r border-slate-800 flex flex-col p-5 gap-4 overflow-y-auto">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500">Draft Under Test</h2>

          <div className="flex flex-col gap-2">
            <button
              onClick={loadPreset}
              disabled={status === 'loading_preset' || status === 'analyzing'}
              className="w-full px-3 py-2 rounded-lg bg-indigo-700 hover:bg-indigo-600 disabled:opacity-50 text-sm font-medium transition-colors text-white"
            >
              Load POJK 40/2024 (Demo)
            </button>

            <label className="w-full px-3 py-2 rounded-lg border border-slate-700 hover:border-slate-500 text-sm text-slate-400 text-center cursor-pointer transition-colors">
              Upload .txt file
              <input
                type="file"
                accept=".txt"
                className="hidden"
                onChange={handleFileUpload}
                disabled={status === 'analyzing'}
              />
            </label>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-500 shrink-0">Model:</label>
            <select
              value={model}
              onChange={e => setModel(e.target.value)}
              disabled={status === 'analyzing'}
              className="flex-1 bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200 disabled:opacity-50"
            >
              <option value="claude-opus-4-7">Opus 4.7</option>
              <option value="claude-sonnet-4-6">Sonnet 4.6</option>
            </select>
          </div>

          <button
            onClick={analyze}
            disabled={!draftText.trim() || status === 'analyzing' || status === 'loading_preset'}
            className="w-full px-3 py-2.5 rounded-lg bg-emerald-700 hover:bg-emerald-600 disabled:opacity-50 text-sm font-semibold transition-colors text-white"
          >
            {status === 'analyzing' ? 'Analyzing…' : `Analyze with ${model === 'claude-opus-4-7' ? 'Opus 4.7' : 'Sonnet 4.6'}`}
          </button>

          {draftId && (
            <p className="text-xs text-slate-500 font-mono truncate">ID: {draftId}</p>
          )}

          <textarea
            readOnly
            value={draftText}
            placeholder="No draft loaded. Click 'Load POJK 40/2024' or upload a .txt file."
            className="flex-1 min-h-64 font-mono text-xs bg-slate-900 border border-slate-800 rounded-lg p-3 text-slate-300 resize-none placeholder:text-slate-600"
          />
        </div>

        {/* Right column — 60% */}
        <div className="w-3/5 flex flex-col p-5 overflow-y-auto">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500">Friction Analysis</h2>
            <StatusBar status={status} findingsCount={findingsCount} />
          </div>

          {errorMsg && (
            <div className="mb-3 px-3 py-2 rounded-lg bg-red-950 border border-red-800 text-red-300 text-xs">
              {errorMsg}
            </div>
          )}

          <ReasoningStream text={reasoning} isStreaming={isStreaming} />
          <FindingsList data={findings} />

          {status === 'idle' && !reasoning && (
            <div className="flex-1 flex items-center justify-center text-slate-700 text-sm">
              Load a draft and click Analyze to begin.
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
