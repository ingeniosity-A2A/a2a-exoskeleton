# Void Agent — Merge Decision

**Decision (2026-09-17): STAY IN IDE. Do not merge into Cybernetic-Ava007.**

## Why

| Concern | Owner |
|---------|--------|
| **Void Agent Mode** (search, edit, delete, terminal, MCP) | **IDE** — `a2a-exoskeleton/void/` |
| **Intellect agent loop** (perceive → infer → intent → propose) | **Cybernetic-Ava007** — `inferential-kernel/` |
| **Free buff / consolidation capacity** | Already present — Freebuff package + SuperLoop / kernel; no need to absorb Void’s agent into Intellect |

Void Agent is a *curation tool surface* (how a human or operator acts on the repo inside the editor).  
Ava007’s agent is *cognition* (how she forms Intent). Merging them would blur the hard boundary and duplicate what Freebuff + inferential-kernel already cover.

## Rule

```text
Void Agent  →  stays in void/ (IDE)
Ava007 Agent loop  →  stays in Cybernetic-Ava007
Free buff  →  keep; do not replace with Void Agent
```

If MCP tools in Void need to *call* Ava007 Intent emission, wire them as **clients** of Cybernetic-Ava007 / a2a-exoskeleton contracts — not as a second mind inside the Intellect repo.
