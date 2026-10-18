"""The agent loop: one conversation per agent, tools executed by the harness."""
import json

from .config import MAX_TURNS_PER_AGENT
from .tools import ToolError, Toolbox


class AgentStopped(Exception):
    """The model refused, or the agent exceeded its turn budget."""


def _preview(value, n=220):
    s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n] + "…"


class Agent:
    def __init__(self, name: str, system: str, toolbox: Toolbox, llm, emit):
        self.name, self.system, self.toolbox, self.llm, self.emit = name, system, toolbox, llm, emit
        self.messages = []       # append-only, so thinking blocks stay valid across turns
        self.steps = 0

    def turn(self, user_content: str) -> str:
        """Add a user message and run the model until it ends its turn. Returns its final text."""
        self.messages.append({"role": "user", "content": user_content})
        while True:
            self.steps += 1
            if self.steps > MAX_TURNS_PER_AGENT:
                raise AgentStopped(f"{self.name} exceeded {MAX_TURNS_PER_AGENT} model calls")
            response = self.llm.create(self.system, self.toolbox.schemas(), self.messages)
            self.messages.append({"role": "assistant", "content": response.content})
            for block in response.content:
                if block.type == "thinking" and getattr(block, "thinking", ""):
                    self.emit(self.name, "thinking", _preview(block.thinking, 400))
                elif block.type == "text" and block.text.strip():
                    self.emit(self.name, "text", block.text)
                elif block.type == "fallback":
                    self.emit(self.name, "info", "a safeguard declined; the fallback model continued")

            if response.stop_reason == "refusal":
                raise AgentStopped(f"{self.name}: the model declined the request")
            if response.stop_reason == "pause_turn":
                continue
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            if response.stop_reason == "max_tokens" and not tool_uses:
                self.messages.append({"role": "user", "content": "Continue from where you stopped."})
                continue
            if not tool_uses:
                return "\n".join(b.text for b in response.content if b.type == "text").strip()

            results = []
            for tu in tool_uses:
                self.emit(self.name, "tool", f"{tu.name} {_preview(tu.input)}")
                if response.stop_reason == "max_tokens":
                    out, err = "tool input was cut off at max_tokens; send a smaller input", True
                else:
                    try:
                        out, err = self.toolbox.execute(tu.name, tu.input), False
                    except ToolError as e:
                        out, err = f"error: {e}", True
                    except Exception as e:  # a tool crash is reported to the model, not raised
                        out, err = f"error: {type(e).__name__}: {e}", True
                self.emit(self.name, "error" if err else "result", _preview(out, 300))
                results.append({"type": "tool_result", "tool_use_id": tu.id, "content": out, "is_error": err})
            self.messages.append({"role": "user", "content": results})


def make_agent(name: str, system: str, toolbox: Toolbox, llm, emit):
    """An API-loop Agent, or an Agent SDK agent when the backend is the Claude Code login."""
    if getattr(llm, "sdk", False):
        from .sdk_backend import SdkAgent
        return SdkAgent(name, system, toolbox, emit)
    return Agent(name, system, toolbox, llm, emit)
