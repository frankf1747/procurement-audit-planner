"""Harness tests with a scripted model: no API key and no network needed.

The scripted model plays each agent from a queue of canned responses
(text and tool calls), so these tests exercise the real harness: the
sandboxed tools, workspaces, team messaging, the gates, the deterministic
verifiers and the web API.
"""
import json
import shutil
import time
from types import SimpleNamespace as NS

import pytest

from harness import pipeline, workspace
from harness.config import ROOT, RUNS_DIR
from harness.team import Team
from harness.tools import Toolbox, ToolError, ALL_TOOLS

_n = 0


def tool(name, **inp):
    global _n
    _n += 1
    return NS(type="tool_use", id=f"tu_{_n}", name=name, input=inp)


def text(t):
    return NS(type="text", text=t)


def resp(*blocks):
    stop = "tool_use" if any(b.type == "tool_use" for b in blocks) else "end_turn"
    return NS(content=list(blocks), stop_reason=stop)


class ScriptedLLM:
    """Plays each agent from its own queue; an agent with nothing queued ends its turn."""

    def __init__(self, scripts):
        self.scripts = {k: list(v) for k, v in scripts.items()}
        self.calls = []

    def create(self, system, tools, messages):
        who = next((k for k in self.scripts if f"agent-memory/{k}/" in system), "?")
        self.calls.append((who, messages[-1]["content"]))
        q = self.scripts.get(who) or []
        return q.pop(0) if q else resp(text(f"{who}: nothing more to do"))


@pytest.fixture
def ws_team():
    run_id = f"test-{time.time_ns()}"
    ws = workspace.create(run_id, "team")
    yield ws
    shutil.rmtree(ws, ignore_errors=True)


# ---------------------------------------------------------------- tools
def test_tools_enforce_the_sandbox(ws_team):
    box = Toolbox(ws_team, ALL_TOOLS)
    assert "\t# CLAUDE.md" in box.execute("read_file", {"path": "CLAUDE.md", "limit": 3})
    for bad in ({"path": "data/contracts.csv", "content": "x"}, {"path": ".claude/skills/x.md", "content": "x"},
                {"path": "scripts/checks/run_checks.py", "content": "x"}, {"path": "../escape.txt", "content": "x"}):
        with pytest.raises(ToolError):
            box.execute("write_file", bad)
    assert "wrote outputs/note.txt" in box.execute("write_file", {"path": "outputs/note.txt", "content": "hi"})
    with pytest.raises(ToolError):
        box.execute("run", {"command": "ls outputs | wc -l"})
    with pytest.raises(ToolError):
        box.execute("run", {"command": "curl https://example.com"})
    out = box.execute("run", {"command": ".venv/bin/python -c \"print(6*7)\""})
    assert "exit code 0" in out and "42" in out
    with pytest.raises(ToolError):
        box.execute("read_file", {"path": "outputs/note.txt", "limit": "ten"})   # schema check on tool input
    restricted = Toolbox(ws_team, ["read_file"])
    with pytest.raises(ToolError):
        restricted.execute("write_file", {"path": "outputs/x", "content": "x"})


def test_workspace_is_a_copy(ws_team):
    assert (ws_team / "outputs" / "risk-register.md").exists()          # earlier stages copied in
    assert not (ws_team / "outputs" / "audit-plan.json").exists()       # the team's own outputs are not
    (ws_team / "outputs" / "rules.json").write_text("{}")
    assert json.loads((ROOT / "outputs" / "rules.json").read_text())["rules"]   # the repo is untouched


# ---------------------------------------------------------------- team
def test_team_messages_flow_between_peers(ws_team):
    llm = ScriptedLLM({
        "planner": [
            resp(tool("send_message", to="challenger", message="PACK READY v1"),
                 tool("send_message", to="qa-reviewer", message="PACK READY v1")),
            resp(text("waiting")),
            resp(tool("send_message", to="challenger", message="RESPONSE #1: accepted"),
                 tool("send_message", to="lead", message="PLANNER DONE v2")),
            resp(text("done")),
        ],
        "challenger": [
            resp(tool("send_message", to="planner", message="CHALLENGE #1 [sample] R-01: ask")),
            resp(text("waiting")),
            resp(tool("send_message", to="lead", message="CHALLENGER DONE: 1 resolved")),
            resp(text("done")),
        ],
        "qa-reviewer": [
            resp(tool("send_message", to="planner", message="QA v1: PASS")),
            resp(text("waiting for done")),
            resp(tool("send_message", to="lead", message="QA DONE: READY FOR SIGN-OFF")),
            resp(text("done")),
        ],
    })
    events = []
    result = Team(ws_team, llm, lambda *a: events.append(a), "gate closed").run()
    assert result["complete"], result
    assert set(result["done"]) == {"planner", "challenger", "qa-reviewer"}
    delivered = [c for w, c in llm.calls if isinstance(c, str) and c.startswith(("Messages", "You have"))]
    assert any("from planner: PACK READY v1" in c for c in delivered)
    assert any("from challenger: CHALLENGE #1" in c for c in delivered)
    qa_inputs = [c for w, c in llm.calls if w == "qa-reviewer" and isinstance(c, str)]
    assert any("planner reported: PLANNER DONE" in c for c in qa_inputs)      # lead tells QA the others are done


def test_unknown_recipient_is_an_error(ws_team):
    llm = ScriptedLLM({"planner": [resp(tool("send_message", to="auditor", message="hi")), resp(text("ok"))]})
    t = Team(ws_team, llm, lambda *a: None, "gate closed")
    t.agents["planner"].turn("start")
    results = [c for w, c in llm.calls if w == "planner" and isinstance(c, list)]
    assert results and results[0][0]["is_error"] is False and "unknown recipient" in results[0][0]["content"]


