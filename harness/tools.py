"""Sandboxed tools the agents call, scoped to one run workspace.

Each agent gets only the tools its `.claude/agents/*.md` frontmatter lists
(Read, Write, Edit, Glob, Grep, Bash), mapped to the functions below.
Protections that were instructions in Part A are enforced here: writes to the
inputs, the agent and skill definitions and the QA scripts are refused, paths
cannot leave the workspace, and commands run without a shell from a short
allow-list. This is a guard rail for local use, not a security boundary
against a hostile model: a Python script an agent writes can still do what
Python can do, so run the harness only on your own machine.
"""
import fnmatch
import re
import shlex
import subprocess
from pathlib import Path

from .config import COMMAND_TIMEOUT, OUTPUT_LIMIT, PYTHON

PROTECTED = ("data/", ".claude/agents/", ".claude/skills/", "scripts/checks/",
             "scripts/verify_history.py", "CLAUDE.md")
ALLOWED_COMMANDS = {"python", "python3", ".venv/bin/python", "pdftotext", "pdfinfo", "head", "tail",
                    "wc", "ls", "cat", "grep", "mkdir", "shasum", "sort", "uniq", "cut", "find", "diff"}
SHELL_TOKENS = {"|", "||", "&&", ";", ">", ">>", "<", "&", "2>", "2>&1", "<<"}

TOOL_SPECS = {
    "read_file": {
        "description": "Read a text file in the workspace. Returns numbered lines. Use offset/limit for long files.",
        "input_schema": {"type": "object", "properties": {
            "path": {"type": "string"}, "offset": {"type": "integer", "description": "first line, 1-based"},
            "limit": {"type": "integer", "description": "max lines (default 2000)"}},
            "required": ["path"], "additionalProperties": False}},
    "write_file": {
        "description": "Create or overwrite a file in the workspace with the given content.",
        "input_schema": {"type": "object", "properties": {
            "path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"], "additionalProperties": False}},
    "edit_file": {
        "description": "Replace one exact, unique occurrence of old_string with new_string in a file.",
        "input_schema": {"type": "object", "properties": {
            "path": {"type": "string"}, "old_string": {"type": "string"}, "new_string": {"type": "string"}},
            "required": ["path", "old_string", "new_string"], "additionalProperties": False}},
    "list_files": {
        "description": "List workspace files matching a glob pattern, e.g. 'outputs/**/*.csv' or 'data/committee/*'.",
        "input_schema": {"type": "object", "properties": {"pattern": {"type": "string"}},
                         "required": ["pattern"], "additionalProperties": False}},
    "grep": {
        "description": "Search file contents with a regular expression. path is a file or folder (default: whole workspace).",
        "input_schema": {"type": "object", "properties": {
            "pattern": {"type": "string"}, "path": {"type": "string"}},
            "required": ["pattern"], "additionalProperties": False}},
    "run": {
        "description": ("Run one command in the workspace without a shell (no pipes or redirects). Allowed programs: "
                        + ", ".join(sorted(ALLOWED_COMMANDS)) + ". Returns exit code, stdout and stderr."),
        "input_schema": {"type": "object", "properties": {"command": {"type": "string"}},
                         "required": ["command"], "additionalProperties": False}},
    "send_message": {
        "description": "Send a message to a teammate or to the lead. It is delivered verbatim.",
        "input_schema": {"type": "object", "properties": {
            "to": {"type": "string"}, "message": {"type": "string"}},
            "required": ["to", "message"], "additionalProperties": False}},
}

# Claude Code tool names in agent frontmatter -> harness tools
FRONTMATTER_MAP = {"Read": ["read_file"], "Write": ["write_file"], "Edit": ["edit_file"],
                   "Glob": ["list_files"], "Grep": ["grep"], "Bash": ["run"]}
ALL_TOOLS = ["read_file", "write_file", "edit_file", "list_files", "grep", "run"]


def tools_for(frontmatter_tools: list) -> list:
    names = []
    for t in frontmatter_tools:
        for n in FRONTMATTER_MAP.get(t, []):
            if n not in names:
                names.append(n)
    return names


class ToolError(Exception):
    pass


