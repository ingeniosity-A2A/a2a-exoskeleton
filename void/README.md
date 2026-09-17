# Tekton Core — Ava007 Curation Workstation

**Former name:** Void  
**Status:** Merged 2026-09-16; brand updated to **Tekton Core** 2026-09-17.

**Source reference:** [voideditor/void](https://github.com/voideditor/void) (VS Code fork, Apache 2.0 / MIT).  
Folder path remains `void/` for git stability; **product name is Tekton Core**.

## Role in Hierarchy

```text
Cybernetic-Ava007
  └── a2a-exoskeleton
        ├── void/                 ← Tekton Core (curation workstation)
        ├── forged/               ← Forged filing (merge in progress)
        └── Ava007-Omni-OS       ← A2A / edge branch
              └── Agent-X
```

Tekton Core is **not** a second Intellect. It is the IDE / agent shell where humans and Ava007 curate, separate, coordinate, refactor, and package intelligence **before** promotion through Forged / SPARC into the Exoskeleton runtime.

## Critical Properties

1. **No middleman backend** — prompts go to providers or local Ollama / vLLM / LM Studio.
2. **Open source** — Apache 2.0 + MIT base.
3. **Agent Mode** + **Gather Mode** + checkpoints + MCP.
4. Type-safe React + Tailwind for contracts and Bento UI.

## Documents in this folder

| File | Purpose |
|------|--------|
| `SPARC_MAPPING.md` | Layer map onto Intake → Packaging → Training → UI |
| `INTEGRATION_CHECKLIST.md` | Fork/adapt steps for Ava007 |
| `HIERARCHY.md` | Position vs Cybernetic, QAG, Agent-X |
| `TOKEN_TAX_DEFENSE.md` | Harness flaw vs Forged + Exoskeleton zero-copy path |

## Related

- Mapping also in `forged-ai-filing-os/docs/VOID_SPARC_MAPPING.md` (legacy filename; content = Tekton Core)
- Memory writes → QAG-MemBrain
- Semantic search → turbovec (Forged layer)
