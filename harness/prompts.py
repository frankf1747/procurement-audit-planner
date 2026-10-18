"""Turn the repository's agent and skill files into system prompts."""
import re
from pathlib import Path

PREAMBLE = """You are running inside a standalone agent harness, not Claude Code.

Environment
- Your working directory is a private workspace that mirrors the project. Use paths relative to it
  (for example `outputs/rules.json`, `data/contract-rules.pdf`).
- Tools: {tools}. They replace Claude Code's Read/Write/Edit/Glob/Grep/Bash tools.
- `run` executes one command without a shell: no pipes, redirects or `&&`. Use `.venv/bin/python`
  for Python; write longer code to a file under `scripts/` and run it. pdftotext and pdfinfo are available.
- `data/`, `.claude/agents/`, `.claude/skills/`, `scripts/checks/`, `scripts/verify_history.py` and
  `CLAUDE.md` are read-only; writes there are refused.
- Your memory directory is `.claude/agent-memory/{name}/`; its MEMORY.md (if any) is shown below.
- Keep going until your task is complete, then finish with your report as plain text.
"""

TEAM_NOTE = """
Team messaging
- Your teammates are {others}; the lead is the harness, addressed as `lead`.
- Send a message with the `send_message` tool. It is delivered to the recipient verbatim.
- Messages you receive arrive as a user turn that starts with `Messages:`.
- When you are waiting for a reply, end your turn with a one-line status; you will be resumed
  when a message arrives. Do not end your turn while you still have work you can do now.
"""


def parse_agent(path: Path) -> dict:
    """Frontmatter (name, description, tools) and body of a .claude/agents/*.md file."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {"name": path.stem, "tools": [], "body": text}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    tools = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
    return {"name": meta.get("name", path.stem), "tools": tools, "body": m.group(2).strip(),
            "description": meta.get("description", "")}


def memory_text(ws: Path, name: str) -> str:
    mem = ws / ".claude" / "agent-memory" / name
    if not (mem / "MEMORY.md").exists():
        return "(no memory saved yet)"
    out = (mem / "MEMORY.md").read_text(encoding="utf-8")
    others = sorted(p.name for p in mem.glob("*.md") if p.name != "MEMORY.md")
    if others:
        out += "\n\nOther memory files you can read: " + ", ".join(others)
    return out


def system_prompt(ws: Path, name: str, role_text: str, tool_names: list, teammates: list = None) -> str:
    parts = [PREAMBLE.format(tools=", ".join(tool_names), name=name)]
    if teammates is not None:
        parts.append(TEAM_NOTE.format(others=", ".join(teammates)))
    parts.append("# Project brief (CLAUDE.md)\n\n" + (ws / "CLAUDE.md").read_text(encoding="utf-8"))
    parts.append("# Your role\n\n" + role_text)
    parts.append(f"# Your memory (.claude/agent-memory/{name}/MEMORY.md)\n\n" + memory_text(ws, name))
    return "\n\n".join(parts)


def agent_prompt(ws: Path, agent: str, tool_names: list, teammates: list = None) -> tuple:
    spec = parse_agent(ws / ".claude" / "agents" / f"{agent}.md")
    return system_prompt(ws, spec["name"], spec["body"], tool_names, teammates), spec


def skill_prompt(ws: Path, skill: str, tool_names: list) -> str:
    text = (ws / ".claude" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    role = (f"The human has invoked the `/{skill}` skill. Follow it exactly.\n\n" + body)
    return system_prompt(ws, skill, role, tool_names)
