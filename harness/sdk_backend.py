"""Backend 2: run each agent through the Claude Agent SDK on your Claude Code login.

No API key is needed: the SDK drives the locally installed `claude` CLI, which
uses whatever account you are signed in to. The harness keeps its own
architecture: Claude Code's built-in tools are switched off (`tools=[]`),
project settings are not loaded (`setting_sources=[]`), the system prompt is
the harness prompt, and the only tools are the harness tools, served from an
in-process MCP server so the same sandbox rules and team messaging apply.
Each agent's conversation continues from turn to turn with `resume`.
"""
import asyncio
import shutil

from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, ThinkingBlock,
                              create_sdk_mcp_server, query, tool)

from .agent import AgentStopped, _preview
from .config import EFFORT, MAX_TURNS_PER_AGENT, MODEL
from .tools import TOOL_SPECS, ToolError, Toolbox

SERVER = "harness"


def available() -> bool:
    return shutil.which("claude") is not None


class ClaudeCodeLLM:
    """Marker passed through the pipeline; agents built with it use SdkAgent."""
    sdk = True


class SdkAgent:
    def __init__(self, name: str, system: str, toolbox: Toolbox, emit):
        self.name, self.system, self.toolbox, self.emit = name, system, toolbox, emit
        self.session_id = None
        self.cost = 0.0
        self.server = create_sdk_mcp_server(SERVER, tools=[self._wrap(n) for n in toolbox.names])

    def _wrap(self, name):
        @tool(name, TOOL_SPECS[name]["description"], TOOL_SPECS[name]["input_schema"])
        async def handler(args):
            self.emit(self.name, "tool", f"{name} {_preview(args)}")
            try:
                out, err = await asyncio.to_thread(self.toolbox.execute, name, args), False
            except ToolError as e:
                out, err = f"error: {e}", True
            except Exception as e:
                out, err = f"error: {type(e).__name__}: {e}", True
            self.emit(self.name, "error" if err else "result", _preview(out, 300))
            return {"content": [{"type": "text", "text": out}], "is_error": err}
        return handler

    def _options(self):
        return ClaudeAgentOptions(
            system_prompt=self.system,
            tools=[],                                   # no Claude Code built-in tools
            mcp_servers={SERVER: self.server},
            allowed_tools=[f"mcp__{SERVER}__{n}" for n in self.toolbox.names],
            setting_sources=[],                         # do not load project or user settings
            cwd=str(self.toolbox.ws),
            model=MODEL,
            effort=EFFORT,
            max_turns=MAX_TURNS_PER_AGENT,
            resume=self.session_id,
        )

    async def _turn(self, prompt: str) -> str:
        final = None
        async for msg in query(prompt=prompt, options=self._options()):
            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, ThinkingBlock) and b.thinking:
                        self.emit(self.name, "thinking", _preview(b.thinking, 400))
                    elif isinstance(b, TextBlock) and b.text.strip():
                        self.emit(self.name, "text", b.text)
            elif isinstance(msg, ResultMessage):
                self.session_id = msg.session_id
                self.cost += msg.total_cost_usd or 0
                if msg.is_error:
                    raise AgentStopped(f"{self.name}: {msg.subtype} {msg.errors or msg.result or ''}".strip())
                final = msg.result or ""
        return final or ""

    def turn(self, user_content: str) -> str:
        return asyncio.run(self._turn(user_content))
