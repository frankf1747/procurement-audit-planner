"""A standalone harness that runs the procurement audit planner outside Claude Code.

The repository is the source of truth: agent files in `.claude/agents/` become
system prompts, skills in `.claude/skills/` are the methods the agents read,
and the existing Python builders and verifiers are the tools that compute and
check. The harness supplies what Claude Code supplied in Part A: the agent
loop, sandboxed tools, team messaging, the human gates and a web UI.
"""
