"""Web app: start runs, watch agents work, decide at the gates, read the outputs.

Start with `make run` (or `.venv/bin/uvicorn harness.app:app --port 8000`),
then open http://localhost:8000.
"""
import asyncio
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from . import workspace
from .config import MODEL, ROOT, RUNS_DIR, load_env
from .pipeline import STAGE_LABELS, Run, _active

load_env()
STATIC = Path(__file__).parent / "static"
DEMO = "demo"
TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt", ".py"}


def backend() -> str:
    """'api' with an API key, else 'claude-code' (Agent SDK on the local Claude Code login), else ''.
    HARNESS_BACKEND=api|claude-code forces one."""
    forced = os.environ.get("HARNESS_BACKEND", "").strip()
    if forced in ("api", "claude-code"):
        return forced
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return "api"
    from .sdk_backend import available
    return "claude-code" if available() else ""


def has_credentials() -> bool:
    return bool(backend())


def llm():
    if backend() == "claude-code":
        from .sdk_backend import ClaudeCodeLLM
        return ClaudeCodeLLM()
    from .llm import ClaudeLLM
    return ClaudeLLM()


@asynccontextmanager
async def lifespan(_app):
    """A server restart ends any agent threads; say so instead of showing them as running."""
    RUNS_DIR.mkdir(exist_ok=True)
    for p in RUNS_DIR.glob("*/run.json"):
        st = json.loads(p.read_text())
        if st.get("status") in ("running", "created"):
            st["status"], st["message"] = "failed", "interrupted by a server restart"
            p.write_text(json.dumps(st, indent=2))
    yield


app = FastAPI(title="Procurement Audit Planner harness", lifespan=lifespan)


# ---------------------------------------------------------------- helpers
def outputs_root(run_id: str) -> Path:
    if run_id == DEMO:
        return ROOT / "outputs"
    ws = RUNS_DIR / run_id
    if not (ws / "run.json").exists():
        raise HTTPException(404, "no such run")
    return ws / "outputs"


def demo_state() -> dict:
    return {"id": DEMO, "created": "Part A (Claude Code)", "start_stage": "rules", "status": "done",
            "stage": "gate2", "stages": {s: "done" for s in workspace.STAGES},
            "message": "The completed Part A run from this repository (read-only).", "verify": {}}


def file_list(root: Path) -> list:
    out = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != ".DS_Store":
            rel = p.relative_to(root).as_posix()
            group = rel.split("/")[0] if "/" in rel else ""
            out.append({"path": rel, "size": p.stat().st_size, "group": group})
    return out


# ---------------------------------------------------------------- API
@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/health")
def health():
    return {"credentials": has_credentials(), "backend": backend(), "model": MODEL, "active_run": _active["run"],
            "stages": [{"id": s, "label": STAGE_LABELS[s]} for s in workspace.STAGES]}


@app.get("/api/runs")
def runs():
    items = [demo_state()]
    for p in sorted(RUNS_DIR.glob("*/run.json"), reverse=True):
        items.append(json.loads(p.read_text()))
    return items


class NewRun(BaseModel):
    start_stage: str = "rules"


@app.post("/api/runs")
def new_run(body: NewRun):
    if not has_credentials():
        raise HTTPException(400, "No backend: set ANTHROPIC_API_KEY in .env, or install and sign in to Claude Code (the claude CLI).")
    if body.start_stage not in ("rules", "analysts", "risks", "team"):
        raise HTTPException(400, "start_stage must be rules, analysts, risks or team")
    if _active["run"]:
        raise HTTPException(409, f"run {_active['run']} is still working; wait for it to reach a gate or finish")
    run = Run.create(body.start_stage)
    try:
        run.start(llm())
    except RuntimeError as e:
        raise HTTPException(409, str(e))
    return run.load()


@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    root = outputs_root(run_id)
    if run_id == DEMO:
        st = demo_state()
    else:
        st = Run(run_id).load()
    st["files"] = file_list(root)
    if run_id != DEMO and st["stage"] == "gate1" and st["status"] == "waiting":
        st["gate"] = Run(run_id).gate_rows()
    return st


@app.get("/api/runs/{run_id}/file")
def get_file(run_id: str, path: str):
    root = outputs_root(run_id).resolve()
    f = (root / path).resolve()
    if not str(f).startswith(str(root)) or not f.is_file():
        raise HTTPException(404, "no such file")
    if f.suffix not in TEXT_SUFFIXES:
        raise HTTPException(415, "not a text file")
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    limit = 400 if f.suffix == ".csv" else 5000
    return {"path": path, "content": "\n".join(lines[:limit]), "truncated": max(0, len(lines) - limit)}


@app.get("/api/runs/{run_id}/stream")
async def stream(run_id: str):
    """Server-sent events: every event line, then the run state whenever it changes."""
    if run_id == DEMO:
        async def demo_gen():
            yield f"data: {json.dumps({'type': 'state', 'state': demo_state()})}\n\n"
        return StreamingResponse(demo_gen(), media_type="text/event-stream")
    run = Run(run_id)
    if not run.state_path.exists():
        raise HTTPException(404, "no such run")

    async def gen():
        pos, last_state = 0, None
        while True:
            if run.events_path.exists():
                with run.events_path.open(encoding="utf-8") as f:
                    f.seek(pos)
                    for line in f:
                        if line.endswith("\n"):
                            yield f"data: {json.dumps({'type': 'event', 'event': json.loads(line)})}\n\n"
                    pos = f.tell()
            st = run.state_path.read_text()
            if st != last_state:
                last_state = st
                yield f"data: {json.dumps({'type': 'state', 'state': json.loads(st)})}\n\n"
            await asyncio.sleep(0.8)
    return StreamingResponse(gen(), media_type="text/event-stream")


class Decisions(BaseModel):
    reviewer: str
    decisions: dict


@app.post("/api/runs/{run_id}/decisions")
def decisions(run_id: str, body: Decisions):
    if run_id == DEMO:
        raise HTTPException(400, "the demo run is read-only")
    if not has_credentials():
        raise HTTPException(400, "No backend: set ANTHROPIC_API_KEY in .env, or sign in to Claude Code; the risk-assessor must run to apply the decisions.")
    try:
        Run(run_id).submit_decisions(llm(), body.reviewer, body.decisions)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(400, str(e))
    return {"ok": True}


class Signoff(BaseModel):
    name: str
    decision: str
    comment: str = ""


@app.post("/api/runs/{run_id}/signoff")
def signoff(run_id: str, body: Signoff):
    if run_id == DEMO:
        raise HTTPException(400, "the demo run is read-only")
    try:
        Run(run_id).submit_signoff(body.name, body.decision, body.comment)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"ok": True}
