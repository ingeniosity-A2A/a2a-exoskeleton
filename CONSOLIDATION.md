# Repository Consolidation — Official Hierarchy

**Date:** 2026-09-17  
**Authority:** ingeniosity-A2A / Ava007  
**Void merger:** Complete  
**Omni role:** A2A / edge branch of Exoskeleton (updated)

## Canonical Topology

```text
Cybernetic-Ava007                         ← Primary Intellect (sovereign)
  └── a2a-exoskeleton                     ← Substrate / execution boundary (THIS REPO)
        ├── main                           ← Core substrate (DuckDB, transport, kernel)
        ├── forged/  OR branch forged-ai-filing-os
        │     ← Forged-AI-Filing-OS intelligence layer MERGED HERE
        │        (SPARC, turbovec, forging pipeline, Lens, explorer)
        ├── void/                          ← Curation Workstation (Void reference)
        ├── branch: fapo-ran               ← RAN / FAPO capability
        └── Ava007-Omni-OS                 ← A2A / EDGE BRANCH OF EXOSKELETON
              │  Omnibus hub, Agent Browser ownership,
              │  enhanced bridge (Mercury T1 / vLLM T0 / reflex),
              │  S26 / Onomondo / ASIMCA edge path
              └── Agent-X                   ← Skills + consoles (client of hub)

QAG-MemBrain                              ← Memory authority
```

## Ownership Rules

| Concern | Owner |
|---------|--------|
| Intellect | Cybernetic-Ava007 |
| Execution substrate | **a2a-exoskeleton** (this repo) |
| Forged filing / intelligence OS | **Merged into a2a-exoskeleton** (not a competing top-level OS) |
| A2A / edge / Omnibus / Agent Browser | **Ava007-Omni-OS** as **branch of Exoskeleton** |
| Skills + Bento consoles | Agent-X (plugin/client; does not own Agent Browser) |
| Memory authority | QAG-MemBrain |

## UI / Hub (Forged parent)

```text
Omni-OS > Forged-OS (parent UI)
  └── Agent Browser
        ├── File Explorer
        ├── Agent Explorer
        ├── Intelligence Explorer
        ├── Terminal
        ├── ESA          ← Arrow JS sandbox A only
        └── HelpAssembly ← Arrow JS sandbox B only (separate)
```

## Merge Status — Forged into Exoskeleton

| Source | Action | Destination |
|--------|--------|-------------|
| `ingeniosity-A2A/forged-ai-filing-os` | **Merge in progress** | `a2a-exoskeleton` branch `forged-ai-filing-os` and/or `forged/` |
| Standalone `forged-ai-filing-os` repo | Remains until merge verified; then thin pointer or archive |
| Omni `Omnibus/forged_ai_filing_os/` | Align with merged Forged; Omni stays edge/A2A limb |

## Install Rule (no double-install)

- Install **a2a-exoskeleton** once (substrate).
- Forged is a **layer under Exoskeleton**, not a second top-level package name competing with `ava007`.
- Omni-OS is the **edge/A2A branch**, not a parallel OS above Exoskeleton.
- Agent-X attaches as client; does not own Omnibus or Agent Browser.

## Related Live Repos

- `Cybernetic-Ava007` — Intellect
- `a2a-exoskeleton` — Substrate + Void + **Forged merge target** (this repo)
- `forged-ai-filing-os` — Source tree being merged in
- `Ava007-Omni-OS` — **A2A / edge branch of Exoskeleton**
- `Agent-X` — Skills + consoles
- `QAG-MemBrain` — Memory authority
- `fapo-ran` — RAN capability branch
