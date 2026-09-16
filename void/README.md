# Void — Ava007 Curation Workstation (Merged)

**Status:** Merged 2026-09-16 into the official hierarchy.

**Source:** [voideditor/void](https://github.com/voideditor/void) (VS Code fork, Apache 2.0 / MIT).  
Development paused / repo archived; source remains the preferred **reference base** for Ava007’s local-first, zero-copy curation workstation.

## Role in Hierarchy

```text
Cybernetic-Ava007                    ← Intellect
  └── a2a-exoskeleton                ← Substrate (this repo)
        ├── void/                    ← Curation Workstation (this folder)
        ├── forged-ai-filing-os      ← SPARC + turbovec intelligence layer
        └── fapo-ran                 ← RAN capability
              └── Ava007-Omni-OS
                    └── Agent-X
```

Void is **not** a second Intellect. It is the IDE / agent shell in which humans and Ava007 curate, separate, coordinate, refactor, and package intelligence before it is promoted through SPARC.

## Critical Properties Kept

1. **No middleman backend** — prompts go directly to providers or local Ollama / vLLM / LM Studio.
2. **Open source** — Apache 2.0 (Void) + MIT (VS Code base).
3. **Agent Mode** + **Gather Mode** + checkpoints + MCP.
4. **Type-safe** React 19 + Tailwind pipeline for contracts and BENTO-007 UI.

## Documents in this folder

| File | Purpose |
|------|---------|
| `SPARC_MAPPING.md` | Full layer-by-layer map onto Intake → Packaging → Training → UI |
| `INTEGRATION_CHECKLIST.md` | Concrete steps to fork/adapt Void for Ava007 |
| `HIERARCHY.md` | Position relative to Cybernetic-Ava007, QAG-MemBrain, Agent-X |

## Related

- Full original mapping also lives in `forged-ai-filing-os/docs/VOID_SPARC_MAPPING.md`
- Memory writes from Void MCP handlers → QAG-MemBrain / L1 Atom Store
- Semantic search from Void → turbovec index (forged-ai-filing-os)
