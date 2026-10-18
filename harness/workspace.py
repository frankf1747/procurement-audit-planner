"""Per-run workspaces: an isolated copy of the project for agents to work in.

A run never touches the repository. Its workspace holds copies of the brief,
the data, the agents, the skills, agent memory and the verifier scripts, plus
`.venv` linked to the project's environment. When a run starts part-way
(for example at the risk-assessor), the outputs of the earlier stages are
copied in from the repository's completed run so the later stages have their
inputs.
"""
import shutil
from pathlib import Path

from .config import ROOT, RUNS_DIR

STAGES = ["rules", "analysts", "risks", "gate1", "team", "gate2"]

# outputs/ entries each stage produces; copied in when a run starts after that stage
STAGE_OUTPUTS = {
    "rules": ["rules.json"],
    "analysts": ["analytics.json", "analytics-full", "history.json"],
    "risks": ["risk-ratings.json", "risk-register.md", "auditor-comments.md", "register-state.json"],
    "gate1": [],
    "team": ["audit-plan.json", "planning-memo.md", "risk-control-matrix.md", "audit-program.md",
             "samples", "pack-figures.json", "challenges.md", "review.md"],
    "gate2": [],
}

# scripts the spend-analyst writes itself: left out when the run includes that stage
AGENT_WRITTEN_SCRIPTS = ["clean.py", "analyse.py", "selfcheck.py"]


def _copy(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    elif src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def create(run_id: str, start_stage: str = "rules") -> Path:
    if start_stage not in STAGES:
        raise ValueError(f"unknown stage {start_stage}")
    ws = RUNS_DIR / run_id
    ws.mkdir(parents=True, exist_ok=False)
    for item in ("CLAUDE.md", "requirements.txt", "data", "scripts",
                 ".claude/agents", ".claude/skills", ".claude/agent-memory"):
        _copy(ROOT / item, ws / item)
    if STAGES.index(start_stage) <= STAGES.index("analysts"):
        for name in AGENT_WRITTEN_SCRIPTS:
            (ws / "scripts" / name).unlink(missing_ok=True)
    (ws / ".venv").symlink_to(ROOT / ".venv")
    out = ws / "outputs"
    out.mkdir()
    for stage in STAGES[: STAGES.index(start_stage)]:
        for name in STAGE_OUTPUTS[stage]:
            _copy(ROOT / "outputs" / name, out / name)
    return ws
