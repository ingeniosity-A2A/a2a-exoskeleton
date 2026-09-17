# Repository Consolidation — Official Hierarchy

**Date:** 2026-09-17  
**Authority:** ingeniosity-A2A / Ava007  
**Curation workstation brand:** **Tekton Core** (formerly Void; path `void/`)  
**Omni role:** A2A / edge branch of Exoskeleton

## Canonical Topology

```text
Cybernetic-Ava007                         ← Primary Intellect
  └── a2a-exoskeleton                     ← Substrate (THIS REPO)
        ├── main                           ← Core (DuckDB, Arrow transport, kernel)
        ├── forged/                        ← Forged-AI-Filing-OS (merge in progress)
        ├── void/                          ← Tekton Core (curation workstation)
        ├── branch: fapo-ran               ← RAN / FAPO
        └── Ava007-Omni-OS                 ← A2A / EDGE BRANCH
              └── Agent-X                   ← Skills + consoles (client)

QAG-MemBrain                              ← Memory authority
```

## Token tax / harness flaw — who solves what

| Layer | Role |
|-------|------|
| **Tekton Core** | Curate before promotion (reduce volume) |
| **Forged** | Govern F0→F3; classify Skills vs Intelligence; stop blind JSON-as-source-of-truth **upstream** |
| **Exoskeleton** | **Runtime defense:** Arrow columnar state + Flight + DuckDB in-place zero-copy |

Forged reduces what enters the hot path; **Exoskeleton** eliminates pack/unpack on the hot path. See `void/TOKEN_TAX_DEFENSE.md`.

## Ownership Rules

| Concern | Owner |
|---------|--------|
| Intellect | Cybernetic-Ava007 |
| Execution + zero-copy membrane | **a2a-exoskeleton** |
| Forged filing | Merged into **a2a-exoskeleton/forged/** |
| Curation IDE | **Tekton Core** (`void/`) |
| A2A / Omnibus / Agent Browser | **Ava007-Omni-OS** |
| Skills + Bento consoles | Agent-X (client) |
| Memory authority | QAG-MemBrain |

## Install Rule

- Install **a2a-exoskeleton** once.
- Forged is a layer under Exoskeleton, not a competing top-level OS.
- Omni-OS is the edge/A2A branch, not above Exoskeleton.
