"""Paths, model settings and the local .env loader."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # the repository
RUNS_DIR = ROOT / "runs"                             # one workspace per run (git-ignored)
PYTHON = ROOT / ".venv" / "bin" / "python"           # the project venv runs every script

MODEL = os.environ.get("HARNESS_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("HARNESS_EFFORT", "high")
MAX_TOKENS = 64000                                   # streamed, so no HTTP timeout concern
MAX_TURNS_PER_AGENT = int(os.environ.get("HARNESS_MAX_TURNS", "60"))
COMMAND_TIMEOUT = 600                                # seconds per tool command
OUTPUT_LIMIT = 20000                                 # characters of tool output returned to the model


def load_env(path: Path = ROOT / ".env") -> None:
    """Read KEY=VALUE lines from .env into os.environ (existing values win)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