# ---------------------------------------------------------------- pipeline: gate 1 -> team -> QA -> gate 2
def wait_for(run, cond, timeout=180):
    end = time.time() + timeout
    while time.time() < end:
        st = run.load()
        if cond(st):
            return st
        time.sleep(0.3)
    raise AssertionError(f"timed out; state {run.load()}")


def test_full_gate_and_team_flow():
    run = pipeline.Run.create("team")
    try:
        # reopen gate 1: blank the decisions that were recorded at step 5.1, keep the revision-1 ones
        comments = run.ws / "outputs" / "auditor-comments.md"
        lines = []
        for line in comments.read_text().splitlines():
            if "Approved as rated at step 5.1" in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                line = f"| {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} |  |  |"
            lines.append(line)
        comments.write_text("\n".join(lines) + "\n")
        # the copied pack stands in for the team's work (the scripted planner only announces it)
        for name in ("audit-plan.json", "planning-memo.md", "risk-control-matrix.md", "audit-program.md",
                     "samples", "pack-figures.json", "challenges.md", "review.md"):
            src = ROOT / "outputs" / name
            (shutil.copytree if src.is_dir() else shutil.copy2)(src, run.ws / "outputs" / name)
        run.update(stage="gate1", status="waiting", stages={"gate1": "waiting", "team": "pending", "gate2": "pending"})

        open_ids = [r["id"] for r in run.gate_rows()["rows"] if not r["decision"]]
        assert len(open_ids) == 8
        with pytest.raises(ValueError):    # every open risk needs a decision
            run.submit_decisions(ScriptedLLM({}), "Tester", {})
        with pytest.raises(ValueError):    # amend needs a comment
            run.submit_decisions(ScriptedLLM({}), "Tester", {i: {"decision": "amend"} for i in open_ids})

        llm = ScriptedLLM({
            "risk-assessor": [resp(text("decisions already applied; register rebuilt"))],
            "planner": [resp(tool("send_message", to="challenger", message="PACK READY v1"),
                             tool("send_message", to="qa-reviewer", message="PACK READY v1"),
                             tool("send_message", to="lead", message="PLANNER DONE v1"))],
            "challenger": [resp(tool("send_message", to="lead", message="CHALLENGER DONE: 0 open"))],
            "qa-reviewer": [resp(tool("run", command=".venv/bin/python scripts/checks/run_checks.py")),
                            resp(text("checks pass")),
                            resp(tool("send_message", to="lead", message="QA DONE: READY FOR SIGN-OFF"))],
        })
        run.submit_decisions(llm, "Tester", {i: {"decision": "approve", "comment": ""} for i in open_ids})
        st = wait_for(run, lambda s: s["status"] in ("failed", "done") or (s["stage"] == "gate2" and s["status"] == "waiting"))
        assert st["status"] == "waiting" and st["stage"] == "gate2", st
        assert st["verify"]["gate check"]["ok"] and st["verify"]["QA checks"]["ok"]
        text_ = comments.read_text()
        assert "Reviewer: Tester" in text_ and text_.count("| approve |") >= 9

        with pytest.raises(ValueError):
            run.submit_signoff("", "sign off", "")
        run.submit_signoff("Tester", "sign off", "ok")
        assert run.load()["status"] == "done"
        assert "Signed off by: Tester" in (run.ws / "outputs" / "review.md").read_text()
        kinds = [json.loads(l)["kind"] for l in run.events_path.read_text().splitlines()]
        assert "message" in kinds and "verify" in kinds and "gate" in kinds
    finally:
        shutil.rmtree(run.ws, ignore_errors=True)


# ---------------------------------------------------------------- web API
def test_api_demo_and_files():
    from fastapi.testclient import TestClient
    from harness.app import app
    c = TestClient(app)
    h = c.get("/api/health").json()
    assert [s["id"] for s in h["stages"]] == workspace.STAGES
    runs = c.get("/api/runs").json()
    assert runs[0]["id"] == "demo" and runs[0]["status"] == "done"
    demo = c.get("/api/runs/demo").json()
    assert any(f["path"] == "risk-register.md" for f in demo["files"])
    f = c.get("/api/runs/demo/file", params={"path": "review.md"}).json()
    assert "READY FOR SIGN-OFF" in f["content"]
    assert c.get("/api/runs/demo/file", params={"path": "../CLAUDE.md"}).status_code == 404
    assert c.post("/api/runs/demo/signoff", json={"name": "x", "decision": "sign off"}).status_code == 400
    assert c.get("/").status_code == 200


def test_backend_selection(monkeypatch):
    from harness import app as appmod
    from harness.agent import Agent, make_agent
    from harness.sdk_backend import ClaudeCodeLLM, SdkAgent
    monkeypatch.setenv("HARNESS_BACKEND", "claude-code")
    assert appmod.backend() == "claude-code" and isinstance(appmod.llm(), ClaudeCodeLLM)
    monkeypatch.setenv("HARNESS_BACKEND", "api")
    assert appmod.backend() == "api"
    box = Toolbox(ROOT, ["read_file"])
    assert isinstance(make_agent("x", "sys", box, ClaudeCodeLLM(), lambda *a: None), SdkAgent)
    assert isinstance(make_agent("x", "sys", box, ScriptedLLM({}), lambda *a: None), Agent)
