# Repository Consolidation — Official Hierarchy

**Date:** 2026-09-16  
**Authority:** ingeniosity-A2A / Ava007  
**Void merger:** Complete

## Canonical Topology

```text
Cybernetic-Ava007                    ← Primary Intellect (sovereign)
  └── a2a-exoskeleton                ← Substrate / execution boundary (this repo)
        ├── void/                    ← Curation Workstation (Void VS Code fork reference)
        ├── branch: forged-ai-filing-os
        └── branch: fapo-ran
              └── merges into
                    Ava007-Omni-OS   ← Edge / modem / telemetry bridge
                      └── Agent-X    ← Skills + consoles surface

QAG-MemBrain                         ← Memory authority (Core-Membrain absorbed)
```

## Branch / Folder Status (this repo)

| Path | Role |
|------|------|
| `main` | Core a2a-exoskeleton substrate |
| `void/` | **Curation Workstation** — SPARC-mapped Void reference (merged) |
| `forged-ai-filing-os` (branch) | SPARC + turbovec + PDF/Image Lens |
| `fapo-ran` (branch) | RAN capability, FAPO Lyapunov, SafetyEnvelope |
| `wiki/` | System wiki (gitbook-ingest absorbed) |

## Merge & Delete Schedule

| Source | Action | Destination | Final |
|--------|--------|-------------|-------|
| **Core-Membrain** | Merged | **QAG-MemBrain** (`memory/core-membrain/`) | Delete empty repo |
| **gitbook-ingest** | Merged | `wiki/gitbook-ingest/` | Delete empty repo |
| **Ava007** | Split | Intellect → Cybernetic-Ava007; Memory → QAG-MemBrain; Edge → Omni-OS | Delete empty repo |
| **Void** (upstream) | Reference merged | `void/` (this repo) | Upstream stays archived; we own the mapping |

## Install Rule (no double-install)

- Install `a2a-exoskeleton` once.
- Install `fapo-ran-capability` from the `fapo-ran` branch or standalone repo (thin `ava007.capabilities` only).
- Do **not** publish a competing top-level `ava007` package from any other repo.
- Void is a *fork reference*, not an npm/pip package of this monorepo.

## Related Live Repos

- `Cybernetic-Ava007` — Intellect only
- `a2a-exoskeleton` — Substrate + Void workstation (this repo)
- `forged-ai-filing-os` — Intelligence filing OS
- `fapo-ran` — RAN capability
- `Ava007-Omni-OS` — Edge bridge
- `Agent-X` — Skills + consoles
- `QAG-MemBrain` — Memory authority

Empty shells to delete after verification: `gitbook-ingest`, `Core-Membrain`, `Ava007`.
