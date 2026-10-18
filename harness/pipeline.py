"""The six-stage pipeline, its deterministic checks and the two human gates.

Stage             Who (from the repo)                       Then the harness runs
rules             /extract-rules skill                      verify_quotes.py
analysts          spend-analyst + findings-analyst (parallel) selfcheck.py, verify_history.py
risks             risk-assessor (+ risk-assessment skill)   build_register.py
gate1             the auditor, in the web form              risk-assessor revision, build_pack.py --gate
team              planner, challenger, qa-reviewer          run_checks.py
gate2             the auditor signs review.md               -

State lives in runs/<id>/run.json and every event in runs/<id>/events.jsonl,
so the UI can reconnect and a restart of the server does not lose a run.
"""
import datetime
import json
import re
import subprocess
import threading
import time
import uuid
from pathlib import Path

from . import workspace
from .agent import AgentStopped, make_agent
from .config import PYTHON, RUNS_DIR
from .prompts import agent_prompt, parse_agent, skill_prompt
from .team import Team
from .tools import ALL_TOOLS, Toolbox, tools_for

STAGE_LABELS = {
    "rules": "1. Extract rules (skill)", "analysts": "2. Spend + history analysts (sub-agents)",
    "risks": "3. Risk register (sub-agent + skill)", "gate1": "4. Auditor gate: approve the risks",
    "team": "5. Planning pack (agent team)", "gate2": "6. Auditor sign-off",
}
_active_lock = threading.Lock()
_active = {"run": None}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


