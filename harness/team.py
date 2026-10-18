"""The Phase 3 agent team: planner, challenger and qa-reviewer as peers.

Teammates message each other directly with the send_message tool; the harness
only delivers mail. An agent runs a turn whenever its inbox has messages, so
the challenger and qa-reviewer sit idle until the planner's PACK READY v1, and
the planner wakes for each CHALLENGE or QA failure. The lead (the harness)
records DONE reports, tells the qa-reviewer when the other two are done (it
must not write the final review before that), and stops when all three are
done or nobody has mail left.
"""
import re

from .agent import make_agent
from .prompts import agent_prompt, parse_agent
from .tools import Toolbox, tools_for

MEMBERS = ["planner", "challenger", "qa-reviewer"]
MAX_DELIVERIES = 40


class Team:
    def __init__(self, ws, llm, emit, gate_output: str):
        self.ws, self.llm, self.emit, self.gate_output = ws, llm, emit, gate_output
        self.inbox = {m: [] for m in MEMBERS}
        self.done = {}            # "planner" -> the DONE line
        self.blocked = None
        self.agents = {}
        self.started = set()
        for m in MEMBERS:
            spec = parse_agent(ws / ".claude" / "agents" / f"{m}.md")
            names = tools_for(spec["tools"])
            box = Toolbox(ws, names, send=self._sender(m))
            system, _ = agent_prompt(ws, m, box.names, teammates=[x for x in MEMBERS if x != m])
            self.agents[m] = make_agent(m, system, box, llm, emit)

    def _sender(self, frm):
        def send(to, message):
            to = to.strip().lower()
            self.emit(frm, "message", f"→ {to}: {message}")
            if to in self.inbox and to != frm:
                self.inbox[to].append(f"from {frm}: {message}")
                return f"delivered to {to}"
            if to == "lead":
                self._to_lead(frm, message)
                return "delivered to lead"
            return f"error: unknown recipient {to!r}; use one of {', '.join(MEMBERS + ['lead'])}"
        return send

    def _to_lead(self, frm, message):
        if re.search(r"\bBLOCKED\b", message) and "QA DONE" not in message:
            self.blocked = f"{frm}: {message}"
        for marker, who in (("PLANNER DONE", "planner"), ("CHALLENGER DONE", "challenger"), ("QA DONE", "qa-reviewer")):
            if marker in message:
                self.done[who] = message
                if who in ("planner", "challenger"):   # the qa-reviewer waits for both before writing review.md
                    self.inbox["qa-reviewer"].append(f"from lead: {who} reported: {message}")
        if "?" in message and not any(m in message for m in ("DONE", "BLOCKED")):
            self.inbox[frm].append("from lead: no further instruction; follow your agent file and CLAUDE.md.")

    def _deliver(self, m):
        msgs, self.inbox[m] = self.inbox[m], []
        head = ""
        if m not in self.started:
            head = ("You have been spawned as a teammate for the audit planning pack. The auditor gate is closed.\n\n")
            self.started.add(m)
        self.agents[m].turn(head + "Messages:\n" + "\n".join(msgs))

    def run(self) -> dict:
        self.started.add("planner")
        self.agents["planner"].turn(
            "You have been spawned as the planner. The auditor gate is closed; the lead's gate check printed:\n\n"
            f"{self.gate_output}\n\nStart now. Follow your agent file and the audit-program skill. When the builder "
            "reports no failures, send PACK READY v1 (with the builder's summary line) to challenger and qa-reviewer.")
        deliveries, nudged = 0, set()
        while deliveries < MAX_DELIVERIES and not self.blocked:
            pending = [m for m in MEMBERS if self.inbox[m]]
            if not pending:
                missing = [m for m in MEMBERS if m not in self.done and m not in nudged]
                if len(self.done) == len(MEMBERS) or not missing:
                    break
                for m in missing:      # one status nudge per teammate that went quiet before reporting done
                    nudged.add(m)
                    self.inbox[m].append("from lead: no messages are pending. If your protocol is complete, send your "
                                         "DONE message to lead now; otherwise finish what is outstanding.")
                continue
            for m in pending:
                deliveries += 1
                self._deliver(m)
        return {"done": self.done, "blocked": self.blocked, "deliveries": deliveries,
                "complete": len(self.done) == len(MEMBERS) and not self.blocked}