class Toolbox:
    def __init__(self, ws: Path, names: list, send=None):
        self.ws = ws.resolve()
        self.names = list(names) + (["send_message"] if send else [])
        self.send = send

    # ---- schemas sent to the API
    def schemas(self) -> list:
        return [{"name": n, **TOOL_SPECS[n], "eager_input_streaming": True} for n in self.names]

    # ---- helpers
    def _path(self, p: str, write: bool = False) -> Path:
        if not isinstance(p, str) or not p.strip():
            raise ToolError("path must be a non-empty string")
        full = (self.ws / p).resolve() if not p.startswith("/") else Path(p).resolve()
        try:
            rel = full.relative_to(self.ws).as_posix()
        except ValueError:
            raise ToolError(f"path {p!r} is outside the workspace")
        if write and any(rel == x.rstrip("/") or rel.startswith(x) for x in PROTECTED):
            raise ToolError(f"{rel} is read-only in this harness")
        return full

    @staticmethod
    def validate(name: str, args) -> None:
        """Check a (possibly eagerly streamed) tool input against its schema."""
        if not isinstance(args, dict):
            raise ToolError("tool input must be a JSON object")
        schema = TOOL_SPECS[name]["input_schema"]
        missing = [k for k in schema["required"] if k not in args]
        if missing:
            raise ToolError(f"missing required fields {missing}")
        for k, v in args.items():
            spec = schema["properties"].get(k)
            if spec is None:
                raise ToolError(f"unknown field {k!r}")
            if spec["type"] == "string" and not isinstance(v, str):
                raise ToolError(f"{k} must be a string")
            if spec["type"] == "integer" and (not isinstance(v, int) or isinstance(v, bool)):
                raise ToolError(f"{k} must be an integer")

    def execute(self, name: str, args: dict) -> str:
        if name not in self.names:
            raise ToolError(f"tool {name} is not available to this agent")
        self.validate(name, args)
        return getattr(self, f"t_{name}")(**args)

    # ---- tools
    def t_read_file(self, path, offset=1, limit=2000):
        f = self._path(path)
        if not f.is_file():
            raise ToolError(f"{path} is not a file")
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        start = max(1, offset)
        chunk = lines[start - 1: start - 1 + max(1, limit)]
        body = "\n".join(f"{i:6}\t{l}" for i, l in enumerate(chunk, start))
        more = len(lines) - (start - 1 + len(chunk))
        return body + (f"\n... {more} more lines (use offset)" if more > 0 else "")

    def t_write_file(self, path, content):
        f = self._path(path, write=True)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
        return f"wrote {f.relative_to(self.ws)} ({len(content)} characters)"

    def t_edit_file(self, path, old_string, new_string):
        f = self._path(path, write=True)
        text = f.read_text(encoding="utf-8")
        n = text.count(old_string)
        if n != 1:
            raise ToolError(f"old_string found {n} times; it must be unique")
        f.write_text(text.replace(old_string, new_string), encoding="utf-8")
        return f"edited {f.relative_to(self.ws)}"

    def t_list_files(self, pattern):
        hits = sorted(p.relative_to(self.ws).as_posix() for p in self.ws.glob(pattern)
                      if ".venv" not in p.parts and "__pycache__" not in p.parts)
        return "\n".join(hits[:500]) + (f"\n... {len(hits) - 500} more" if len(hits) > 500 else "") or "(no matches)"

    def t_grep(self, pattern, path="."):
        try:
            rx = re.compile(pattern)
        except re.error as e:
            raise ToolError(f"bad regex: {e}")
        root = self._path(path)
        files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()
                                               and ".venv" not in p.parts and p.suffix not in (".pdf", ".xlsx", ".pyc")]
        out = []
        for f in sorted(files):
            try:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if rx.search(line):
                        out.append(f"{f.relative_to(self.ws)}:{i}: {line[:300]}")
                        if len(out) >= 200:
                            return "\n".join(out) + "\n... (stopped at 200 matches)"
            except OSError:
                continue
        return "\n".join(out) or "(no matches)"

    def t_run(self, command):
        try:
            argv = shlex.split(command)
        except ValueError as e:
            raise ToolError(f"cannot parse command: {e}")
        if not argv:
            raise ToolError("empty command")
        if argv[0] not in ALLOWED_COMMANDS:
            raise ToolError(f"{argv[0]} is not an allowed program")
        if any(a in SHELL_TOKENS for a in argv):
            raise ToolError("pipes, redirects and command chaining are not supported; run one command")
        for a in argv[1:]:
            if a.startswith("/") and not a.startswith(str(self.ws)) and Path(a).exists():
                raise ToolError(f"{a} is outside the workspace")
            if "../" in a or a == "..":
                raise ToolError("paths may not leave the workspace")
        if argv[0] in ("python", "python3", ".venv/bin/python"):
            argv[0] = str(PYTHON)
        try:
            p = subprocess.run(argv, cwd=self.ws, capture_output=True, text=True, timeout=COMMAND_TIMEOUT)
        except subprocess.TimeoutExpired:
            raise ToolError(f"command timed out after {COMMAND_TIMEOUT}s")
        out = f"exit code {p.returncode}\n--- stdout\n{p.stdout}\n--- stderr\n{p.stderr}"
        if len(out) > OUTPUT_LIMIT:
            out = out[:OUTPUT_LIMIT] + f"\n... output truncated at {OUTPUT_LIMIT} characters"
        return out

    def t_send_message(self, to, message):
        return self.send(to, message)