class Run:
    def __init__(self, run_id: str):
        self.id = run_id
        self.ws = RUNS_DIR / run_id
        self.state_path = self.ws / "run.json"
        self.events_path = self.ws / "events.jsonl"
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- state
    @classmethod
    def create(cls, start_stage: str = "rules") -> "Run":
        run_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        ws = workspace.create(run_id, start_stage)
        run = cls(run_id)
        stages = {s: ("skipped" if workspace.STAGES.index(s) < workspace.STAGES.index(start_stage) else "pending")
                  for s in workspace.STAGES}
        run.save({"id": run_id, "created": now(), "start_stage": start_stage, "status": "created",
                  "stage": start_stage, "stages": stages, "message": "", "verify": {}})
        run.emit("lead", "stage", f"workspace created at runs/{run_id}; starting at {STAGE_LABELS[start_stage]}")
        return run

    def load(self) -> dict:
        return json.loads(self.state_path.read_text())

    def save(self, state: dict) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2))
        tmp.replace(self.state_path)

    def update(self, **kw) -> dict:
        with self._lock:
            st = self.load()
            stages = kw.pop("stages", None)
            st.update(kw)
            if stages:
                st["stages"].update(stages)
            self.save(st)
            return st

    def emit(self, agent: str, kind: str, text: str) -> None:
        with self._lock:
            with self.events_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"t": now(), "agent": agent, "kind": kind, "text": text}) + "\n")

    # ---------------------------------------------------------------- helpers
    def check(self, label: str, argv: list) -> tuple:
        """Run a deterministic verifier in the workspace and record its result."""
        p = subprocess.run([str(PYTHON)] + argv, cwd=self.ws, capture_output=True, text=True, timeout=900)
        out = (p.stdout + p.stderr).strip()
        tail = "\n".join(out.splitlines()[-12:])
        self.emit("lead", "verify", f"{label}: exit {p.returncode}\n{tail}")
        st = self.load()
        st["verify"][label] = {"ok": p.returncode == 0, "tail": tail}
        self.save(st)
        return p.returncode == 0, out

    def agent(self, llm, name: str):
        spec = parse_agent(self.ws / ".claude" / "agents" / f"{name}.md")
        box = Toolbox(self.ws, tools_for(spec["tools"]))
        system, _ = agent_prompt(self.ws, name, box.names)
        return make_agent(name, system, box, llm, self.emit)

    def _stage(self, stage, fn):
        self.update(stage=stage, status="running", stages={stage: "running"}, message="")
        self.emit("lead", "stage", f"start {STAGE_LABELS[stage]}")
        ok = fn()
        self.update(stages={stage: "done" if ok else "failed"})
        if not ok:
            raise StageFailed(f"{STAGE_LABELS[stage]} did not pass its checks")

    # ---------------------------------------------------------------- stages
    def run_rules(self, llm):
        box = Toolbox(self.ws, ALL_TOOLS)
        a = make_agent("extract-rules", skill_prompt(self.ws, "extract-rules", box.names), box, llm, self.emit)
        a.turn("/extract-rules")
        ok, _ = self.check("extract-rules verifier",
                           [".claude/skills/extract-rules/verify_quotes.py", "outputs/rules.json", "data/contract-rules.pdf"])
        return ok

    def run_analysts(self, llm):
        errors = []

        def go(name):
            try:
                self.agent(llm, name).turn(f"Run the {name}.")
            except Exception as e:
                errors.append(f"{name}: {e}")
                self.emit(name, "error", str(e))
        threads = [threading.Thread(target=go, args=(n,)) for n in ("spend-analyst", "findings-analyst")]
        for t in threads: t.start()
        for t in threads: t.join()
        ok1, _ = self.check("spend self-check", ["scripts/selfcheck.py"])
        ok2, _ = self.check("history verifier", ["scripts/verify_history.py", "outputs/history.json", "data/committee"])
        return not errors and ok1 and ok2

    def run_risks(self, llm):
        self.agent(llm, "risk-assessor").turn("Run the risk-assessor.")
        ok, _ = self.check("register builder", [".claude/skills/risk-assessment/build_register.py"])
        return ok

    def run_revision(self, llm):
        self.agent(llm, "risk-assessor").turn(
            "Run the risk-assessor again. The auditor has recorded a decision for every risk in "
            "outputs/auditor-comments.md. Apply the decisions and mark the register as a revision.")
        ok, _ = self.check("register builder", [".claude/skills/risk-assessment/build_register.py"])
        gate_ok, gate_out = self.check("gate check", [".claude/skills/audit-program/build_pack.py", "--gate"])
        return ok and gate_ok, gate_out

    def run_team(self, llm, gate_output):
        result = Team(self.ws, llm, self.emit, gate_output).run()
        self.emit("lead", "info", "team finished: " + json.dumps({k: v for k, v in result.items() if k != "done"})
                  + "\n" + "\n".join(f"{k}: {v}" for k, v in result["done"].items()))
        ok, _ = self.check("QA checks", ["scripts/checks/run_checks.py"])
        return ok and result["complete"]

    # ---------------------------------------------------------------- drivers
    def start(self, llm):
        st = self.load()
        order = workspace.STAGES[workspace.STAGES.index(st["start_stage"]):]
        self._spawn(llm, order)

    def _spawn(self, llm, order, **kw):
        if not _active_lock.acquire(blocking=False):
            raise RuntimeError("another live run is in progress; wait for it to reach a gate or finish")
        _active["run"] = self.id
        threading.Thread(target=self._drive, args=(llm, order), kwargs=kw, daemon=True).start()

    def _drive(self, llm, order, gate_output=None):
        try:
            for stage in order:
                if stage == "revision":      # after gate 1: apply the decisions, then re-check the gate
                    self.update(stage="gate1", status="running", message="applying the auditor's decisions")
                    self.emit("lead", "stage", "start applying the auditor's decisions (risk-assessor revision)")
                    ok, gate_output = self.run_revision(llm)
                    if not ok:
                        self.update(stage="gate1", status="waiting", stages={"gate1": "waiting"},
                                    message="The revision or the gate check failed; see the activity log.")
                        self.emit("lead", "error", "revision or gate check failed; the gate is open again")
                        return
                    self.update(stages={"gate1": "done"})
                    continue
                if stage == "gate1":
                    self.update(stage="gate1", status="waiting", stages={"gate1": "waiting"},
                                message="Record a decision for every risk.")
                    self.emit("lead", "gate", "waiting for the auditor's decisions on the risk register")
                    return
                if stage == "gate2":
                    self.update(stage="gate2", status="waiting", stages={"gate2": "waiting"},
                                message="Review the QA verdict and sign off.")
                    self.emit("lead", "gate", "waiting for the auditor's sign-off in review.md")
                    return
                if stage == "team" and gate_output is None:
                    ok, gate_output = self.check("gate check", [".claude/skills/audit-program/build_pack.py", "--gate"])
                    if not ok:
                        raise StageFailed("the auditor gate is not closed")
                fn = {"rules": lambda: self.run_rules(llm), "analysts": lambda: self.run_analysts(llm),
                      "risks": lambda: self.run_risks(llm), "team": lambda: self.run_team(llm, gate_output)}[stage]
                self._stage(stage, fn)
            self.update(status="done")
        except (StageFailed, AgentStopped) as e:
            self.update(status="failed", message=str(e))
            self.emit("lead", "error", str(e))
        except Exception as e:  # surface anything unexpected in the UI
            self.update(status="failed", message=f"{type(e).__name__}: {e}")
            self.emit("lead", "error", f"{type(e).__name__}: {e}")
        finally:
            _active["run"] = None
            _active_lock.release()

    # ---------------------------------------------------------------- gates
    def gate_rows(self) -> dict:
        """The decision template rows and reviewer/date, for the gate form."""
        path = self.ws / "outputs" / "auditor-comments.md"
        rows = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                c = [x.strip() for x in line.strip().strip("|").split("|")]
                if len(c) >= 6 and re.fullmatch(r"R-\d+", c[0]):
                    rows.append({"id": c[0], "title": c[1], "now": c[2], "scope": c[3],
                                 "decision": c[4], "comment": "|".join(c[5:]).strip()})
        return {"rows": rows}

    def submit_decisions(self, llm, reviewer: str, decisions: dict):
        st = self.load()
        if st["status"] != "waiting" or st["stage"] != "gate1":
            raise ValueError("this run is not waiting at the risk gate")
        if _active_lock.locked():
            raise RuntimeError("another live run is in progress; try again when it reaches a gate")
        rows = self.gate_rows()["rows"]
        open_ids = [r["id"] for r in rows if not r["decision"]]
        for rid in open_ids:
            d = decisions.get(rid) or {}
            if d.get("decision") not in ("approve", "amend", "reject"):
                raise ValueError(f"{rid}: choose approve, amend or reject")
            if d["decision"] in ("amend", "reject") and not d.get("comment", "").strip():
                raise ValueError(f"{rid}: {d['decision']} needs a comment saying what to change or why")
        if not reviewer.strip():
            raise ValueError("reviewer name is required")
        path = self.ws / "outputs" / "auditor-comments.md"
        out = []
        for line in path.read_text(encoding="utf-8").splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if line.startswith("Reviewer:"):
                line = f"Reviewer: {reviewer.strip()}"
            elif line.startswith("Date:"):
                line = f"Date: {datetime.date.today()}"
            elif len(c) >= 6 and c[0] in open_ids:
                d = decisions[c[0]]
                comment = " ".join(d.get("comment", "").replace("|", "/").split()) or "Approved as rated."
                line = f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {d['decision']} | {comment} |"
            out.append(line)
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        self.emit("auditor", "gate", f"{reviewer} recorded {len(open_ids)} decisions: "
                  + ", ".join(f"{k} {decisions[k]['decision']}" for k in open_ids))
        self._spawn(llm, ["revision", "team", "gate2"])

    def submit_signoff(self, name: str, decision: str, comment: str):
        st = self.load()
        if st["status"] != "waiting" or st["stage"] != "gate2":
            raise ValueError("this run is not waiting for sign-off")
        if decision not in ("sign off", "return to the team") or not name.strip():
            raise ValueError("name and a decision (sign off / return to the team) are required")
        path = self.ws / "outputs" / "review.md"
        text = path.read_text(encoding="utf-8")
        block = (f"Signed off by: {name.strip()}\nDate: {datetime.date.today()}\n"
                 f"Decision (sign off / return to the team): {decision}\nComment: {' '.join(comment.split())}")
        new, n = re.subn(r"Signed off by:.*?\nDate:.*?\nDecision \(sign off / return to the team\):.*?\nComment:.*?(\n|$)",
                         block + "\n", text, flags=re.S)
        if n == 0:
            new = text.rstrip() + "\n\n## Auditor sign-off\n\n" + block + "\n"
        path.write_text(new, encoding="utf-8")
        self.emit("auditor", "gate", f"{name}: {decision}")
        self.update(stages={"gate2": "done"}, status="done", stage="gate2", message=f"{decision} by {name}")


class StageFailed(Exception):
    pass

