"""The Claude API call, isolated so tests can swap in a scripted model."""
import anthropic

from .config import EFFORT, MAX_TOKENS, MODEL


class ClaudeLLM:
    """One streamed Messages API call per agent step.

    - claude-opus-5-5 with adaptive thinking (summaries shown in the UI) and explicit effort;
    - streamed, so large tool inputs (files the agents write) never hit an HTTP timeout;
    - server-side refusal fallbacks ("default" routing) so a safeguard decline is retried on a
      fallback model inside the same call;
    - top-level prompt caching: the long, stable system prompt and the growing history are reused.
    """

    def __init__(self, client: anthropic.Anthropic = None):
        self.client = client or anthropic.Anthropic()

    def create(self, system: str, tools: list, messages: list):
        with self.client.beta.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            tools=tools,
            messages=messages,
            thinking={"type": "adaptive", "display": "summarized"},
            output_config={"effort": EFFORT},
            cache_control={"type": "ephemeral"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        ) as stream:
            return stream.get_final_message()
