# Repository Consolidation — Official Hierarchy

**Date:** 2026-09-16  
**Authority:** ingeniosity-A2A / Ava007

## Canonical Topology

```text
Cybernetic-Ava007                    ← Primary Intellect (sovereign)
  └── a2a-exoskeleton                ← Substrate / execution boundary (this repo)
        ├── branch: forged-ai-filing-os
        └── branch: fapo-ran
              └── merges into
                    Ava007-Omni-OS   ← Edge / modem / telemetry bridge
                      └── Agent-X    ← Skills + consoles surface
```

## Branch Status (this repo)

| Branch | Points to / Role |
|--------|------------------|
| `main` | Core a2a-exoskeleton substrate |
| `forged-ai-filing-os` | SPARC + turbovec + PDF/Image Lens + Void mapping (see `ingeniosity-A2A/forged-ai-filing-os`) |
| `fapo-ran` | RAN capability, FAPO Lyapunov, SafetyEnvelope (see `ingeniosity-A2A/fapo-ran`) |

## Merge & Delete Schedule

| Source | Action | Destination | Final |
|--------|--------|-------------|-------|
| **Core-Membrain** | Merge memory / graph / context-lake | **QAG-MemBrain** | Delete empty repo |
| **gitbook-ingest** | Merge docs-pipeline / wiki material | System wiki (a2a-exoskeleton/wiki or Cybernetic docs) | Delete empty repo |
| **Ava007** | Split | Intellect → **Cybernetic-Ava007**<br>Memory/rest → **QAG-MemBrain**<br>Edge → **Ava007-Omni-OS**<br>Skills surface → **Agent-X** | Delete empty repo |

## Install Rule (no double-install)

- Install `a2a-exoskeleton` once (this repo).
- Install `fapo-ran-capability` from the `fapo-ran` branch or the standalone `fapo-ran` repo (thin `ava007.capabilities` surface only).
- Do **not** publish a competing top-level `ava007` package from any other repo.
- TypeScript surfaces (Ava007 legacy UI, QAG-MemBrain, Agent-X) remain separate runtimes.

## Related Live Repos (post-consolidation)

- `Cybernetic-Ava007` — Intellect only
- `a2a-exoskeleton` — Substrate (this repo)
- `forged-ai-filing-os` — Intelligence filing OS (absorbed via branch)
- `fapo-ran` — RAN capability (absorbed via branch)
- `Ava007-Omni-OS` — Edge bridge
- `Agent-X` — Skills + consoles
- `QAG-MemBrain` — Memory authority (receives Core-Membrain)

Empty shells to delete after content verification: `gitbook-ingest`, `Core-Membrain`, `Ava007`.
