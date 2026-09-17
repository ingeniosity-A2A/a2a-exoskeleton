# Repository Consolidation — Official Hierarchy

**Forged product name:** **Forged-Filing-Sys** (formerly Forged-AI-Filing-OS)

## Canonical Topology

```text
Cybernetic-Ava007                    ← Intelligence / firmware / ingestion
  └── a2a-exoskeleton                ← Substrate (this repo)
        ├── void/ · tekton-core      ← Curation workstation (IDE)
        ├── forged/                  ← Forged-Filing-Sys (canonical limb)
        ├── exoskeleton/             ← runtime / orchestration / transport
        └── → Ava007-Omni-OS         ← Edge / Omnibus integration only
              └── Agent-X            ← Execution adapters

QAG-MemBrain                         ← Memory authority
forged-ai-filing-os (GitHub)         ← HISTORICAL source only
```

## Forged merge status (authoritative)

| Item | State |
|------|--------|
| Source repository `forged-ai-filing-os` | **HISTORICAL** |
| Canonical implementation | **a2a-exoskeleton/forged/** |
| Product name | **Forged-Filing-Sys** |
| New development | **This repo only** |
| Omnibus/forged_ai_filing_os | Integration consumer / pointer — not a second implementation |
| Cybernetic-Ava007 | Intelligence authority; emits IR into Forged contracts |

## Rule

> Intelligence is promoted. Skills are packaged. Curation decides. **Forged-Filing-Sys records.** Sandboxes execute.

Do **not** put Refactoring Intelligence inside `forged/` as if Forged owned cognition. Unify **contracts and data flow**, not ownership boundaries.
